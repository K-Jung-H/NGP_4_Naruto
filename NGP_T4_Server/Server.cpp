#pragma once
#include "stdafx.h"
#include "Server.h"

void Server::EnqueueKeyInput(int client_n, const Key_Info& keyInfo)
{
	EnterCriticalSection(&cs_key_queue);
	keyQueue.push(std::make_pair(client_n, keyInfo));  // 큐에 키 입력 추가
	LeaveCriticalSection(&cs_key_queue);
}

// 키 입력 처리 함수 (큐에서 꺼내기)
bool Server::DequeueKeyInput(std::pair<int, Key_Info>& keyInfo)
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

void Server::Add_P1(Object* p_ptr, int n) 
{
	p1_ptr = static_cast<Player*>(p_ptr);
	p1_ptr->Set_Character(n, this);
}
void Server::Add_P2(Object* p_ptr, int n) 
{
	p2_ptr = static_cast<Player*>(p_ptr);
	p2_ptr->Set_Character(n, this);
}

void Server::Add_Skill_Object(Object* skill_ptr)
{
	auto empty_space = std::find(Stage_Attack_Object_List.begin(), Stage_Attack_Object_List.end(), static_cast<Attack*>(nullptr));

	if (empty_space != Stage_Attack_Object_List.end()) 
		*empty_space = static_cast<Attack*>(skill_ptr);
	else
		std::cout << "No space for skill_object in game world" << std::endl;
	
}

void Server::Update_Server(float elapsed_time)
{
	// 플레이어 업데이트
	if (p1_ptr) 
		p1_ptr->update(elapsed_time);

	if (p2_ptr) 
		p2_ptr->update(elapsed_time);

	// 공격 객체 업데이트
	for (auto& attack_ptr : Stage_Attack_Object_List)
	{
		if (attack_ptr != nullptr)
		{
			attack_ptr->update(elapsed_time);

			if (attack_ptr->life == false)
			{
				delete attack_ptr;
				attack_ptr = nullptr;
			}
		}
	}

}


void Server::Decoding(std::pair<int, Key_Info>* key_info)
{
	int client_n = key_info->first;
	Key_Info key_value = key_info->second;

	if (key_value.key_action == 0)
		return;

	int key = EVENT_NONE;

	switch (key_value.key_name)
	{
	case 'a':
	case 'A':
		if(key_value.key_action == 1)
			key = EVENT_MOVE_LEFT_KEY_DOWN;
		else
			key = EVENT_MOVE_LEFT_KEY_UP;
		break;

	case 'd':
	case 'D':
		if (key_value.key_action == 1)
			key = EVENT_MOVE_RIGHT_KEY_DOWN;
		else
			key = EVENT_MOVE_RIGHT_KEY_UP;
		break;

	case 'w':
	case 'W':
		if (key_value.key_action == 1)
			key = EVENT_MOVE_UP_KEY_DOWN;
		else
			key = EVENT_MOVE_UP_KEY_UP;
		break;

	case 's':
	case 'S':
		if (key_value.key_action == 1)
			key = EVENT_MOVE_DOWN_KEY_DOWN;
		else
			key = EVENT_MOVE_DOWN_KEY_UP;
		break;

	case ',':
		if (key_value.key_action == 1)
			key = EVENT_NORMAL_ATTACK_KEY_DOWN;
		else
			key = EVENT_NORMAL_ATTACK_KEY_UP;
		break;

	case '/':
		if (key_value.key_action == 1)
			key = EVENT_RANGED_ATTACK_KEY_DOWN;
		else
			key = EVENT_RANGED_ATTACK_KEY_UP;
		break;

	case 'L':
	case 'l':
		if (key_value.key_action == 1)
			key = EVENT_SKILL_ATTACK_1_KEY_DOWN;
		else
			key = EVENT_SKILL_ATTACK_1_KEY_UP;
		break;

	case ';':
		if (key_value.key_action == 1)
			key = EVENT_SKILL_ATTACK_2_KEY_DOWN;
		else
			key = EVENT_SKILL_ATTACK_2_KEY_UP;
		break;

	case '.':
		if (key_value.key_action == 1)
			key = EVENT_SKILL_TELEPORT_KEY_DOWN;
		else
			key = EVENT_SKILL_TELEPORT_KEY_UP;
		break;

	default:
		break;
	}

	if (client_n == 1 && p1_ptr != NULL)
		p1_ptr->key_update(key);
	else if (client_n == 2 && p2_ptr != NULL)
		p2_ptr->key_update(key);


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
			temp_info.X_Direction = temp_player->X_Direction;

		}
		sending_data->players[i] = temp_info;
	}

	// 공격 정보를 Game_Data에 저장
	for (int i = 0; i < MAX_ATTACKS; ++i)
	{
		Attack_Info temp_info;
		Attack* temp_attack = Stage_Attack_Object_List[i];

		if (temp_attack != nullptr)
		{
			temp_info.pos = temp_attack->pos;
			temp_info.X_Direction = temp_attack->X_Direction;
			temp_info.attack_type = (temp_attack->selected_character_type * 10) + temp_attack->attack_type;
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
	// 호출 횟수 증가
	call_count++;

	// 현재 시간과 마지막 시간 비교
	auto now = std::chrono::steady_clock::now();
	auto elapsed_time = std::chrono::duration_cast<std::chrono::seconds>(now - last_time).count();
	if (elapsed_time >= 1) 
	{ 
		// 1초가 경과한 경우
		std::wstring debug_message = L"Broadcast_GameData_All 호출 횟수 (1초): " + std::to_wstring(call_count.load()) + L"\n";
		OutputDebugString(debug_message.c_str());

		// 출력 (업데이트와 분리)
		system("cls");
		std::cout << "=== Debug Info ===\n";

		// 플레이어 정보 출력
		if (p1_ptr)
		{
			std::cout << "p1 - ";
			p1_ptr->Print_info();
		}
		if (p2_ptr)
		{
			std::cout << "p2 - ";
			p2_ptr->Print_info();
		}

		// 공격 객체 정보 출력
		int i = 0;
		for (Object* obj_ptr : Stage_Attack_Object_List)
		{
			if (obj_ptr)
			{
				std::cout << "Attack_Info " << i << ": ";
				obj_ptr->Print_info();
			}
			++i;
		}

		call_count = 0; // 카운터 초기화
		last_time = now; // 타이머 갱신
	}


	if (client1_socket != INVALID_SOCKET)
	{
		send(client1_socket, (char*)data, sizeof(Game_Data), 0);

	}
	if (client2_socket != INVALID_SOCKET)
	{
		send(client2_socket, (char*)data, sizeof(Game_Data), 0);

	}

	delete data;
}

Player* Server::Get_Player(int Client)
{
	if (Client == 1)
	{
		if (p1_ptr != NULL)
			if (p1_ptr->Get_StateMachine() != NULL)
				return p1_ptr;
	}
	else if (Client == 2)
	{
		if (p2_ptr != NULL)
			if (p2_ptr->Get_StateMachine() != NULL)
				return p2_ptr;
	}
	
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