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
#include <array>
#include <algorithm>
#include <iostream>
#include <chrono>
#include <thread>
#include <queue>


#pragma comment(lib, "ws2_32") // ws2_32.lib 링크


// 형식을 통일해야 하는 구조체
//=========================================================================
#define EVENT_NONE 0
#define EVENT_MOVE_LEFT_KEY_DOWN   1
#define EVENT_MOVE_LEFT_KEY_UP  2

#define EVENT_MOVE_RIGHT_KEY_DOWN  3
#define EVENT_MOVE_RIGHT_KEY_UP  4

#define EVENT_MOVE_UP_KEY_DOWN    5
#define EVENT_MOVE_UP_KEY_UP    6

#define EVENT_MOVE_DOWN_KEY_DOWN   7
#define EVENT_MOVE_DOWN_KEY_UP   8

#define EVENT_NORMAL_ATTACK_KEY_DOWN 9
#define EVENT_NORMAL_ATTACK_KEY_UP 10

#define EVENT_RANGED_ATTACK_KEY_DOWN 11
#define EVENT_RANGED_ATTACK_KEY_UP 12

#define EVENT_SKILL_ATTACK_1_KEY_DOWN 13
#define EVENT_SKILL_ATTACK_1_KEY_UP 14

#define EVENT_SKILL_ATTACK_2_KEY_DOWN 15
#define EVENT_SKILL_ATTACK_2_KEY_UP 16

#define LEFT false
#define RIGHT true

#define MAX_PLAYERS 2
#define MAX_ATTACKS 18
#define OBJECT_MAX_LEN (MAX_PLAYERS + MAX_ATTACKS)

#define MAX_INPUT_PER_FRAME 10

#define CHARACTER_NARUTO 1
#define CHARACTER_SASUKE 2
#define CHARACTER_ITACHI 3

#define STATE_IDLE 0
#define STATE_RUN 1
#define STATE_JUMP 2
#define STATE_ATTACK_NORMAL_1 3
#define STATE_ATTACK_NORMAL_2 4
#define STATE_ATTACK_NORMAL_3 5
#define STATE_ATTACK_NORMAL_4 6
#define STATE_ATTACK_SKILL_1 7
#define STATE_ATTACK_SKILL_2 8
#define STATE_ATTACK_SKILL_3 9
#define STATE_HIT_EASY 10
#define STATE_HIT_HARD 11
#define STATE_WIN 12
#define STATE_LOSE 13


#define Ground_Y 120
#define Player_Attack_Combo_Time_Limit 1.0f

static float PIXEL_PER_METER = (10.0 / 0.3); // 10 pixel 30 cm
static float  RUN_SPEED_KMPH = 50.0f; // Km / Hour
static float RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0);
static float RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0);
static float RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER);

struct Position
{
	float x;
	float y;
	Position() : x(0), y(0) {}
};

struct Player_Info
{
	char player_ID[32];
	Position pos;
	bool X_Direction = false; // Left: false, Right: true
	int player_state = 0;
	int selected_character = 0;
	int sprite_index = 0;

	Player_Info() : player_ID("Unknown_Player"), pos(), X_Direction(false), player_state(0), selected_character(0), sprite_index(0) {}
};


struct Attack_Info
{

	Position  pos;
	bool X_Direction;		// Left: false, Right: true
	
	// 10의 자리: 1. 나루토, 2. 사스케, 3. 이타치
	// 1의 자리: 1. 투사체, 2. 스킬_1 , 2. 스킬_2

	int attack_type;			
	int sprite_index;

	Attack_Info() : pos(), X_Direction(false), attack_type(0), sprite_index(0) {}
};

struct ETC_Info
{
	int player1_hp; // 체력
	int player1_sp; // 차크라

	int player2_hp; // 체력
	int player2_sp; // 차크라

	int game_time;

	ETC_Info() : player1_hp(0), player1_sp(0), player2_hp(0), player2_sp(0), game_time(0) {}

};

struct Game_Data
{
	Player_Info players[MAX_PLAYERS];
	Attack_Info attacks[MAX_ATTACKS];
	ETC_Info etc;
};

struct Key_Info
{
//	int client_info;			// 클라이언트 식별
	int key_name;			// 키 정보
	int key_action;			// 키 상태  down : 1, up : 2
};

struct Client_Info
{
	SOCKET socket;
	int player_N;
};

// 소켓 함수 오류 출력 후 종료
void err_quit(const char* msg);

// 소켓 함수 오류 출력
void err_display(const char* msg);
// 소켓 함수 오류 출력
void err_display(int errcode);