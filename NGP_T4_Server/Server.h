#pragma once

class Object;

class Server
{
public:
	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

	std::vector<Object*> Stage_Object_List; // ��ų ��ü�� ���� ��
	
	void Update_Server();
	void Add_P1(Object* p_ptr) { p1_ptr = static_cast<Player*>(p_ptr); }
	void Add_P2(Object* p_ptr) { p2_ptr = static_cast<Player*>(p_ptr); }
};

// ���� �Լ� ���� ��� �� ����
void err_quit(const char* msg);

// ���� �Լ� ���� ���
void err_display(const char* msg);
// ���� �Լ� ���� ���
void err_display(int errcode);