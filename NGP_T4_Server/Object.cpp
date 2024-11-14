#include "stdafx.h"
#include "Object.h"
//========================================================
// 상태 머신
void StateMachine::start()
{
    enterState(currentState, 0);
}

void StateMachine::update(float Elapsed_time)
{
    // 현재 상태에 따른 동작을 수행
    doAction(currentState, Elapsed_time);
}

void StateMachine::handleEvent(int key_event)
{
    if (key_event == EVENT_MOVE_LEFT_KEY_DOWN)
        Move_Left = true;
    else if (key_event == EVENT_MOVE_RIGHT_KEY_DOWN)
        Move_Right = true;
    else if (key_event == EVENT_MOVE_LEFT_KEY_UP)
        Move_Left = false;
    else if (key_event == EVENT_MOVE_RIGHT_KEY_UP)
        Move_Right = false;

    switch (currentState)
    {
    case State::Idle:
    {
        if (Move_Left != Move_Right)
            changeState(State::Run, key_event);
        
        if (key_event == EVENT_MOVE_UP_KEY_DOWN)
            changeState(State::Jump, key_event);

    }
    break;

    case State::Run:
    {
        if (Move_Left == Move_Right)
            changeState(State::Idle, key_event);

        if (key_event == EVENT_MOVE_UP_KEY_DOWN)
            changeState(State::Jump, key_event);

    }
    break;

    case State::Jump:
    {
        if(key_event == EVENT_MOVE_UP_KEY_DOWN)
            changeState(State::Jump, key_event);

        if (is_air == false)
        {
            if (Move_Left != Move_Right)
                changeState(State::Idle, key_event);
            else 
                changeState(State::Run, key_event);
        }
        else if (key_event == EVENT_RANGED_ATTACK_KEY_DOWN)
        {
            //        changeState(State::Idle, key_event); 원거리 공격 상태
            break;
        }
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
        is_air = true;
        break;

    default:
        break;
    }
}

void StateMachine::exitState(State state, int key_event)
{
    sprite_index = 0;
    sprite_frame_value = 0.0f;
}

void StateMachine::doAction(State state, float Elapsed_time)
{
}

int StateMachine::Get_Sprite_Index(float Elapsed_time, int sprite_range, bool index_loop = true)
{
    int draw_index = 0;

    sprite_frame_value += Elapsed_time * 6;

    if (index_loop)
    {
        draw_index = int(sprite_frame_value) % sprite_range;

        if (sprite_frame_value > float(sprite_range))
            sprite_frame_value = 0.0f;
    }
    else
    {
        draw_index = int(sprite_frame_value) % sprite_range;
        if (sprite_frame_value > float(sprite_range))
            draw_index = sprite_range - 1;
    }
    return draw_index;
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
void Naruto_StateMachine::doAction(State state, float ElapsedTime)
{
    switch (state)
    {
    case State::Idle:
         sprite_index = Get_Sprite_Index(ElapsedTime, 6);
        break;

    case State::Run:
    {
        sprite_index = Get_Sprite_Index(ElapsedTime, 6);
        if (Move_Left) // 왼쪽으로 이동
            pos.x -= RUN_SPEED_PPS * ElapsedTime;  
        else if (Move_Right) // 오른쪽으로 이동
            pos.x += RUN_SPEED_PPS * ElapsedTime;  
    }
    break;

    case State::Jump:
    {
        if (is_air)
        {
            if(sprite_index < 4) // 점프 애니메이션은 반복되면 안됨 
                sprite_index = Get_Sprite_Index(ElapsedTime, 4, false);

            pos.y += 1.2 * RUN_SPEED_PPS * ElapsedTime * (2 - sprite_index);

            // 움직이게 될 때
            if (Move_Left != Move_Right)
            {
                if (Move_Left) // 왼쪽으로 이동
                    pos.x -= 0.8f * RUN_SPEED_PPS * ElapsedTime;
                else if (Move_Right) // 오른쪽으로 이동
                    pos.x += 0.8f * RUN_SPEED_PPS * ElapsedTime;
            }
        }

        if (pos.y > Ground_Y)
            is_air = true;
        else if (pos.y <= Ground_Y)
        {
            is_air = false;
            pos.y = float(Ground_Y);
            sprite_index = 0;
        }
    
    }

    break;

    default:
        break;
    }
    Set_Draw_Direction();
}

void Sasuke_StateMachine::doAction(State state, float ElapsedTime)
{
}

void Itachi_StateMachine::doAction(State state, float ElapsedTime)
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

void Player::update(float Elapsed_time)
{
    if (state_machine != NULL)
    {
        state_machine->update(Elapsed_time);
        synchronize_state_machine();
    }
}

void Player::key_update(int key_event)
{
    state_machine->handleEvent(key_event);
}

void Attack::update(float Elapsed_time)
{
    // 위치 이동
}

