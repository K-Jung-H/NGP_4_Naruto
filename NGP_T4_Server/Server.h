#pragma once
#include "Object.h"

#define Ground_Y 120


class Server
{
private:
	std::array<Attack*, MAX_ATTACKS> Stage_Attack_Object_List; 

	SOCKET client1_socket = INVALID_SOCKET;
    SOCKET client2_socket = INVALID_SOCKET;

	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

public:
	bool Add_Client_Socket(SOCKET clientSocket, int playerNum);
	void Remove_Client_Socket(int playerNum);

	void Decoding(int client_n, Key_Info* key_info);
	Game_Data* Encoding();

	void Update_Server();
	void Update_Collision() {};

	void Add_P1(Object* p_ptr) { p1_ptr = static_cast<Player*>(p_ptr); }
	void Add_P2(Object* p_ptr) { p2_ptr = static_cast<Player*>(p_ptr); }

	Player* Get_Player(int Client);
	void Remove_Player(int Client);
};

