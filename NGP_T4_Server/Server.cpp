#pragma once
#include "stdafx.h"
#include "Server.h"


std::vector<Object*> Public_Object_List(20);

void Server::Update_Server()
{
	if(p1_ptr)
		p1_ptr->update();
	if(p2_ptr)
		p2_ptr->update();

	for (Object* obj_ptr : Stage_Object_List)
	{
		obj_ptr->update();
	}
	    //������Ʈ ���� �� ������Ʈ
		// �÷��̾�� ������ ����� Ű ���� ��� ������Ʈ
		// ���� ������ �׳� ������Ʈ	
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

	//	Key_Info ��� �÷��̾���� Ű ���� ������Ʈ

}

void Server::Delete_Player(int Client)
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