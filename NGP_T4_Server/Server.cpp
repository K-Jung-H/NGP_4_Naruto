#pragma once
#include "stdafx.h"
#include "Server.h"

void Server::EnqueueKeyInput(int client_n, const Key_Info& keyInfo)
{
	EnterCriticalSection(&cs_key_queue);
	keyQueue.push(std::make_pair(client_n, keyInfo));  // ť�� Ű �Է� �߰�
	LeaveCriticalSection(&cs_key_queue);
}

// Ű �Է� ó�� �Լ� (ť���� ������)
bool Server::DequeueKeyInput(std::pair<int, Key_Info>& keyInfo)
{
	EnterCriticalSection(&cs_key_queue);
	if (!keyQueue.empty()) {
		keyInfo = keyQueue.front();  // ť�� ù ��° �׸��� ������
		keyQueue.pop();  // �׸� ����
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
	static int debug_tick = 0;
	constexpr int DEBUG_TICK_INTERVAL = 10; // ����� ����
	++debug_tick;

	// �ܼ� ȭ���� ����� ��� ��� ���� ��ġ�� ���
	std::cout << "\033[2J\033[H"; // ANSI escape �ڵ�� ȭ�� ����� �� Ŀ�� �̵�

	// �÷��̾� ������Ʈ
	if (p1_ptr) 
		p1_ptr->update(elapsed_time);

	if (p2_ptr) 
		p2_ptr->update(elapsed_time);

	// ���� ��ü ������Ʈ
	for (Object* obj_ptr : Stage_Attack_Object_List) 
		if (obj_ptr) 
			obj_ptr->update(elapsed_time);
	

	// ��� (������Ʈ�� �и�)
	std::cout << "=== Debug Info ===\n";

	// �÷��̾� ���� ���
	if (p1_ptr && debug_tick > DEBUG_TICK_INTERVAL) 
	{
		p1_ptr->Print_info();
	}

	if (p2_ptr && debug_tick > DEBUG_TICK_INTERVAL)
	{
		p2_ptr->Print_info();
	}

	// ���� ��ü ���� ���
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

	// ����� ƽ �ʱ�ȭ
	if (debug_tick > DEBUG_TICK_INTERVAL) 
	{
		debug_tick = 0;
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
	// Game_Data ��ü�� �������� �Ҵ�
	Game_Data* sending_data = new Game_Data;

	// �÷��̾� ������ Game_Data�� ����
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

	// ���� ������ Game_Data�� ����
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

	// �� �� �������� Game_Data�� ����
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

	// �������� �Ҵ�� ������ ��ȯ
	return sending_data;  
}

void Server::Broadcast_GameData_All(Game_Data* data)
{
	std::string result_message = "";
	if (client1_socket != INVALID_SOCKET)
	{
		send(client1_socket, (char*)data, sizeof(Game_Data), 0);
		result_message += "1P - ";
	}
	if (client2_socket != INVALID_SOCKET)
	{
		send(client2_socket, (char*)data, sizeof(Game_Data), 0);
		result_message += "2P - ";
	}

	//if(result_message.length() > 0)
	//	std::cout << result_message << " send_success" << std::endl;
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