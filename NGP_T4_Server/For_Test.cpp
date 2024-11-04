#pragma once
#include "stdafx.h"
#include "Server.h"
#include "Object.h"
#include <windows.h>

Server server_test;

LRESULT CALLBACK WndProc(HWND, UINT, WPARAM, LPARAM);

int WINAPI WinMain(HINSTANCE hInstance, HINSTANCE hPrevInstance, LPSTR lpCmdLine, int nCmdShow)
{
	// �ܼ� â �Ҵ�
	AllocConsole();
	freopen("CONOUT$", "w", stdout);

	// ������ Ŭ���� ���
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

	// ������ ����
	HWND hWnd = CreateWindow(_T("MyWndClass"), _T("Simple Window"),
		WS_OVERLAPPEDWINDOW, 0, 0, 500, 220, NULL, NULL, hInstance, NULL);
	if (hWnd == NULL) return 1;
	ShowWindow(hWnd, nCmdShow);
	UpdateWindow(hWnd);

	Object* p1 = new Player();
	
	server_test.Add_P1(p1);

	// �޽��� ����
	MSG msg;
	while (true) {
		// �޽����� �ִ� ��� ó��
		if (PeekMessage(&msg, NULL, 0, 0, PM_REMOVE)) {
			if (msg.message == WM_QUIT) break;
			TranslateMessage(&msg);
			DispatchMessage(&msg);
		}
		else {
			// �޽����� ���� ���� �ݺ������� ȣ��
			server_test.Update_Server();
		}
	}
	return (int)msg.wParam;
}

// ������ ���ν���
LRESULT CALLBACK WndProc(HWND hWnd, UINT uMsg, WPARAM wParam, LPARAM lParam)
{
	switch (uMsg) {
	case WM_CREATE:
		return 0;
	case WM_SIZE:
		return 0;
	case WM_KEYDOWN: 
		switch (wParam)
		{
		case VK_LEFT: 
		case VK_RIGHT: 
		case VK_UP: 
		case VK_DOWN: 
			server_test.p1_ptr->key_update();
			break;
		default:
			break;
		}
		return 0;
	case WM_KEYUP: 
		switch (wParam) {
		case VK_LEFT:

			break;
		case VK_RIGHT:
			break;
		case VK_UP:
			break;
		case VK_DOWN:
			break;

		default:
			break;
		}
		return 0;
	case WM_DESTROY:
		PostQuitMessage(0);
		return 0;
	}
	return DefWindowProc(hWnd, uMsg, wParam, lParam);
}