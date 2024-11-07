#pragma once
#define _CRT_SECURE_NO_WARNINGS // ���� C �Լ� ��� �� ��� ����
#define _WINSOCK_DEPRECATED_NO_WARNINGS // ���� ���� API ��� �� ��� ����

#include <winsock2.h> // ����2 ���� ���
#include <ws2tcpip.h> // ����2 Ȯ�� ���

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
#pragma comment(lib, "ws2_32") // ws2_32.lib ��ũ


// ������ �����ؾ� �ϴ� ����ü
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
 
struct Position
{
	float x;
	float y;
	Position() : x(0), y(0) {}
};

struct Player_Info
{
	std::string player_ID = "";
	Position pos;
	bool X_Direction = false; // Left: false, Right: true
	int player_state = 0;
	int selected_character = 0;
	int sprite_index = 0;

	Player_Info() : player_ID("Unknown"), pos(), X_Direction(false), player_state(0), selected_character(0), sprite_index(0) {}
};


struct Attack_Info
{
	std::string player_ID;	// ���� ������ �ĺ�
	Position  pos;
	bool X_Direction;		// Left: false, Right: true
	int attack_type;			// ��ų 1, ��ų 2, ����ü, �⺻ ����
	int sprite_index;

	Attack_Info() : player_ID("Unknown"), pos(), X_Direction(false), attack_type(0), sprite_index(0) {}
};

struct ETC_Info
{
	int player1_hp; // ü��
	int player1_sp; // ��ũ��

	int player2_hp; // ü��
	int player2_sp; // ��ũ��

	int game_time;

	ETC_Info() : player1_hp(0), player1_sp(0), player2_hp(0), player2_sp(0), game_time(0) {}

};

struct Game_Data {
	std::array<Player_Info, MAX_PLAYERS> players;
	std::array<Attack_Info, MAX_ATTACKS> attacks;
	ETC_Info etc;
};


struct Key_Info
{
//	int client_info;			// Ŭ���̾�Ʈ �ĺ�
	int key_name;			// Ű ����
	int key_action;			// Ű ���� 
};

struct Client_Info
{
	SOCKET socket;
	int player_N;
};

// ���� �Լ� ���� ��� �� ����
void err_quit(const char* msg);

// ���� �Լ� ���� ���
void err_display(const char* msg);
// ���� �Լ� ���� ���
void err_display(int errcode);