#pragma once
constexpr int PORT_NUM = 9000;
constexpr int MAX_CLIENTS = 10;
constexpr int MAX_BUFFER_SIZE = 1024;
constexpr int NAME_SIZE = 20;

//용어 정의
//CS : Client to Server
//SC : Server to Client


// Packet types
constexpr char CS_LOGIN = 0;
constexpr char CS_MOVE = 1;
constexpr char CS_ATTACK = 2;
constexpr char CS_LOGOUT = 3;

struct CS_LOGIN_PACKET
{
	unsigned short size; // 패킷의 크기
	char type;
	char name[NAME_SIZE];
};

struct CS_MOVE_PACKET 
{
	unsigned short size; // 패킷의 크기
	char type;
	char direction;  // 0 : UP, 1 : DOWN, 2 : LEFT, 3 : RIGHT
	unsigned move_time;
};

struct CS_LOGOUT_PACKET 
{
	unsigned short size; // 패킷의 크기
	char type;
};

struct CS_LOGIN_INFO_PACKET
{
	unsigned short size; // 패킷의 크기
	char	type;
	int		id;
	int		hp;
	int		max_hp;
	short	x, y;
};

struct SC_MOVE_PACKET
{
	unsigned short size; // 패킷의 크기
	char type;
	char direction;  // 0 : UP, 1 : DOWN, 2 : LEFT, 3 : RIGHT
	unsigned move_time;
};
