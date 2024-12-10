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

void Server::Add_P1(Player* p_ptr)
{
	p1_ptr = p_ptr;
	
	char player_id[32] = "Server_P1";
	std::memcpy(p1_ptr->player_ID, player_id, sizeof(player_id));
}

void Server::Add_P2(Player* p_ptr)
{
	p2_ptr = p_ptr;

	char player_id[32] = "Server_P2";
	std::memcpy(p2_ptr->player_ID, player_id, sizeof(player_id));
}

void Server::Add_Skill_Object(Object* skill_ptr)
{
	auto empty_space = std::find(Stage_Attack_Object_List.begin(), Stage_Attack_Object_List.end(), static_cast<Attack*>(nullptr));

	if (empty_space != Stage_Attack_Object_List.end()) 
		*empty_space = static_cast<Attack*>(skill_ptr);
	else
		std::cout << "No space for skill_object in game world" << std::endl;
	
}

void Server::Update_Character_Select(float elapsed_time)
{
	// �������� ������Ʈ
	if(p1_ptr != NULL && p2_ptr != NULL)
		if (p1_ptr->game_ready && p2_ptr->game_ready)
		{
			p1_ptr->Set_Character(this);
			p2_ptr->Set_Character(this);
			server_mode = Server_Mode::Game_Play;
		}


}

void Server::Update_Game_World(float elapsed_time)
{
	// �ð� ������Ʈ
	game_time += elapsed_time;
	// std::cout << game_time << "\n";
	// �÷��̾� ������Ʈ
	if (p1_ptr) 
		p1_ptr->update(elapsed_time);

	if (p2_ptr) 
		p2_ptr->update(elapsed_time);

	// ���� ��ü ������Ʈ
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

	if (p1_ptr == NULL || p2_ptr == NULL)
	{
		server_mode = Server_Mode::Character_Select;

		if (p1_ptr != NULL)
		{
			delete p1_ptr;
			p1_ptr = new Player();
		}

		if (p2_ptr != NULL)
		{
			delete p2_ptr;
			p2_ptr = new Player();
		}
	}
}

void Server::Update_Collision(float Elapsed_time)
{
	if (p1_ptr == NULL || p2_ptr == NULL)
		return;

	BoundingBox* p1_box = NULL;
	BoundingBox* p2_box = NULL;
	std::string_view p1_ID;
	std::string_view p2_ID;

	BoundingBox* p1_normal_attack_box = NULL;
	BoundingBox* p2_normal_attack_box = NULL;

	if (p1_ptr != NULL)
	{
		p1_box = p1_ptr->Get_Player_BoundingBox();
		p1_ID = std::string_view(p1_ptr->player_ID, std::strlen(p1_ptr->player_ID));
	}

	if (p2_ptr != NULL)
	{
		p2_box = p2_ptr->Get_Player_BoundingBox();
		p2_ID = std::string_view(p2_ptr->player_ID, std::strlen(p2_ptr->player_ID));
	}

	// �Ϲ� �������� �ƴϸ� NULL ��ȯ��
	if (p1_ptr != NULL)
		p1_normal_attack_box = p1_ptr->Get_Normal_Attack_BoundingBox();
	
	if (p2_ptr != NULL)
		p2_normal_attack_box = p2_ptr->Get_Normal_Attack_BoundingBox();

	if (p1_box != NULL && p2_normal_attack_box != NULL)
	{
		bool is_hurt = p1_box->intersects(p2_normal_attack_box);
		if (is_hurt)
		{
			if (p2_ptr->Get_StateMachine()->combo_stack <= 3)
			{
				p1_ptr->Get_StateMachine()->changeState(State::Hit_Easy, EVENT_NONE);
				p1_ptr->hp -= Normal_Damage;
			}
			else
			{
				p1_ptr->Get_StateMachine()->changeState(State::Hit_Hard, EVENT_NONE);
				p1_ptr->hp -= Normal_Damage * 2;
			}			
		}
	}
	if (p2_box != NULL && p1_normal_attack_box != NULL)
	{
		bool is_hurt = p2_box->intersects(p1_normal_attack_box);
		if (is_hurt)
		{
			if (p1_ptr->Get_StateMachine()->combo_stack <= 3)
			{
				p2_ptr->Get_StateMachine()->changeState(State::Hit_Easy, EVENT_NONE);
				p2_ptr->hp -= Normal_Damage;
			}
			else
			{
				p2_ptr->Get_StateMachine()->changeState(State::Hit_Hard, EVENT_NONE);
				p2_ptr->hp -= Normal_Damage * 2;
			}
		}
	}


	for (Attack* attack_ptr : Stage_Attack_Object_List)
	{
		if (attack_ptr != NULL)
		{
			BoundingBox* attack_obj_box = attack_ptr->Get_Attack_BoundingBox();
			std::string_view attack_ID(attack_ptr->player_ID, std::strlen(attack_ptr->player_ID));

			if (attack_obj_box != NULL)
			{
				if (p1_ID != attack_ID)
				{
					bool is_hurt = p1_box->intersects(attack_obj_box);

					if (is_hurt && attack_ptr->Has_Target()) // Ÿ���� �ִ� ���� ��ü == �Ƹ��׶�					
						p1_ptr->hp -= attack_ptr->fire_stack * DOT_Damage * Elapsed_time;
					else if (is_hurt && attack_ptr->attack_type == 1) // ������
					{
						p1_ptr->Get_StateMachine()->changeState(State::Hit_Easy, EVENT_NONE); 
						p1_ptr->hp -= Shuriken_Damage;

						attack_ptr->life = false;

					}
					else if (is_hurt) // ��ų ��ü
					{
						float player_x_pos = p1_ptr->Get_StateMachine()->Get_Pos().x;
						float attack_x_pos = attack_ptr->pos.x;

						if (player_x_pos < attack_x_pos) // �����ʿ��� ���ƿ��� �� �¾Ҵٸ�
							p1_ptr->Get_StateMachine()->X_Direction = true;		
						else if (player_x_pos < attack_x_pos) // ���ʿ��� ���ƿ��� �� �¾Ҵٸ�
							p1_ptr->Get_StateMachine()->X_Direction = false;

						p1_ptr->Get_StateMachine()->changeState(State::Hit_Hard, EVENT_NONE); 
						p1_ptr->hp -= Skill_Damage;
					}
				}
				else if (p2_ID != attack_ID)
				{
					bool is_hurt = p2_box->intersects(attack_obj_box);

					if (is_hurt && attack_ptr->Has_Target()) // Ÿ���� �ִ� ���� ��ü == �Ƹ��׶�					
						p2_ptr->hp -= attack_ptr->fire_stack * DOT_Damage * Elapsed_time;
					else if (is_hurt && attack_ptr->attack_type == 1) // ������
					{
						p2_ptr->Get_StateMachine()->changeState(State::Hit_Easy, EVENT_NONE);
						p2_ptr->hp -= Shuriken_Damage;

						attack_ptr->life = false;
					}
					else if (is_hurt) // ��ų ��ü
					{
						float player_x_pos = p2_ptr->Get_StateMachine()->Get_Pos().x;
						float attack_x_pos = attack_ptr->pos.x;

						if (player_x_pos < attack_x_pos) // �����ʿ��� ���ƿ��� �� �¾Ҵٸ�
							p2_ptr->Get_StateMachine()->X_Direction = true;
						else if (player_x_pos < attack_x_pos) // ���ʿ��� ���ƿ��� �� �¾Ҵٸ�
							p2_ptr->Get_StateMachine()->X_Direction = false;

						p2_ptr->Get_StateMachine()->changeState(State::Hit_Hard, EVENT_NONE);
						p2_ptr->hp -= Skill_Damage;
					}
				}
			}
		}
	}

	if (p1_ptr->hp <= 0.0f)
	{
		if(p1_ptr != NULL && p1_ptr->Get_StateMachine()->Get_State() != 13)
			p1_ptr->Get_StateMachine()->changeState(State::Lose, EVENT_NONE);
		if (p2_ptr != NULL && p2_ptr->Get_StateMachine()->Get_State() != 12)
			p2_ptr->Get_StateMachine()->changeState(State::Win, EVENT_NONE);
	}
	else if(p2_ptr->hp <= 0.0f)
	{
		if (p1_ptr != NULL && p1_ptr->Get_StateMachine()->Get_State() != 12)
			p1_ptr->Get_StateMachine()->changeState(State::Win, EVENT_NONE);
		if (p2_ptr != NULL && p2_ptr->Get_StateMachine()->Get_State() != 13)
			p2_ptr->Get_StateMachine()->changeState(State::Lose, EVENT_NONE);
	}

	// �Ƹ��׶� ��ġ�� ��� ��ü ó��
	Check_Overlap();
}

void Server::Check_Overlap()
{
	// �Ƹ��׶� ��ġ�� ��� ��ü ó��
	for (int i = 0; i < Stage_Attack_Object_List.size(); ++i)
	{
		Attack* attack_ptr_1 = Stage_Attack_Object_List[i];
		if (attack_ptr_1 == NULL)
			continue;
		BoundingBox* attack_obj_1_box = attack_ptr_1->Get_Attack_BoundingBox();
		std::string_view attack_ID_1(attack_ptr_1->player_ID, std::strlen(attack_ptr_1->player_ID));

		// �� ��° ��ü
		for (int j = i + 1; j < Stage_Attack_Object_List.size(); ++j)
		{
			Attack* attack_ptr_2 = Stage_Attack_Object_List[j];
			if (attack_ptr_2 == NULL)
				continue;

			BoundingBox* attack_obj_2_box = attack_ptr_2->Get_Attack_BoundingBox();
			std::string_view attack_ID_2(attack_ptr_2->player_ID, std::strlen(attack_ptr_2->player_ID));

			if (attack_ID_1 == attack_ID_2)  // ���� �÷��̾��� ������ ���
			{
				if (attack_obj_1_box->intersects(attack_obj_2_box))  // �浹 �˻�
				{
					if (attack_ptr_1->Has_Target() && attack_ptr_2->Has_Target()) // �� �� �Ƹ��׶󽺶��
					{
						attack_ptr_1->fire_stack += 1;  // ���� ���� ����
						attack_ptr_2->life = false;    // ������ ��ü�� ����
					}
				}
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

	if (server_mode == Server_Mode::Character_Select)
		Select_Mode_Decoding(key_info);
	else if (server_mode == Server_Mode::Game_Play)
		Game_Mode_Decoding(key_info);

}

void Server::Select_Mode_Decoding(std::pair<int, Key_Info>* key_info)
{
	int client_n = key_info->first;
	Key_Info key_value = key_info->second;
	int key = EVENT_NONE;

	switch (key_value.key_name)
	{
	case 'a':
	case 'A':
		if (key_value.key_action == 1)
			key = EVENT_MOVE_LEFT_KEY_DOWN;
		break;

	case 'd':
	case 'D':
		if (key_value.key_action == 1)
			key = EVENT_MOVE_RIGHT_KEY_DOWN;
		break;

	case 32:
		if (key_value.key_action == 1)
			key = EVENT_PLAYER_SELECT_CHARACTER;
		break;

	default:
		break;
	}

	if (std::memcmp(key_value.player_ID, "None", 4) == 0)
	{
		if (p1_ptr != NULL)	p1_ptr->key_update(key, Server_Mode::Character_Select);
		if (p2_ptr != NULL)	p2_ptr->key_update(key, Server_Mode::Character_Select);
	}
	else
	{
		// None�� �ƴϰ� �̸��� ����ִٸ� �̸� ���� + ĳ���� ���� 
		if (p1_ptr != NULL && client_n == 1)
			if (std::memcmp(key_value.player_ID, "None", 4) != 0)
			{
				std::memcpy(p1_ptr->player_ID, key_value.player_ID, sizeof(key_value.player_ID));
				p1_ptr->key_update(key, Server_Mode::Character_Select);
			}

		// None�� �ƴϰ� �̸��� ����ִٸ� �̸� ���� + ĳ���� ����
		if (p2_ptr != NULL && client_n == 2)
			if (std::memcmp(key_value.player_ID, "None", 4) != 0)
			{
				std::memcpy(p2_ptr->player_ID, key_value.player_ID, sizeof(key_value.player_ID));
				p2_ptr->key_update(key, Server_Mode::Character_Select);
			}
	}
}
void Server::Game_Mode_Decoding(std::pair<int, Key_Info>* key_info)
{
	int client_n = key_info->first;
	Key_Info key_value = key_info->second;
	int key = EVENT_NONE;

	switch (key_value.key_name)
	{
	case 'a':
	case 'A':
		if (key_value.key_action == 1)
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

	// "None"�� ������ �ƹ� �Է� ���� ������Ʈ
	if (std::memcmp(key_value.player_ID, "None", 4) == 0)
	{
		if (p1_ptr != NULL)	p1_ptr->key_update(key, Server_Mode::Game_Play);
		if (p2_ptr != NULL)	p2_ptr->key_update(key, Server_Mode::Game_Play);
	}
	else
	{
		// P1�� �Է��̶�� ����
		if (p1_ptr != NULL && std::memcmp(key_value.player_ID, p1_ptr->player_ID, 32) == 0)
			p1_ptr->key_update(key, Server_Mode::Game_Play);
		else if (p2_ptr != NULL && std::memcmp(key_value.player_ID, p2_ptr->player_ID, 32) == 0)
			p2_ptr->key_update(key, Server_Mode::Game_Play);
	}
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
			temp_info.player_ready = temp_player->game_ready;
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
			
			if (temp_attack->sticked == true) // �Ƹ��׶� ���� ����
				temp_info.attack_type += 1;

			temp_info.sprite_index = temp_attack->sprite_index;
		}
		sending_data->attacks[i] = temp_info;
	}

	// �� �� �������� Game_Data�� ����
	ETC_Info etc_info;
	{
		Player* p1_ptr = Get_Player(1);
		Player* p2_ptr = Get_Player(2);

		etc_info.game_time = game_time;
		if (p1_ptr != NULL)
		{
			etc_info.player1_hp = int(p1_ptr->hp);
			etc_info.player1_sp = p1_ptr->sp;
		}

		if (p2_ptr != NULL)
		{
			etc_info.player2_hp = int(p2_ptr->hp);
			etc_info.player2_sp = p2_ptr->sp;
		}
	}
	sending_data->etc = etc_info;

	// �������� �Ҵ�� ������ ��ȯ
	return sending_data;  
}

void Server::Broadcast_GameData_All(Game_Data* data)
{
	// ȣ�� Ƚ�� ����
	call_count++;

	// ���� �ð��� ������ �ð� ��
	auto now = std::chrono::steady_clock::now();
	auto elapsed_time = std::chrono::duration_cast<std::chrono::milliseconds>(now - last_time).count();

	if (elapsed_time >= 1000) { // 1�ʰ� ����� ���
		// ����� �޽��� ���
		std::wstring debug_message = L"Broadcast_GameData_All ȣ�� Ƚ�� (1��): " + std::to_wstring(call_count.load()) + L"\n";
		OutputDebugString(debug_message.c_str());

		// 1�� Ÿ�̸� ����
		last_time = now;
		call_count = 0; // ȣ�� Ƚ�� �ʱ�ȭ

		// ��� (������Ʈ�� �и�)
		{
			system("cls");
			std::cout << "=== Debug Info ===\n";

			// �÷��̾� ���� ���
			if (p1_ptr)
			{
				std::cout << p1_ptr->player_ID << " - ";
				p1_ptr->Print_info(server_mode);
			}
			if (p2_ptr)
			{
				std::cout << p2_ptr->player_ID << " - ";
				p2_ptr->Print_info(server_mode);
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
		}
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
				return p1_ptr;
	}
	else if (Client == 2)
	{
		if (p2_ptr != NULL)
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