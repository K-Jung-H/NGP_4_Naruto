#pragma once
#include "algorithm"

struct Key_State 
{
	// true == Key_Down
	// false == Key_Up

	bool up; // w 또는 방향키
	bool down; // s 또는 방향키
	bool left; // a 또는 방향키
	bool right; // d 또는 방향키

	Key_State()
	{
		up = false;		down = false;
		left = false;		right = false;
	}
	void update(int key_state);
};


// 형식 통일 필요 없는 구조체
//=========================================================================

enum class State 
{
	Idle,
	Run,
	Jump,
	Teleport,
	Attack_Normal,
	Attack_Run,
	Attack_Jump,
	Attack_Shuriken,
	Attack_Skill_1,
	Attack_Skill_2,
	Hit_Easy,
	Hit_Hard,
	Win,
	Lose,
};

class Server;

// 플레이어 상태 머신 
class StateMachine
{
protected:
	State lastState = State::Idle;
	State currentState = State::Idle; // 현재 상태
	Server* server_ptr;

	Key_State key_state;
public:
	char player_ID[32] = { 0, };
	Position pos;
	bool X_Direction; // Left: false, Right: true
	bool Move_Left = false;
	bool Move_Right = false;


	int sprite_index = 0;
	float sprite_frame_value = 0.0f;

	int jump_value = 0;
	bool Y_Direction = false; // Down: false, Up: true
	bool is_air = false;


	float attack_after_time = 0.0f;
	bool attack_combo = false;
	bool attack_action = false;
	int combo_stack = 0;

	StateMachine() { 
		currentState = State::Idle;
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y;
	}

	void start();
	void Set_Server(Server* server) { server_ptr = server; };
	void update(float Elapsed_time);

	void handleEvent(int key_event);
	void changeState(State newState, int key_event);

	int Get_Sprite_Index(float Elapsed_time, int sprite_range, bool index_loop);

	Position Get_Pos() { return pos; };
	int  Get_State();
	void Set_Draw_Direction();

private:

	void enterState(State state, int key_event);

	void exitState(State state, int key_event);

	virtual void doAction(State state, float Elapsed_time);

};

class Naruto_StateMachine : public StateMachine
{
public:
	Naruto_StateMachine() { 
		currentState = State::Idle; 
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y;
	}

	void doAction(State state, float Elapsed_time) override;
};

class Sasuke_StateMachine : public StateMachine
{
public:
	Sasuke_StateMachine() { 
		currentState = State::Idle; 
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y;
	}

	void doAction(State state, float Elapsed_time) override;
};

class Itachi_StateMachine : public StateMachine
{
public:
	Itachi_StateMachine() { 
		currentState = State::Idle; 
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y;
	}

	void doAction(State state, float Elapsed_time) override;
};

class Object
{
public:
	char player_ID[32] = { 0, };
	Position pos;
	bool X_Direction; // Left: false, Right: true
	int sprite_index = 0;


	virtual void update(float Elapsed_time) {};
	virtual	 void Print_info() {};
};

class Player : public Object
{
private:
	StateMachine* state_machine;
	

public:
	int hp;
	int sp;
	int state;
	int selected_character_type;

	void Set_Character(int n, Server* server_ptr);
	StateMachine* Get_StateMachine() { return state_machine; };
	void  update(float Elapsed_time) override;
	void key_update(int key_event);
	void synchronize_state_machine();

	void Print_info();
};


#define ATTACK_TYPE_SHURIKEN 1
#define ATTACK_TYPE_SKILL_1 2
#define ATTACK_TYPE_SKILL_2 3

class Attack : public Object
{
private:
	float sprite_frame_value = 0.0f;

public:
	int selected_character_type = 0;
	int attack_type = 0; // 1. 수리검, 2. 스킬 1, 3. 스킬 2

	Attack(const char player_id[32], int c_t, int a_t, Position p, bool x_dir)
	{
		std::copy(player_id, player_id + 32, player_ID);
		selected_character_type = c_t;
		attack_type = a_t;
		pos = p;
		X_Direction = x_dir;
	}

	void  update(float Elapsed_time) override;
	int Get_Sprite_Index(float Elapsed_time, int sprite_range, bool index_loop);

	void Print_info();
};
