#pragma once
#include "Object.h"

#define Ground_Y 120

extern std::vector<Object*> Public_Object_List;

class Server
{
public:
	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

	std::vector<Object*> Stage_Object_List; // 스킬 객체만 넣을 것

	void Decoding(int client_n, Key_Info* key_info);
	void Update_Server();
	void Add_P1(Object* p_ptr) { p1_ptr = static_cast<Player*>(p_ptr); }
	void Delete_Player(int Client);
	void Add_P2(Object* p_ptr) { p2_ptr = static_cast<Player*>(p_ptr); }
};

