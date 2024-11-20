#pragma once
#include "stdafx.h"
#include "Server.h"
#include "Object.h"
#include <windows.h>
#include "../protocol.h"

DWORD WINAPI ServerMain(LPVOID arg);
DWORD WINAPI ProcessClient(LPVOID arg);
DWORD WINAPI ServerUpdateThread(LPVOID arg);

CRITICAL_SECTION cs_server_program; // ���� �Ӱ� ����

Server server_program;

int main()
{
    // ���� ���� ������ ����
    HANDLE hServerThread = CreateThread(NULL, 0, ServerMain, NULL, 0, NULL);
    if (hServerThread == NULL) {
        std::cerr << "Failed to create server thread." << std::endl;
        return 1;
    }

    // ���� ���� �����尡 ���� ������ ��ٸ���
    WaitForSingleObject(hServerThread, INFINITE);
    return 0;
}

// ���� ���� ������ == Ŭ�� ���� ������
DWORD WINAPI ServerMain(LPVOID arg)
{
    int retval;

    // ���� �ʱ�ȭ
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return 1;

    // ���� ����
    SOCKET listen_sock = socket(AF_INET, SOCK_STREAM, 0);
    if (listen_sock == INVALID_SOCKET)
        err_quit("socket()");

    // bind()
    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
    serveraddr.sin_port = htons(SERVERPORT);
    retval = bind(listen_sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr));
    if (retval == SOCKET_ERROR)
        err_quit("bind()");

    // listen()
    retval = listen(listen_sock, SOMAXCONN);
    if (retval == SOCKET_ERROR)
        err_quit("listen()");

    // ���� ������Ʈ ������ ����
    HANDLE hUpdateThread = CreateThread(NULL, 0, ServerUpdateThread, NULL, 0, NULL);
    if (hUpdateThread == NULL)
    {
        std::cerr << "Failed to create server update thread." << std::endl;
        return 1;
    }

    // Ŭ���̾�Ʈ ���� ��� �� ó��
    while (true)
    {
        // �÷��̾ 2�� ��� ����� ���, ���� ��⸦ ����
        if (server_program.Get_Player(1) != NULL && server_program.Get_Player(2) != NULL)
        {
            // 2���� �÷��̾ ��� ����Ǿ��� ��� ��� ����
            SOCKET client_sock = accept(listen_sock, NULL, NULL);
            if (client_sock == INVALID_SOCKET)
            {
                std::cerr << "accept() failed" << std::endl;
                continue;
            }
            continue;
        }
    //while (true)
    //{
    //    // �÷��̾� ���� ���� Ȯ��
    //    bool player1_connected = (server_program.Get_Player(1) != NULL);
    //    bool player2_connected = (server_program.Get_Player(2) != NULL);

    //    // �� �� ��� ����� ���
    //    if (player1_connected && player2_connected)
    //    {
    //        // ���� ���� ���������� Ȯ��
    //        Sleep(100); // CPU ������ ������ ���� ��� ���
    //        continue;
    //    }
        //===========================================

        struct sockaddr_in clientaddr;
        int addrlen = sizeof(clientaddr);
        SOCKET client_sock = accept(listen_sock, (struct sockaddr*)&clientaddr, &addrlen);
        if (client_sock == INVALID_SOCKET)
        {
            std::cerr << "accept() failed" << std::endl;
            continue;
        }

        // Ŭ���̾�Ʈ ���� �ʱ�ȭ
        Client_Info* client_info = new Client_Info;
        client_info->socket = client_sock;
        client_info->player_N = 0;

        // ������ ����� �÷��̾� 2������ ���� // ���������� player_N 1 or 2�� ó����
        if (server_program.Get_Player(1) == NULL)
            client_info->player_N = 1;
        else if (server_program.Get_Player(2) == NULL)
            client_info->player_N = 2;

        HANDLE hThread = CreateThread(NULL, 0, ProcessClient, (LPVOID)client_info, 0, NULL);
        if (hThread == NULL)
        {
            std::cerr << "Failed to create client thread." << std::endl;
            closesocket(client_sock);
        }
        else
        {
            CloseHandle(hThread);
        }
    }

    // ���� �ݱ�
    closesocket(listen_sock);

    // ���� ����
    WSACleanup();
    return 0;
}

// ���� ������Ʈ ������
DWORD WINAPI ServerUpdateThread(LPVOID arg)
{
    int target_fps =60;  // ��ǥ FPS ���� (60FPS)
    server_program.Set_FrameRate(target_fps);  // ���� Ÿ�̸� ����
    
    while (true)
    {
        // �÷��̾ �ϳ��� ����Ǹ� ���� ������Ʈ
        if (server_program.Get_Player(1) == NULL && server_program.Get_Player(2) == NULL)
        {
            // ����� �÷��̾ ������ ������Ʈ �� ��
            continue;
        }

        // ť�� ����� Ű �Է� ó��
        std::pair<int, Key_Info> keyInfo;

        // ť�� ����� Ű �Է��� ���ٸ�
        if (server_program.Get_Key_Input_Buffer_size() == 0)
        {
            keyInfo.first = 1;
            keyInfo.second.key_action = 1;
            keyInfo.second.key_name = 0;
            server_program.Decoding(&keyInfo);

            keyInfo.first = 2;
            server_program.Decoding(&keyInfo);
        }
        else
        {
            int processedCount = 0;
            while (server_program.DequeueKeyInput(keyInfo) && processedCount < MAX_INPUT_PER_FRAME)
            {
                server_program.Decoding(&keyInfo);
                processedCount++;
            }
        }

        // float�� ��� �ð� �ޱ�
        float ElapsedTime = server_program.Get_ElapsedTime();
        server_program.Update_Server(ElapsedTime);
        server_program.Update_Collision();
        Game_Data* sending_data = server_program.Encoding();
        server_program.Broadcast_GameData_All(sending_data);

        // ��� �ð� �� FPS�� ���� ���
        server_program.Wait();
    }

    return 0;
}

// Ŭ���̾�Ʈ ó�� ������
DWORD WINAPI ProcessClient(LPVOID arg)
{
    Client_Info* clientInfo = (Client_Info*)arg;

    // clientInfo�� �߸��� ���̸� �����带 ����
    if (clientInfo == nullptr || clientInfo->player_N == 0)
    {
        delete clientInfo;
        return 1;
    }

    int addrlen;
    char addr[INET_ADDRSTRLEN];
    struct sockaddr_in clientaddr;
    SOCKET client_sock = clientInfo->socket;

    // Ŭ���̾�Ʈ ���� ���
    addrlen = sizeof(clientaddr);
    getpeername(client_sock, (struct sockaddr*)&clientaddr, &addrlen);
    inet_ntop(AF_INET, &clientaddr.sin_addr, addr, sizeof(addr));

    int Client_N = clientInfo->player_N;

    Object* player = new Player();

    if (Client_N == 1)
        server_program.Add_P1(player, CHARACTER_SASUKE);
    else if (Client_N == 2)
        server_program.Add_P2(player, CHARACTER_SASUKE);
    else
        std::cout << "Client_N ���� ���� �߻�" << std::endl;

    server_program.Add_Client_Socket(client_sock, Client_N);
    
    std::cout << Client_N << "P Ŭ���̾�Ʈ �����: IP �ּ�=" << addr << ", ��Ʈ ��ȣ=" << ntohs(clientaddr.sin_port) << "\r\n";


    Key_Info keyInfo;
    while (true)
    {
        // Key_Info ������ ������ �ޱ�
        int retval = recv(client_sock, (char*)&keyInfo, sizeof(Key_Info), 0);
        if (retval == SOCKET_ERROR)
        {
            int error = WSAGetLastError();
            std::cerr << "recv() error: " << error << std::endl;
            break;
        }
        else if (retval == 0)
        {
            // Ŭ���̾�Ʈ�� ���� ����
            std::cout << Client_N << "P Disconnected\n";
            break;
        }
        else if (retval > 0)
        {
            // ���޹��� Key_Info ���� ���
            std::cout << "Player: " << Client_N 
                << ", Received KeyCode: " << keyInfo.key_name 
                << ", ActionType: " << (keyInfo.key_action == 1 ? "Down" : (keyInfo.key_action == 2 ? "Up" : "Unknown")) 
                << "\r\n";

                // Ű ������Ʈ ȣ��
                server_program.EnqueueKeyInput(Client_N, keyInfo);
        }
    }

    // ���� �ݱ� �� Ŭ���̾�Ʈ ���� ����
    closesocket(client_sock);
    std::cout << Client_N << "P Disconnected\n";
    std::cout << "Ŭ���̾�Ʈ ����: IP �ּ�=" << addr << ", ��Ʈ ��ȣ=" << ntohs(clientaddr.sin_port) << "\r\n";

    server_program.Remove_Player(Client_N);
    server_program.Remove_Client_Socket(Client_N);

    // ���� �Ҵ�� �޸� ����
    delete clientInfo;
    return 0;
}
