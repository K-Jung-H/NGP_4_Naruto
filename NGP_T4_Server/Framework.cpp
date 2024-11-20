#pragma once
#include "stdafx.h"
#include "Server.h"
#include "Object.h"
#include <windows.h>
#include "../protocol.h"

DWORD WINAPI ServerMain(LPVOID arg);
DWORD WINAPI ProcessClient(LPVOID arg);
DWORD WINAPI ServerUpdateThread(LPVOID arg);

CRITICAL_SECTION cs_server_program; // 서버 임계 영역

Server server_program;

int main()
{
    // 서버 메인 스레드 시작
    HANDLE hServerThread = CreateThread(NULL, 0, ServerMain, NULL, 0, NULL);
    if (hServerThread == NULL) {
        std::cerr << "Failed to create server thread." << std::endl;
        return 1;
    }

    // 서버 메인 스레드가 끝날 때까지 기다리기
    WaitForSingleObject(hServerThread, INFINITE);
    return 0;
}

// 서버 메인 스레드 == 클라 연결 스레드
DWORD WINAPI ServerMain(LPVOID arg)
{
    int retval;

    // 윈속 초기화
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return 1;

    // 소켓 생성
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

    // 서버 업데이트 스레드 시작
    HANDLE hUpdateThread = CreateThread(NULL, 0, ServerUpdateThread, NULL, 0, NULL);
    if (hUpdateThread == NULL)
    {
        std::cerr << "Failed to create server update thread." << std::endl;
        return 1;
    }

    // 클라이언트 연결 대기 및 처리
    while (true)
    {
        // 플레이어가 2명 모두 연결된 경우, 연결 대기를 중지
        if (server_program.Get_Player(1) != NULL && server_program.Get_Player(2) != NULL)
        {
            // 2명의 플레이어가 모두 연결되었을 경우 대기 중지
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
    //    // 플레이어 연결 상태 확인
    //    bool player1_connected = (server_program.Get_Player(1) != NULL);
    //    bool player2_connected = (server_program.Get_Player(2) != NULL);

    //    // 두 명 모두 연결된 경우
    //    if (player1_connected && player2_connected)
    //    {
    //        // 연결 상태 지속적으로 확인
    //        Sleep(100); // CPU 과부하 방지를 위해 잠시 대기
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

        // 클라이언트 정보 초기화
        Client_Info* client_info = new Client_Info;
        client_info->socket = client_sock;
        client_info->player_N = 0;

        // 서버에 연결될 플레이어 2명으로 제한 // 서버에서는 player_N 1 or 2만 처리함
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

    // 소켓 닫기
    closesocket(listen_sock);

    // 윈속 종료
    WSACleanup();
    return 0;
}

// 서버 업데이트 스레드
DWORD WINAPI ServerUpdateThread(LPVOID arg)
{
    int target_fps =60;  // 목표 FPS 설정 (60FPS)
    server_program.Set_FrameRate(target_fps);  // 서버 타이머 시작
    
    while (true)
    {
        // 플레이어가 하나라도 연결되면 서버 업데이트
        if (server_program.Get_Player(1) == NULL && server_program.Get_Player(2) == NULL)
        {
            // 연결된 플레이어가 없으면 업데이트 안 함
            continue;
        }

        // 큐에 저장된 키 입력 처리
        std::pair<int, Key_Info> keyInfo;

        // 큐에 저장된 키 입력이 없다면
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

        // float로 경과 시간 받기
        float ElapsedTime = server_program.Get_ElapsedTime();
        server_program.Update_Server(ElapsedTime);
        server_program.Update_Collision();
        Game_Data* sending_data = server_program.Encoding();
        server_program.Broadcast_GameData_All(sending_data);

        // 경과 시간 후 FPS에 맞춰 대기
        server_program.Wait();
    }

    return 0;
}

// 클라이언트 처리 스레드
DWORD WINAPI ProcessClient(LPVOID arg)
{
    Client_Info* clientInfo = (Client_Info*)arg;

    // clientInfo가 잘못된 값이면 스레드를 종료
    if (clientInfo == nullptr || clientInfo->player_N == 0)
    {
        delete clientInfo;
        return 1;
    }

    int addrlen;
    char addr[INET_ADDRSTRLEN];
    struct sockaddr_in clientaddr;
    SOCKET client_sock = clientInfo->socket;

    // 클라이언트 정보 얻기
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
        std::cout << "Client_N 에서 오류 발생" << std::endl;

    server_program.Add_Client_Socket(client_sock, Client_N);
    
    std::cout << Client_N << "P 클라이언트 연결됨: IP 주소=" << addr << ", 포트 번호=" << ntohs(clientaddr.sin_port) << "\r\n";


    Key_Info keyInfo;
    while (true)
    {
        // Key_Info 단위로 데이터 받기
        int retval = recv(client_sock, (char*)&keyInfo, sizeof(Key_Info), 0);
        if (retval == SOCKET_ERROR)
        {
            int error = WSAGetLastError();
            std::cerr << "recv() error: " << error << std::endl;
            break;
        }
        else if (retval == 0)
        {
            // 클라이언트가 연결 종료
            std::cout << Client_N << "P Disconnected\n";
            break;
        }
        else if (retval > 0)
        {
            // 전달받은 Key_Info 정보 출력
            std::cout << "Player: " << Client_N 
                << ", Received KeyCode: " << keyInfo.key_name 
                << ", ActionType: " << (keyInfo.key_action == 1 ? "Down" : (keyInfo.key_action == 2 ? "Up" : "Unknown")) 
                << "\r\n";

                // 키 업데이트 호출
                server_program.EnqueueKeyInput(Client_N, keyInfo);
        }
    }

    // 소켓 닫기 및 클라이언트 연결 해제
    closesocket(client_sock);
    std::cout << Client_N << "P Disconnected\n";
    std::cout << "클라이언트 종료: IP 주소=" << addr << ", 포트 번호=" << ntohs(clientaddr.sin_port) << "\r\n";

    server_program.Remove_Player(Client_N);
    server_program.Remove_Client_Socket(Client_N);

    // 동적 할당된 메모리 해제
    delete clientInfo;
    return 0;
}
