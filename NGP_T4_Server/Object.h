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

enum class State {
	Idle,
	Run,
	Jump,
	Attack
};

// �÷��̾� ���� �ӽ� 
class StateMachine
{
private:
	State currentState; // ���� ����
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
