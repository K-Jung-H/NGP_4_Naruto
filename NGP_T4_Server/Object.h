#pragma once

struct Key_State 
{
	// true == Key_Down
	// false == Key_Up

	bool up; // w 또는 방향키
	bool down; // s 또는 방향키
	bool left; // a 또는 방향키
	bool right; // d 또는 방향키

	bool normal_attack;	// c 또는 ','
	bool ranged_attack;	// b  또는 '/'
	bool skill_attack_1;		// f 또는 l
	bool skill_attack_2;		// g 또는 ';'
	bool teleport;			// v 또는 '.'

};

// 형식 통일 필요 없는 구조체
//=========================================================================

enum class State 
{
	Idle,
	Run,
	Jump,
	Attack_Normal,
	Attack_Skill_1,
	Attack_Skill_2,
	Hit_Easy,
	Hit_Hard,
	Win,
	Lose,
};

// 플레이어 상태 머신 
class StateMachine
{
protected:
	State currentState; // 현재 상태
public:
	Position pos;
	bool X_Direction; // Left: false, Right: true
	bool Move_Left = false;
	bool Move_Right = false;

	int sprite_index = 0;
	float sprite_frame_value = 0.0f;

	int jump_value = 0;
	bool Y_Direction = false; // Down: false, Up: true
	bool is_air = false;

	StateMachine() : currentState(State::Idle) { 
		sprite_index = 0;
		pos.x = 500;
		pos.y = Ground_Y;
	}

	void start();

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
	int sprite_index;

	virtual void update(float Elapsed_time) {};
};

class Player : public Object
{
private:
	StateMachine* state_machine;
	Key_State key_state;

public:
	int hp;
	int sp;
	int state;
	int selected_character_type;

	void Set_Character(int n);
	void  update(float Elapsed_time) override;
	void key_update(int key_event);
	void synchronize_state_machine();
};

class Attack : public Object
{
public:
	int attack_type;

	void  update(float Elapsed_time) override;
};
