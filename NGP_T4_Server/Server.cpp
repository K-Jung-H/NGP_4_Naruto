#pragma once
#include "stdafx.h"
#include "Server.h"

void Server::EnqueueKeyInput(const Key_Info& keyInfo)
{
	EnterCriticalSection(&cs_key_queue);
	keyQueue.push(keyInfo);  // 큐에 키 입력 추가
	LeaveCriticalSection(&cs_key_queue);
}

// 키 입력 처리 함수 (큐에서 꺼내기)
bool Server::DequeueKeyInput(Key_Info& keyInfo)
{
	EnterCriticalSection(&cs_key_queue);
	if (!keyQueue.empty()) {
		keyInfo = keyQueue.front();  // 큐의 첫 번째 항목을 가져옴
		keyQueue.pop();  // 항목 제거
		LeaveCriticalSection(&cs_key_queue);
		return true;
	}
	LeaveCriticalSection(&cs_key_queue);
	return false;
}

bool Server::Add_Client_Socket(SOCKET clientSocket, int playerNum) 
{
	if (playerNum == 1 && client1_socket == INVALID_SOCKET) 
	{
		client1_socket = clientSocket;
		return true;
	}
	else if (playerNum == 2 && client2_socket == INVALID_SOCKET)
	{
		client2_socket = clientSocket;
		return true;
	}

	return false; 
}


void Server::Remove_Client_Socket(int playerNum) 
{
	if (playerNum == 1)
	{
		closesocket(client1_socket);
		client1_socket = INVALID_SOCKET;
	}
	else if (playerNum == 2) 
	{
		closesocket(client2_socket);
		client2_socket = INVALID_SOCKET;
	}
}

void Server::Update_Server()
{
	if (p1_ptr)
	{
		std::cout << "1P - ";
		p1_ptr->update();
	}
	if (p2_ptr)
	{
		std::cout << "2P - ";
		p2_ptr->update();
	}
	for (Object* obj_ptr : Stage_Attack_Object_List)
	{
		if(obj_ptr != NULL)
			obj_ptr->update();
	}
	    //오브젝트 전부 다 업데이트
		// 플레이어는 서버에 저장된 키 상태 기반 업데이트
		// 공격 정보는 그냥 업데이트	
}



void Server::Decoding(int client_n, Key_Info* key_info)
{
	if (key_info->key_action == 0)
		return;

	int key = EVENT_NONE;
	switch (key_info->key_name)
	{
	case 'a':
	case 'A':
		if(key_info->key_action == 1)
			key = EVENT_MOVE_LEFT_KEY_DOWN;
		else
			key = EVENT_MOVE_LEFT_KEY_UP;
		break;

	default:
		break;
	}

	if (client_n == 1 && p1_ptr != NULL)
		p1_ptr->key_update(key);
	else if (client_n == 2 && p2_ptr != NULL)
		p2_ptr->key_update(key);

	//	Key_Info 기반 플레이어들의 키 상태 업데이트

}


Game_Data* Server::Encoding()
{
	// Game_Data 객체를 동적으로 할당
	Game_Data* sending_data = new Game_Data;

	// 플레이어 정보를 Game_Data에 저장
	for (int i = 0; i < MAX_PLAYERS; ++i)
	{
		Player_Info temp_info;
		Player* temp_player = Get_Player(i + 1);

		if (temp_player != NULL)
		{
			temp_info.pos = temp_player->pos;
			temp_info.X_Direction = temp_player->X_Direction;

			std::memcpy(temp_info.player_ID, temp_player->player_ID, sizeof(temp_info.player_ID));
			temp_info.selected_character = temp_player->selected_character_type;
			temp_info.player_state = temp_player->state;
			temp_info.sprite_index = temp_player->sprite_index;
		}
		sending_data->players[i] = temp_info;
	}

	// 공격 정보를 Game_Data에 저장
	for (int i = 0; i < MAX_ATTACKS; ++i)
	{
		Attack_Info temp_info;
		Attack* temp_attack = Stage_Attack_Object_List[i];

		if (temp_attack != NULL)
		{
			temp_info.pos = temp_attack->pos;
			temp_info.X_Direction = temp_attack->X_Direction;

			std::memcpy(temp_info.player_ID, temp_attack->player_ID, sizeof(temp_info.player_ID));
			temp_info.attack_type = temp_attack->attack_type;
			temp_info.sprite_index = temp_attack->sprite_index;
		}
		sending_data->attacks[i] = temp_info;
	}

	// 그 외 정보들을 Game_Data에 저장
	ETC_Info etc_info;
	{
		Player* p1_ptr = Get_Player(1);
		Player* p2_ptr = Get_Player(2);

		etc_info.game_time = 0;
		if (p1_ptr != NULL)
		{
			etc_info.player1_hp = p1_ptr->hp;
			etc_info.player1_sp = p1_ptr->sp;
		}

		if (p2_ptr != NULL)
		{
			etc_info.player2_hp = p2_ptr->hp;
			etc_info.player2_sp = p2_ptr->sp;
		}
	}
	sending_data->etc = etc_info;

	// 동적으로 할당된 포인터 반환
	return sending_data;  
}

void Server::Broadcast_GameData_All(Game_Data* data)
{
	if (client1_socket != INVALID_SOCKET)
	{
		send(client1_socket, (char*)data, sizeof(Game_Data), 0);
		std::cout << "1P - send()" << std::endl;
	}
	if (client2_socket != INVALID_SOCKET)
	{
		send(client2_socket, (char*)data, sizeof(Game_Data), 0);
		std::cout << "2P - send()" << std::endl;
	}

	delete data;
}

Player* Server::Get_Player(int Client)
{
	if (Client == 1)
		return p1_ptr;
	else if (Client == 2)
		return p2_ptr;
	else
		return NULL;
}

void Server::Remove_Player(int Client)
{
	if (Client == 0)
		return;
	else if (Client == 1)
	{
		delete p1_ptr;
		p1_ptr = NULL;
	}
	else if (Client == 2)
	{
		delete p2_ptr;
		p2_ptr = NULL;
	}
}