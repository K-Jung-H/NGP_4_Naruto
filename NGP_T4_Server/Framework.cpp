#pragma once
#include "stdafx.h"
#include "Server.h"
#include "Object.h"
#include <windows.h>

#define SERVERPORT 9000
#define BUFSIZE    512

// 윈도우 프로시저
LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);
// 에디트 컨트롤 출력 함수
void DisplayText(const char* fmt, ...);
// 소켓 함수 오류 출력
void DisplayError(const char* msg);
// 소켓 통신 스레드 함수
DWORD WINAPI ServerMain(LPVOID arg);
DWORD WINAPI ProcessClient(LPVOID arg);


HINSTANCE hInst; // 인스턴스 핸들
HWND hEdit; // 에디트 컨트롤

CRITICAL_SECTION cs_message_output; // 출력 부분 임계 영역
CRITICAL_SECTION cs_server_program; // 서버 임계 영역

Server server_program;


int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	// 콘솔 창 할당
	AllocConsole();
	freopen("CONOUT$", "w", stdout);

	InitializeCriticalSection(&cs_message_output);
	InitializeCriticalSection(&cs_server_program);

	// 윈도우 클래스 등록
	WNDCLASS wndclass;
	wndclass.style = CS_HREDRAW | CS_VREDRAW;
	wndclass.lpfnWndProc = WndProc;
	wndclass.cbClsExtra = 0;
	wndclass.cbWndExtra = 0;
	wndclass.hInstance = hInstance;
	wndclass.hIcon = LoadIcon(NULL, IDI_APPLICATION);
	wndclass.hCursor = LoadCursor(NULL, IDC_ARROW);
	wndclass.hbrBackground = (HBRUSH)GetStockObject(WHITE_BRUSH);
	wndclass.lpszMenuName = NULL;
	wndclass.lpszClassName = _T("MyWndClass");
	if (!RegisterClass(&wndclass)) return 1;

	// 윈도우 생성
	HWND hWnd = CreateWindow(_T("MyWndClass"), _T("Simple Window"),
		WS_OVERLAPPEDWINDOW, 0, 0, 500, 220, NULL, NULL, hInstance, NULL);
	if (hWnd == NULL) return 1;
	ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);

	// 소켓 통신 스레드 생성
	CreateThread(NULL, 0, ServerMain, NULL, 0, NULL);

	// 메시지 루프
	MSG msg;
	while (true) {
		// 메시지가 있는 경우 처리
		if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
			if (msg.message == WM_QUIT) break;
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
	}
	return (int)msg.wParam;
}

// 윈도우 프로시저
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	switch (uMsg) {
	case WM_CREATE:
		hEdit = CreateWindow(_T("edit"), NULL,
			WS_CHILD | WS_VISIBLE | WS_HSCROLL |
			WS_VSCROLL | ES_AUTOHSCROLL |
			ES_AUTOVSCROLL | ES_MULTILINE | ES_READONLY,
			0, 0, 0, 0, hWnd, (HMENU)100, hInst, NULL);
		return 0;
	case WM_SIZE:
		MoveWindow(hEdit, 0, 0, LOWORD(lParam), HIWORD(lParam), TRUE);
		return 0;
	case WM_SETFOCUS:
		SetFocus(hEdit);
		return 0;
	case WM_DESTROY:
		PostQuitMessage(0);
		return 0;
	}
	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}

// TCP 서버 쓰레드
DWORD WINAPI ServerMain(LPVOID arg)
{
	int retval;

	// 윈속 초기화
	WSADATA wsa;
	if (WSAStartup(MAKEWORD(2, 2), &wsa) != 0)
		return 1;

	// 소켓 생성
	SOCKET listen_sock = socket(AF_INET, SOCK_STREAM, 0);
	if (listen_sock == INVALID_SOCKET) err_quit("socket()");

	// bind()
	struct sockaddr_in serveraddr;
	memset(&serveraddr, 0, sizeof(serveraddr));
	serveraddr.sin_family = AF_INET;
	serveraddr.sin_addr.s_addr = htonl(INADDR_ANY);
	serveraddr.sin_port = htons(SERVERPORT);
	retval = bind(listen_sock, (struct sockaddr*)&serveraddr, sizeof(serveraddr));
	if (retval == SOCKET_ERROR) err_quit("bind()");

	// listen()
	retval = listen(listen_sock, SOMAXCONN);
	if (retval == SOCKET_ERROR) err_quit("listen()");

	// 데이터 통신에 사용할 변수
	SOCKET client_sock;
	struct sockaddr_in clientaddr;
	int addrlen;
	HANDLE hThread;

	while (1)
	{
		// accept()
		addrlen = sizeof(clientaddr);
		client_sock = accept(listen_sock, (struct sockaddr*)&clientaddr, &addrlen);
		if (client_sock == INVALID_SOCKET)
		{
			DisplayError("accept()");
			break;
		}


		// 스레드 생성
		Client_Info* client_info = new Client_Info;
		client_info->socket = client_sock;
		client_info->player_N = 0;


		// 서버에 연결될 플레이어 2명으로 제한 // 서버에서는 player_N 1 or 2만 처리함
		if (server_program.Get_Player(1) == NULL)
			client_info->player_N = 1;
		else if (server_program.Get_Player(2) == NULL)
			client_info->player_N = 2;


		hThread = CreateThread(NULL, 0, ProcessClient, (LPVOID)client_info, 0, NULL);
		
		if (hThread == NULL)
			closesocket(client_sock);
		else
			CloseHandle(hThread);

		// 서버 업데이트
		EnterCriticalSection(&cs_server_program);

		server_program.Update_Server();
		server_program.Update_Collision();
		Game_Data* sending_data = server_program.Encoding();

		LeaveCriticalSection(&cs_server_program);
	}

	// 소켓 닫기
	closesocket(listen_sock);

	// 윈속 종료
	WSACleanup();
	return 0;
}

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
	Key_Info keyInfo;

	// 클라이언트 정보 얻기
	addrlen = sizeof(clientaddr);
	getpeername(client_sock, (struct sockaddr*)&clientaddr, &addrlen);
	inet_ntop(AF_INET, &clientaddr.sin_addr, addr, sizeof(addr));

	int Client_N = clientInfo->player_N;
	DisplayText("%dP 클라이언트 연결됨: IP 주소=%s, 포트 번호=%d\r\n", Client_N, addr, ntohs(clientaddr.sin_port));

	Object* player = new Player();

	EnterCriticalSection(&cs_server_program);

	if (Client_N == 1)
		server_program.Add_P1(player);
	else if (Client_N == 2)
		server_program.Add_P2(player);

	server_program.Add_Client_Socket(client_sock, Client_N);

	LeaveCriticalSection(&cs_server_program);

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
			DisplayText("%dP Disconnected\n", Client_N);
			break;
		}
		else if (retval > 0)
		{
			// 전달받은 Key_Info 정보 출력
			DisplayText("Player: %d, Received KeyCode: %c, ActionType: %s\r\n", Client_N,
				keyInfo.key_name,
				keyInfo.key_action == 1 ? "Down" : (keyInfo.key_action == 2 ? "Up" : "Unknown"));

			// 키 업데이트 호출
			EnterCriticalSection(&cs_server_program);
			server_program.Decoding(Client_N, &keyInfo);
			LeaveCriticalSection(&cs_server_program);
		}
	}

	// 소켓 닫기 및 클라이언트 연결 해제
	closesocket(client_sock);
	DisplayText("%dP Disconnected\n", Client_N);
	DisplayText("클라이언트 종료: IP 주소=%s, 포트 번호=%d\r\n", addr, ntohs(clientaddr.sin_port));

	EnterCriticalSection(&cs_server_program);

	server_program.Remove_Player(Client_N);
	server_program.Remove_Client_Socket(Client_N);

	LeaveCriticalSection(&cs_server_program);

	// 동적 할당된 메모리 해제
	delete clientInfo;
	return 0;
}




// 에디트 컨트롤 출력 함수
void DisplayText(const char* fmt, ...)
{
	va_list arg;
	va_start(arg, fmt);
	char cbuf[BUFSIZE * 2];
	vsprintf(cbuf, fmt, arg);
	va_end(arg);

	EnterCriticalSection(&cs_message_output);
	int nLength = GetWindowTextLength(hEdit);
	SendMessage(hEdit, EM_SETSEL, nLength, nLength);
	SendMessageA(hEdit, EM_REPLACESEL, FALSE, (LPARAM)cbuf);
	LeaveCriticalSection(&cs_message_output);
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
