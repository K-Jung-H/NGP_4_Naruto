#pragma once
#include "algorithm"
#include "Collider.h"

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
enum class Server_Mode;

// 플레이어 상태 머신 
class StateMachine
{
protected:
	State lastState = State::Idle;
	State currentState = State::Idle; // 현재 상태
	Server* server_ptr;

	Key_State key_state;

	BoundingBox* player_boundingbox = NULL;
	BoundingBox* normal_attack_boundingbox = NULL;
	int sp = 0;
public:
	char player_ID[32] = { 0, };
	Position pos;
	bool X_Direction; // Left: false, Right: true
	bool Move_Left = false;
	bool Move_Right = false;

	bool is_easy_hit = false;
	bool is_hard_hit = false;
	bool is_protected = false;

	int sprite_index = 0;
	float sprite_frame_value = 0.0f;

	int jump_value = 0;
	bool Y_Direction = false; // Down: false, Up: true
	bool is_air = false;

	bool teleport_able = true;
	float teleport_cooltime = 0.0f;

	float attack_after_time = 0.0f;
	bool attack_combo = false;
	int combo_stack = 0;
	bool attack_action = false;

	bool attack_collision = false;

	StateMachine() { 
		currentState = State::Idle;
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y_Min;
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
	void Stage_Area_Check();
	int Get_SP() { return sp; };
	void Set_SP(int player_sp) { sp = player_sp; };

	virtual BoundingBox* Get_Player_BoundingBox() = 0;
	virtual BoundingBox* Get_Normal_Attack_BoundingBox() = 0;
private:

	void enterState(State state, int key_event);

	void exitState(State state, int key_event);

	virtual void doAction(State state, float Elapsed_time);

};

class Naruto_StateMachine : public StateMachine
{
public:
	Naruto_StateMachine() { 
		lastState = State::Idle;
		currentState = State::Idle; 
		player_boundingbox = new BoundingBox();
		normal_attack_boundingbox = new BoundingBox();

		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y_Min;
	}

	void doAction(State state, float Elapsed_time) override;
	virtual BoundingBox* Get_Player_BoundingBox() override;
	virtual BoundingBox* Get_Normal_Attack_BoundingBox() override;

};

class Sasuke_StateMachine : public StateMachine
{
public:
	Sasuke_StateMachine() { 
		lastState = State::Idle;
		currentState = State::Idle; 
		player_boundingbox = new BoundingBox();
		normal_attack_boundingbox = new BoundingBox();
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y_Min;
	}

	void doAction(State state, float Elapsed_time) override;
	virtual BoundingBox* Get_Player_BoundingBox() override;
	virtual BoundingBox* Get_Normal_Attack_BoundingBox() override;
};

class Itachi_StateMachine : public StateMachine
{
public:
	Itachi_StateMachine() { 
		lastState = State::Idle;
		currentState = State::Idle; 
		player_boundingbox = new BoundingBox();
		normal_attack_boundingbox = new BoundingBox();
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y_Min;
	}

	void doAction(State state, float Elapsed_time) override;
	virtual BoundingBox* Get_Player_BoundingBox() override;
	virtual BoundingBox* Get_Normal_Attack_BoundingBox() override;
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

#define SP_RESTORE_COOL_DOWN 3.0f
#define SP_RESTORE_DEGREE 30

class Player : public Object
{
private:
	StateMachine* state_machine = NULL;
	float sp_elapsed_time = 0.0f;

	
public:
	float hp = 400.0f;
	int sp = 0;
	int state = 0;
	int selected_character_type = 0;
	bool game_ready = false;

	Player()
	{
		game_ready = false;
		sp_elapsed_time = 0.0f;
		selected_character_type = 1;
		state = 0;
		hp = 400.0f;
		sp = 0;
	}

	void Set_Character(Server* server_ptr);
	StateMachine* Get_StateMachine() { return state_machine; };
	void  update(float Elapsed_time) override;
	void key_update(int key_event, Server_Mode mode);
	void synchronize_state_machine();

	void Print_info();
	BoundingBox* Get_Player_BoundingBox() 
	{
		BoundingBox* ptr = NULL;
		if (state_machine != NULL)
			ptr = state_machine->Get_Player_BoundingBox();
		return ptr;
	};

	BoundingBox* Get_Normal_Attack_BoundingBox()
	{
		BoundingBox* ptr = NULL;
		if (state_machine != NULL)
		{
			int player_state = state_machine->Get_State();
			if (player_state == STATE_ATTACK_NORMAL_1 ||
				player_state == STATE_ATTACK_NORMAL_2 ||
				player_state == STATE_ATTACK_NORMAL_3 ||
				player_state == STATE_ATTACK_NORMAL_4 ||
				player_state == STATE_ATTACK_RUN ||
				player_state == STATE_ATTACK_JUMP)
				ptr = state_machine->Get_Normal_Attack_BoundingBox();
		}
		return ptr;
	}
};


#define ATTACK_TYPE_SHURIKEN 1
#define ATTACK_TYPE_SKILL_1 2
#define ATTACK_TYPE_SKILL_2 3

class Attack : public Object
{
private:
	BoundingBox* attack_boundingbox = NULL;

	float sprite_frame_value = 0.0f;
	Player* target_ptr = NULL;	// 이타치 - 아마테라스

public:
	bool life = true;
	int selected_character_type = 0;
	int attack_type = 0; // 1. 수리검, 2. 스킬 1, 3. 스킬 2

	bool sticked = false;			// 이타치 - 아마테라스
	int fire_stack = 1;

	Attack(const char player_id[32], int c_t, int a_t, Position p, bool x_dir)
	{
		std::copy(player_id, player_id + 32, player_ID);
		selected_character_type = c_t;
		attack_type = a_t;
		pos = p;
		X_Direction = x_dir;
		attack_boundingbox = new BoundingBox();
	}

	void  update(float Elapsed_time) override;
	BoundingBox* Get_Attack_BoundingBox();

	int Get_Sprite_Index(float Elapsed_time, int sprite_range, bool index_loop);
	void Set_Target(Player* player_ptr) { target_ptr = player_ptr; } // 아마테라스 전용
	bool Has_Target() { return (target_ptr != NULL); }
	void Print_info();
};
