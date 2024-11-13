#pragma once
#include "Object.h"

#define Ground_Y 120


class Server
{
private:
	std::queue<std::pair<int, Key_Info>> keyQueue;
	CRITICAL_SECTION cs_key_queue; // 키 입력 저장 큐에 대한 임계 영역

	std::array<Attack*, MAX_ATTACKS> Stage_Attack_Object_List; 

	SOCKET client1_socket = INVALID_SOCKET;
    SOCKET client2_socket = INVALID_SOCKET;

	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

public:
	Server() { InitializeCriticalSection(&cs_key_queue); }
	~Server() { DeleteCriticalSection(&cs_key_queue); }

	void EnqueueKeyInput(int client_n, const Key_Info& keyInfo);
	bool DequeueKeyInput(std::pair<int, Key_Info>& keyInfo);

	bool Add_Client_Socket(SOCKET clientSocket, int playerNum);
	void Remove_Client_Socket(int playerNum);

	void Decoding(std::pair<int, Key_Info>* key_info);
	Game_Data* Encoding();

	void Update_Server();
	void Update_Collision() {};
	void Broadcast_GameData_All(Game_Data* data);

	void Add_P1(Object* p_ptr, int n) {
		p1_ptr = static_cast<Player*>(p_ptr);
		p1_ptr->Set_Character(n);
	}
	void Add_P2(Object* p_ptr, int n) { 
		p2_ptr = static_cast<Player*>(p_ptr);
		p2_ptr->Set_Character(n);
	}

	Player* Get_Player(int Client);
	void Remove_Player(int Client);


};

