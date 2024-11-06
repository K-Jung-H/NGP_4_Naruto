#include "Common.h"
#include "resource.h"
#include <winsock2.h>
#include <ws2tcpip.h>
#include <tchar.h>
#include <stdio.h>
#include <stdarg.h>
#include <windows.h>

#define SERVERIP   "192.168.81.193"
#define SERVERPORT 9000
#define BUFSIZE    512

struct Key_Info
{
    int key_name;			// Ű ����
    int key_action;			// Ű ���� 
};


// ��ȭ���� ���ν���
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
// ����Ʈ ��Ʈ�� ��� �Լ�
void DisplayText(const char* fmt, ...);
// ���� �Լ� ���� ���
void DisplayError(const char* msg);
// ���� ��� ������ �Լ�
DWORD WINAPI ClientMain(LPVOID arg);

SOCKET sock; // ����
char buf[BUFSIZE + 1]; // ������ �ۼ��� ����
HWND hEdit; // ����Ʈ ��Ʈ��

// Ű ������ �����ϱ� ���� �Լ�
void SendKeyInfo(int key_name, int key_action) 
{
    Key_Info keyInfo;
    keyInfo.key_name = key_name;
    keyInfo.key_action = key_action;

    // ����ü�� ���ڿ��� ��ȯ�Ͽ� ����
    int retval = send(sock, (char*)&keyInfo, sizeof(Key_Info), 0);
    if (retval == SOCKET_ERROR) {
        DisplayError("send()");
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    // ���� �ʱ�ȭ
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return 1;

    // ������ Ŭ���� ���
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = _T("SimpleClient");
    RegisterClass(&wc);

    // ������ ����
    HWND hwnd = CreateWindow(_T("SimpleClient"), _T("TCP Ŭ���̾�Ʈ"),
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 400, 300,
        NULL, NULL, hInstance, NULL);

    // ���� ��� ������ ����
    CreateThread(NULL, 0, ClientMain, NULL, 0, NULL);

    // �޽��� ����
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // ���� ����
    WSACleanup();
    return 0;
}
// ��ȭ���� ���ν���
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static bool bKeyDown = false; // Ű�� ���ȴ��� Ȯ���ϴ� ����

    switch (uMsg) {
    case WM_CREATE:
        hEdit = CreateWindow(_T("EDIT"), _T(""),
            WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL | ES_READONLY,
            0, 0, 400, 300, hWnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
        return 0;

    case WM_KEYDOWN: // Ű�� ������ ��
    {
        UINT ascii = MapVirtualKey(wParam, MAPVK_VK_TO_CHAR);
        SendKeyInfo(ascii, 1); // 1�� Ű ���� ����
        bKeyDown = true; // Ű�� �������� ���
    }
    break;

    case WM_KEYUP: // Ű���� ���� ���� ��
    {
        UINT ascii = MapVirtualKey(wParam, MAPVK_VK_TO_CHAR);
        SendKeyInfo(ascii, 2); // 2�� Ű ������ ����
        bKeyDown = false; // Ű�� ���������� ���
    }
    break;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hWnd, uMsg, wParam, lParam);
}


// ����Ʈ ��Ʈ�� ��� �Լ�
void DisplayText(const char* fmt, ...)
{
    va_list arg;
    va_start(arg, fmt);
    char cbuf[BUFSIZE * 2];
    vsprintf(cbuf, fmt, arg);
    va_end(arg);

    int nLength = GetWindowTextLength(hEdit);
    SendMessage(hEdit, EM_SETSEL, nLength, nLength);
    SendMessageA(hEdit, EM_REPLACESEL, FALSE, (LPARAM)cbuf);
}

// ���� �Լ� ���� ���
void DisplayError(const char* msg)
{
    LPVOID lpMsgBuf;
    FormatMessageA(
        FORMAT_MESSAGE_ALLOCATE_BUFFER | FORMAT_MESSAGE_FROM_SYSTEM,
        NULL, WSAGetLastError(),
        MAKELANGID(LANG_NEUTRAL, SUBLANG_DEFAULT),
        (char*)&lpMsgBuf, 0, NULL);
    DisplayText("[%s] %s\r\n", msg, (char*)lpMsgBuf);
    LocalFree(lpMsgBuf);
}

// TCP Ŭ���̾�Ʈ ���� �κ�
DWORD WINAPI ClientMain(LPVOID arg)
{
    int retval;

    // ���� ����
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        DisplayError("socket()");
        return 1; // ���� �߻� �� ����
    }

    // connect()
    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = inet_addr(SERVERIP);
    serveraddr.sin_port = htons(SERVERPORT);
    retval = connect(sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr));
    if (retval == SOCKET_ERROR) {
        DisplayError("connect()"); // ���� ���� �� ���� �޽��� ���
        closesocket(sock); // ���� �ݱ�
        DisplayText("������ ������ �� �����ϴ�.\r\n"); // ����ڿ��� ���� ���� �˸�
        return 1; // ���� �߻� �� ����
    }

    DisplayText("[TCP Ŭ���̾�Ʈ] ������ ����Ǿ����ϴ�.\r\n");

    // ������ ������ ���
    while (1) {
        // ������ �ޱ�
        retval = recv(sock, buf, BUFSIZE, 0);
        if (retval == SOCKET_ERROR) {
            DisplayError("recv()");
            break;
        }
        else if (retval == 0) // ������ ������ ���� ���
            break;

        // ���� ������ ���
        buf[retval] = '\0';
        DisplayText("[���� ������] %s\r\n", buf);
    }

    // ���� ����
    closesocket(sock);
    return 0;
}
