#pragma once

class Object;

class Server
{
public:
	Player* p1_ptr = NULL;
	Player* p2_ptr = NULL;

	std::vector<Object*> Stage_Object_List; // 스킬 객체만 넣을 것
	
	void Update_Server();
	void Add_P1(Object* p_ptr) { p1_ptr = static_cast<Player*>(p_ptr); }
	void Add_P2(Object* p_ptr) { p2_ptr = static_cast<Player*>(p_ptr); }
};

// 소켓 함수 오류 출력 후 종료
void err_quit(const char* msg);

// 소켓 함수 오류 출력
void err_display(const char* msg);
// 소켓 함수 오류 출력
void err_display(int errcode);