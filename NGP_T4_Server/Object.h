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

enum class State {
	Idle,
	Run,
	Jump,
	Attack
};

// 플레이어 상태 머신 
class StateMachine
{
private:
	State currentState; // 현재 상태
public:
	Position pos;
	bool X_Direction; // Left: false, Right: true

	StateMachine() : currentState(State::Idle) {}

	void start();

	void update();

	void handleEvent(int key_event);

	Position Get_Pos() { return pos; };
	int  Get_State() { return 1; };
private:
	void changeState(State newState, int key_event);

	void enterState(State state, int key_event);

	void exitState(State state, int key_event);

	void doAction(State state);

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
	StateMachine state_machine;
	Key_State key_state;

public:
	int hp;
	int sp;
	int state;
	int selected_character_type;


	void  update() override;
	void key_update(int key_event);
};

class Attack : public Object
{
public:
	int attack_type;

	void  update() override;
};
