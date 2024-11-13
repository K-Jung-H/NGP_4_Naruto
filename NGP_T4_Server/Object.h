#pragma once

struct Key_State 
{
	// true == Key_Down
	// false == Key_Up

	bool up; // w �Ǵ� ����Ű
	bool down; // s �Ǵ� ����Ű
	bool left; // a �Ǵ� ����Ű
	bool right; // d �Ǵ� ����Ű

	bool normal_attack;	// c �Ǵ� ','
	bool ranged_attack;	// b  �Ǵ� '/'
	bool skill_attack_1;		// f �Ǵ� l
	bool skill_attack_2;		// g �Ǵ� ';'
	bool teleport;			// v �Ǵ� '.'

};

// ���� ���� �ʿ� ���� ����ü
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

// �÷��̾� ���� �ӽ� 
class StateMachine
{
protected:
	State currentState; // ���� ����
public:
	Position pos;
	bool X_Direction; // Left: false, Right: true
	bool Move_Left = false;
	bool Move_Right = false;
	int sprite_index = 0;

	int jump_value = 0;
	bool Y_Direction = false; // Down: false, Up: true
	bool is_air = false;

	StateMachine() : currentState(State::Idle) { 
		sprite_index = 0;
		pos.x = 500;
		pos.y = 300;
	}

	void start();

	void update();

	void handleEvent(int key_event);
	void changeState(State newState, int key_event);

	Position Get_Pos() { return pos; };
	int  Get_State();
	void Set_Draw_Direction();

private:

	void enterState(State state, int key_event);

	void exitState(State state, int key_event);

	virtual void doAction(State state);

};

class Naruto_StateMachine : public StateMachine
{
public:
	Naruto_StateMachine() { 
		currentState = State::Idle; 
		sprite_index = 0;
		pos.x = 500;
		pos.y = 300;
	}

	void doAction(State state) override;
};

class Sasuke_StateMachine : public StateMachine
{
public:
	Sasuke_StateMachine() { 
		currentState = State::Idle; 
		sprite_index = 0;
		pos.x = 500;
		pos.y = 300;
	}

	void doAction(State state) override;
};

class Itachi_StateMachine : public StateMachine
{
public:
	Itachi_StateMachine() { 
		currentState = State::Idle; 
		sprite_index = 0;
		pos.x = 500;
		pos.y = 300;
	}

	void doAction(State state) override;
};

class Object
{
public:
	char player_ID[32] = { 0, };
	Position pos;
	bool X_Direction; // Left: false, Right: true
	int sprite_index;

	virtual void update() {};
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
	void  update() override;
	void key_update(int key_event);
	void synchronize_state_machine();
};

class Attack : public Object
{
public:
	int attack_type;

	void  update() override;
};
