#pragma once
#define _CRT_SECURE_NO_WARNINGS // 구형 C 함수 사용 시 경고 끄기
#define _WINSOCK_DEPRECATED_NO_WARNINGS // 구형 소켓 API 사용 시 경고 끄기

#include <winsock2.h> // 윈속2 메인 헤더
#include <ws2tcpip.h> // 윈속2 확장 헤더

#include <windows.h>
#include <tchar.h> // _T(), ...
#include <stdio.h> // printf(), ...
#include <stdlib.h> // exit(), ...
#include <string.h> // strncpy(), ...

#include <string>
#include <vector>
#include <iostream>
#pragma comment(lib, "ws2_32") // ws2_32.lib 링크


// 형식을 통일해야 하는 구조체
//=========================================================================

struct Position
{

	float x;
	float y;
};

struct Player_Info
{
	std::string player_ID;
	Position pos;
	bool X_Direction; // Left: false, Right: true
	int player_state;
	int selected_character;
	int sprite_index;
};


struct Attack_Info
{
	std::string player_ID;	// 공격 시전자 식별
	Position  pos;
	bool X_Direction;		// Left: false, Right: true
	int attack_type;			// 스킬 1, 스킬 2, 투사체, 기본 공격
	int sprite_index;
};

struct ETC_Info
{
	int player1_hp; // 체력
	int player1_sp; // 차크라

	int player2_hp; // 체력
	int player2_sp; // 차크라

	int game_time;
};

struct Key_Info
{
	int client_info;			// 클라이언트 식별
	DWORD key_status;	// 상태 = 토글 0x00
};