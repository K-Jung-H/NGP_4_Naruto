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
    int key_name;			// 키 정보
    int key_action;			// 키 상태 
};


// 대화상자 프로시저
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
// 에디트 컨트롤 출력 함수
void DisplayText(const char* fmt, ...);
// 소켓 함수 오류 출력
void DisplayError(const char* msg);
// 소켓 통신 스레드 함수
DWORD WINAPI ClientMain(LPVOID arg);

SOCKET sock; // 소켓
char buf[BUFSIZE + 1]; // 데이터 송수신 버퍼
HWND hEdit; // 에디트 컨트롤

// 키 정보를 전송하기 위한 함수
void SendKeyInfo(int key_name, int key_action) 
{
    Key_Info keyInfo;
    keyInfo.key_name = key_name;
    keyInfo.key_action = key_action;

    // 구조체를 문자열로 변환하여 전송
    int retval = send(sock, (char*)&keyInfo, sizeof(Key_Info), 0);
    if (retval == SOCKET_ERROR) {
        DisplayError("send()");
    }
}

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance,
    LPSTR lpCmdLine, int nCmdShow)
{
    // 윈속 초기화
    WSADATA wsa;
    if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
        return 1;

    // 윈도우 클래스 등록
    WNDCLASS wc = { 0 };
    wc.lpfnWndProc = WndProc;
    wc.hInstance = hInstance;
    wc.lpszClassName = _T("SimpleClient");
    RegisterClass(&wc);

    // 윈도우 생성
    HWND hwnd = CreateWindow(_T("SimpleClient"), _T("TCP 클라이언트"),
        WS_OVERLAPPEDWINDOW | WS_VISIBLE,
        CW_USEDEFAULT, CW_USEDEFAULT, 400, 300,
        NULL, NULL, hInstance, NULL);

    // 소켓 통신 스레드 생성
    CreateThread(NULL, 0, ClientMain, NULL, 0, NULL);

    // 메시지 루프
    MSG msg;
    while (GetMessage(&msg, NULL, 0, 0)) {
        TranslateMessage(&msg);
        DispatchMessage(&msg);
    }

    // 윈속 종료
    WSACleanup();
    return 0;
}
// 대화상자 프로시저
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
    static bool bKeyDown = false; // 키가 눌렸는지 확인하는 변수

    switch (uMsg) {
    case WM_CREATE:
        hEdit = CreateWindow(_T("EDIT"), _T(""),
            WS_CHILD | WS_VISIBLE | WS_VSCROLL | ES_MULTILINE | ES_AUTOVSCROLL | ES_READONLY,
            0, 0, 400, 300, hWnd, NULL, ((LPCREATESTRUCT)lParam)->hInstance, NULL);
        return 0;

    case WM_KEYDOWN: // 키가 눌렸을 때
    {
        UINT ascii = MapVirtualKey(wParam, MAPVK_VK_TO_CHAR);
        SendKeyInfo(ascii, 1); // 1은 키 눌림 상태
        bKeyDown = true; // 키가 눌렸음을 기록
    }
    break;

    case WM_KEYUP: // 키에서 손을 뗐을 때
    {
        UINT ascii = MapVirtualKey(wParam, MAPVK_VK_TO_CHAR);
        SendKeyInfo(ascii, 2); // 2는 키 떼어짐 상태
        bKeyDown = false; // 키가 떼어졌음을 기록
    }
    break;

    case WM_DESTROY:
        PostQuitMessage(0);
        return 0;
    }
    return DefWindowProc(hWnd, uMsg, wParam, lParam);
}


// 에디트 컨트롤 출력 함수
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

// 소켓 함수 오류 출력
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

// TCP 클라이언트 시작 부분
DWORD WINAPI ClientMain(LPVOID arg)
{
    int retval;

    // 소켓 생성
    sock = socket(AF_INET, SOCK_STREAM, 0);
    if (sock == INVALID_SOCKET) {
        DisplayError("socket()");
        return 1; // 오류 발생 시 종료
    }

    // connect()
    struct sockaddr_in serveraddr;
    memset(&serveraddr, 0, sizeof(serveraddr));
    serveraddr.sin_family = AF_INET;
    serveraddr.sin_addr.s_addr = inet_addr(SERVERIP);
    serveraddr.sin_port = htons(SERVERPORT);
    retval = connect(sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr));
    if (retval == SOCKET_ERROR) {
        DisplayError("connect()"); // 연결 실패 시 오류 메시지 출력
        closesocket(sock); // 소켓 닫기
        DisplayText("서버에 연결할 수 없습니다.\r\n"); // 사용자에게 연결 실패 알림
        return 1; // 오류 발생 시 종료
    }

    DisplayText("[TCP 클라이언트] 서버에 연결되었습니다.\r\n");

    // 서버와 데이터 통신
    while (1) {
        // 데이터 받기
        retval = recv(sock, buf, BUFSIZE, 0);
        if (retval == SOCKET_ERROR) {
            DisplayError("recv()");
            break;
        }
        else if (retval == 0) // 서버가 연결을 끊은 경우
            break;

        // 받은 데이터 출력
        buf[retval] = '\0';
        DisplayText("[받은 데이터] %s\r\n", buf);
    }

    // 소켓 종료
    closesocket(sock);
    return 0;
}
