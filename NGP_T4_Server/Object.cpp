#include "stdafx.h"
#include "Object.h"
//========================================================
// 상태 머신
void StateMachine::start()
{
    enterState(currentState, 0);
}

void StateMachine::update() 
{
    // 현재 상태에 따른 동작을 수행
    doAction(currentState);

    if (currentState == State::Jump)
    {
        changeState(State::Idle, EVENT_NONE);
    }
}

void StateMachine::handleEvent(int key_event)
{
    switch (currentState)
    {
    case State::Idle:
    {
        if (key_event == EVENT_MOVE_LEFT_KEY_DOWN)
            Move_Left = true;
        else if (key_event == EVENT_MOVE_RIGHT_KEY_DOWN)
            Move_Right = true;
        else if (key_event == EVENT_MOVE_LEFT_KEY_UP)
            Move_Left = false;
        else if (key_event == EVENT_MOVE_RIGHT_KEY_UP)
            Move_Right = false;

        if (Move_Left || Move_Right)
            changeState(State::Run, key_event);
        
        if (key_event == EVENT_MOVE_UP_KEY_DOWN)
        {
            changeState(State::Jump, key_event);
        }
    }
    break;

    case State::Run:
    {
        if (key_event == EVENT_MOVE_LEFT_KEY_DOWN)
            Move_Left = true;
        else if (key_event == EVENT_MOVE_RIGHT_KEY_DOWN)
            Move_Right = true;
        else if (key_event == EVENT_MOVE_LEFT_KEY_UP)
            Move_Left = false;
        else if (key_event == EVENT_MOVE_RIGHT_KEY_UP)
            Move_Right = false;

        if ((Move_Left && Move_Right) || !Move_Left && !Move_Right)
            changeState(State::Idle, key_event);

        if (key_event == EVENT_MOVE_UP_KEY_UP)
        {
            changeState(State::Jump, key_event);
        }
    }
    break;

    case State::Jump:
        if (key_event == 0) 
        {
        }
        break;

    case State::Attack_Normal:
        if (key_event == 0) 
        { 
            changeState(State::Idle, key_event);
        }
        break;

    default:
        break;
    }
}

void StateMachine::changeState(State newState, int key_event)
{
    exitState(currentState, key_event);
    currentState = newState;
    enterState(currentState, key_event);
}

void StateMachine::enterState(State state, int key_event)
{

    switch (state)
    {
    case State::Idle:
        break;
    case State::Run:
        break;
    case State::Jump:
        break;

    default:
        break;
    }
}

void StateMachine::exitState(State state, int key_event)
{
    sprite_index = 0;
}

void StateMachine::doAction(State state)
{
}

int  StateMachine::Get_State()
{
    switch (currentState)
    {
    case State::Idle:
        return STATE_IDLE;
        break;
    case State::Run:
        return STATE_RUN;
        break;
    case State::Jump:
        return STATE_JUMP;
        break;
    case State::Attack_Normal:
        return STATE_ATTACK_NORMAL;
        break;
    case State::Attack_Skill_1:
        return STATE_ATTACK_SKILL_1;
        break;
    case State::Attack_Skill_2:
        return STATE_ATTACK_SKILL_2;
        break;
    case State::Hit_Easy:
        return STATE_HIT_EASY;
        break;
    case State::Hit_Hard:
        return STATE_HIT_HARD;
        break;
    case State::Win:
        return STATE_WIN;
        break;
    case State::Lose:
        return STATE_LOSE;
        break;

    default:
        break;
    }
}

void StateMachine::Set_Draw_Direction()
{
    if (Move_Left && Move_Right)
        return;

    if (Move_Left)
        X_Direction = LEFT;
    if (Move_Right)
        X_Direction = RIGHT;

    return;
}
//========================================================
void Naruto_StateMachine::doAction(State state)
{
    switch (state)
    {
    case State::Idle:
        sprite_index = (sprite_index + 1) % 6;
        break;

    case State::Run:
    {
        sprite_index = (sprite_index + 1) % 6;
        if (Move_Left)
            pos.x -= 10;
        else if (Move_Right)
            pos.x += 10;

    }
    break;

    case State::Jump:
        break;

    default:
        break;
    }
    Set_Draw_Direction();
}

void Sasuke_StateMachine::doAction(State state)
{
}

void Itachi_StateMachine::doAction(State state)
{
}
//========================================================

void Player::Set_Character(int n)
{
    selected_character_type = n;

    if (n == CHARACTER_NARUTO)
        state_machine = new Naruto_StateMachine();
    else if (n == CHARACTER_SASUKE)
        state_machine = new Naruto_StateMachine();
    else if (n == CHARACTER_ITACHI)
        state_machine = new Naruto_StateMachine();
}

void Player::synchronize_state_machine()
{
    this->pos = state_machine->Get_Pos();
    this->state = state_machine->Get_State();
    this->sprite_index = state_machine->sprite_index;
    this->X_Direction = state_machine->X_Direction;
}

void Player::update()
{
    if (state_machine != NULL)
    {
        state_machine->update();
        synchronize_state_machine();
    }
}

void Player::key_update(int key_event)
{
    state_machine->handleEvent(key_event);
}

void Attack::update()
{
    // 위치 이동
}

