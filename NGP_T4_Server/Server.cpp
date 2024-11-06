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