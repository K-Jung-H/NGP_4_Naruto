#pragma once
#include "stdafx.h"
#include "Object.h"
#include "Server.h"

void Key_State::update(int key_state)
{
    switch (key_state)
    {
    case EVENT_MOVE_LEFT_KEY_DOWN:
    case EVENT_MOVE_LEFT_KEY_UP:
        left = (key_state % 2 == 1);
        break;
    case EVENT_MOVE_RIGHT_KEY_DOWN:
    case EVENT_MOVE_RIGHT_KEY_UP:
        right = (key_state % 2 == 1);
        break;

    case EVENT_MOVE_UP_KEY_DOWN:
    case EVENT_MOVE_UP_KEY_UP:
        up = (key_state % 2 == 1);
        break;

    case EVENT_MOVE_DOWN_KEY_DOWN:
    case EVENT_MOVE_DOWN_KEY_UP:
        down = (key_state % 2 == 1);
        break;

    default:
        break;
    }
}

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
    // 현재 방향키 눌린 상태 - 텔레포트 방향 정하는 용도
    key_state.update(key_event);

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

        if (key_event == EVENT_NORMAL_ATTACK_KEY_DOWN)
        {
            if (attack_combo)
                combo_stack += 1;

            changeState(State::Attack_Normal, key_event);
        }

        if (key_event == EVENT_RANGED_ATTACK_KEY_DOWN)
            changeState(State::Attack_Shuriken, key_event);

        if (key_event == EVENT_SKILL_ATTACK_1_KEY_DOWN)
            changeState(State::Attack_Skill_1, key_event);

        if (key_event == EVENT_SKILL_ATTACK_2_KEY_DOWN)
            changeState(State::Attack_Skill_2, key_event);

        if (key_event == EVENT_SKILL_TELEPORT_KEY_DOWN)
            changeState(State::Teleport, key_event);
    }
    break;

    case State::Run:
    {
        if (Move_Left == Move_Right)
            changeState(State::Idle, key_event);

        if (key_event == EVENT_MOVE_UP_KEY_DOWN)
            changeState(State::Jump, key_event);

        if (key_event == EVENT_NORMAL_ATTACK_KEY_DOWN)
            changeState(State::Attack_Run, key_event);

        if (key_event == EVENT_RANGED_ATTACK_KEY_DOWN)
            changeState(State::Attack_Shuriken, key_event);

        if (key_event == EVENT_SKILL_ATTACK_1_KEY_DOWN)
            changeState(State::Attack_Skill_1, key_event);

        if (key_event == EVENT_SKILL_ATTACK_2_KEY_DOWN)
            changeState(State::Attack_Skill_2, key_event);

        if (key_event == EVENT_SKILL_TELEPORT_KEY_DOWN)
            changeState(State::Teleport, key_event);
    }
    break;

    case State::Jump:
    {
        if (key_event == EVENT_MOVE_UP_KEY_DOWN)
            changeState(State::Jump, key_event);

        if (key_event == EVENT_NORMAL_ATTACK_KEY_DOWN)
            changeState(State::Attack_Jump, key_event);

        if (is_air == false)
        {
            if (Move_Left != Move_Right)
                changeState(State::Idle, key_event);
            else
                changeState(State::Run, key_event);
        }
        else if (key_event == EVENT_RANGED_ATTACK_KEY_DOWN)
            changeState(State::Attack_Shuriken, key_event);

        if(key_event == EVENT_SKILL_TELEPORT_KEY_DOWN)
            changeState(State::Teleport, key_event);

    }
    break;

    case State::Attack_Normal:
    {
        if (attack_action == false)
            changeState(State::Idle, key_event);
    }
    break;

    case State::Attack_Run:
    {
        if (attack_action == false)
            changeState(State::Run, key_event);

    }
    break;

    case State::Attack_Jump:
    {
        if (attack_action == false)
            changeState(State::Jump, key_event);
    }
    break;

    case State::Attack_Shuriken:
    {
        if (attack_action == false)
        {
            if (is_air == false)
            {
                if (Move_Left != Move_Right)
                    changeState(State::Idle, key_event);
                else
                    changeState(State::Run, key_event);
            }
            else
                changeState(State::Jump, key_event);

        }
    }
    break;

    case State::Attack_Skill_1:
    {
        if (attack_action == false)
            changeState(State::Idle, key_event);
    }
    break;

    case State::Attack_Skill_2:
    {
        if (attack_action == false)
            changeState(State::Idle, key_event);
    }
    break;

    case State::Teleport:
    {
        if (attack_action == false)
            changeState(State::Jump, key_event);
    }
    break;

    default:
        break;
    }
}

void StateMachine::changeState(State newState, int key_event)
{
    lastState = currentState;
    exitState(currentState, key_event);
    currentState = newState;
    enterState(currentState, key_event);
}

void StateMachine::enterState(State state, int key_event)
{
    sprite_index = 0;
    sprite_frame_value = 0.0f;

    switch (state)
    {
    case State::Idle:
        break;
    case State::Run:
        break;
    case State::Jump:
    {
        if (lastState == State::Attack_Shuriken || 
            lastState == State::Attack_Jump || 
            lastState == State::Teleport) // + 공중 공격 + 맞는 상태
        {
            if (Y_Direction)
                sprite_frame_value = 1.0f;
            else
                sprite_frame_value = 2.0f;
        }
        is_air = true;
    }
    break;
         
    case State::Attack_Normal:
    {
        attack_action = true;
        attack_combo = true;

        if (combo_stack == 0 || combo_stack == 5)
            combo_stack = 1;
    }
    break;

    case State::Attack_Run:
        attack_action = true;
        break;

    case State::Attack_Jump:
        attack_action = true;
        break;

    case State::Attack_Shuriken:
        attack_action = true;
        break;

    case State::Attack_Skill_1:
        attack_action = true;
    break;

    case State::Attack_Skill_2:
        attack_action = true;
    break;

    case State::Teleport:
        attack_action = true;
        break;


    default:
        break;
    }
}

void StateMachine::exitState(State state, int key_event)
{
    sprite_index = 0;
    sprite_frame_value = 0.0f;

    switch (state)
    {
    case State::Idle:
        break;
    case State::Run:
        break;
    case State::Jump:
        break;
    case State::Attack_Normal:
        attack_after_time = 0.0f;
        break;

    default:
        break;
    }
}

void StateMachine::doAction(State state, float Elapsed_time)
{
}

int StateMachine::Get_Sprite_Index(float Elapsed_time, int sprite_range, bool index_loop = true)
{
    int draw_index = 0;

    sprite_frame_value += Elapsed_time;

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
        return (STATE_ATTACK_NORMAL_1 + (combo_stack - 1));
        break;

    case State::Attack_Jump:
        return STATE_ATTACK_JUMP;
        break;

    case State::Attack_Run:
        return STATE_ATTACK_RUN;
        break;

    case State::Attack_Shuriken:
        return STATE_ATTACK_SKILL_1;
        break;
    case State::Attack_Skill_1:
        return STATE_ATTACK_SKILL_2;
        break;
    case State::Attack_Skill_2:
        return STATE_ATTACK_SKILL_3;
        break;

    case State::Teleport:
        return STATE_TELEPORT;
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
    {
        sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 6);
    }
    break;

    case State::Run:
    {
        sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 6);
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
                sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 4, false);

            if (sprite_index < 2)
                Y_Direction = true; // 상승
            else
                Y_Direction = false; // 하강

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

    case State::Attack_Normal:
    {
        // 공격 애니메이션은 0~3까지 있음, 4가 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);

        // 한대 때리는 애니메이션 끝나면
        if (sprite_index == 4)
        {
            sprite_index = 3;
            attack_action = false;
        }

    }
    break;

    case State::Attack_Run: // 5
    {
        if (Move_Left) // 왼쪽으로 이동
            pos.x -= 0.4f * RUN_SPEED_PPS * ElapsedTime;
        else if (Move_Right) // 오른쪽으로 이동
            pos.x += 0.4f * RUN_SPEED_PPS * ElapsedTime;

        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 6, false);

        if (sprite_index == 5)
        {
            sprite_index = 4;
            attack_action = false;
        }
    }
    break;

    case State::Attack_Jump: // 4
    {
        // 움직이게 될 때
        if (Y_Direction)
            pos.y += 0.05f * RUN_SPEED_PPS * ElapsedTime;
        else
            pos.y -= 0.05f * RUN_SPEED_PPS * ElapsedTime;

        if (Move_Left != Move_Right)
        {
            if (Move_Left) // 왼쪽으로 이동
                pos.x -= 0.1f * RUN_SPEED_PPS * ElapsedTime;
            else if (Move_Right) // 오른쪽으로 이동
                pos.x += 0.1f * RUN_SPEED_PPS * ElapsedTime;
        }

        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);

        if (sprite_index == 4)
        {
            sprite_index = 4;
            attack_action = false;
        }
    }
    break;

    case State::Attack_Shuriken:
    {
        static bool shuriken_triggered = false;

        if (is_air)
        {
            pos.y += (Y_Direction ? 1 : -1) * 0.5 * RUN_SPEED_PPS * ElapsedTime;

            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 4, false); // 스프라이트 0~2 까지 있음, 3이 되면 종료하도록
            
            if (sprite_index == 1 && shuriken_triggered == false)
            {
                shuriken_triggered = true;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_NARUTO, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);
            }
            if (sprite_index == 3)
            {
                sprite_index = 2;
                attack_action = false;
            }
        }
        else
        {
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 6, false); // 스프라이트 0~4 까지 있음, 5가 되면 종료하도록
            if (sprite_index == 2 && shuriken_triggered == false)
            {
                shuriken_triggered = true;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_NARUTO, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);
            }
            if (sprite_index == 5)
            {
                sprite_index = 4;
                attack_action = false;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_NARUTO, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);
            }
        }
    }
    break;

    case State::Attack_Skill_1:
    {
        static bool skill_1_triggered = false;

        // 스킬 애니메이션은 0~10까지 있음, 11이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 12, false);

        if (sprite_index == 8 && skill_1_triggered == false)
        {
            Object* skill_1_obj = new Attack(player_ID, CHARACTER_NARUTO, ATTACK_TYPE_SKILL_1, pos, X_Direction);
            server_ptr->Add_Skill_Object(skill_1_obj);
            skill_1_triggered = true;
        }

        // 스킬 애니메이션 끝나면
        if (sprite_index == 11)
        {
            sprite_index = 10;
            attack_action = false;
            skill_1_triggered = false;

        }
    }
    break;

    case State::Attack_Skill_2:
    {
        static bool skill_2_triggered = false;

        // 스킬 애니메이션은 0~5까지 있음, 6이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 7, false);

        if (sprite_index == 2 && skill_2_triggered == false)
        {
            Object* skill_2_obj = new Attack(player_ID, CHARACTER_NARUTO, ATTACK_TYPE_SKILL_2, pos, X_Direction);
            server_ptr->Add_Skill_Object(skill_2_obj);
            skill_2_triggered = true;
        }

        // 스킬 애니메이션 끝나면
        if (sprite_index == 6)
        {
            sprite_index = 5;
            attack_action = false;
            skill_2_triggered = false;

        }
    }
    break;

    case State::Teleport:
    {
        static bool teleport_triggered = false;

        // 스킬 애니메이션은 0~3까지 있음, 4이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);

        if (sprite_index == 2 && teleport_triggered == false)
        {
            pos.x += (!key_state.left && key_state.right) ? 200.0f : (key_state.left && !key_state.right) ? -200.0f : 0;
            pos.y += (!key_state.up && key_state.down) ? -200.0f : (key_state.up && !key_state.down) ? 200.0f : 0;

            if (pos.y < 120.0f)
                pos.y = 120.0f;

            teleport_triggered = true;
        }

        if (sprite_index == 4)
        {
            sprite_index = 3;
            attack_action = false;
            teleport_triggered = false;
        }

    }
    break;
    default:
        break;
    }

    // 공격이 끝나고 1초 이상 공격을 재입력 안하면
    if (attack_combo)
    {
        if (attack_after_time > Player_Attack_Combo_Time_Limit)
        {
            attack_combo = false;
            attack_after_time = 0.0f;
            combo_stack = 0;
        }
        else
            attack_after_time += ElapsedTime;
    }


    Set_Draw_Direction();
}

void Sasuke_StateMachine::doAction(State state, float ElapsedTime)
{
    switch (state)
    {
    case State::Idle:
    {
        sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 6);
    }
    break;

    case State::Run:
    {
        sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 6);
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
            if (sprite_index < 4) // 점프 애니메이션은 반복되면 안됨 
                sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 4, false);

            if (sprite_index < 2)
                Y_Direction = true; // 상승
            else
                Y_Direction = false; // 하강

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

    case State::Attack_Normal:
    {
        // 공격 애니메이션은 4, 5, 7, 6
        if (combo_stack == 1)
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);
        else if (combo_stack == 2)
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 6, false);
        else if (combo_stack == 3)
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 8, false);
        else if (combo_stack == 4)
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 7, false);
        else
            sprite_index = 0;

        // 한대 때리는 애니메이션 끝나면
        if (combo_stack == 1 && sprite_index == 4)
        {
            sprite_index = 3;
            attack_action = false;
        }
        else if (combo_stack == 2 && sprite_index == 5)
        {
            sprite_index = 4;
            attack_action = false;
        }
        else if (combo_stack == 3 && sprite_index == 7)
        {
            sprite_index = 6;
            attack_action = false;
        }
        else if (combo_stack == 4 && sprite_index == 6)
        {
            sprite_index = 5;
            attack_action = false;
        }

    }
    break;

    case State::Attack_Run: // 5
    {
        if (Move_Left) // 왼쪽으로 이동
            pos.x -= 0.4f * RUN_SPEED_PPS * ElapsedTime;
        else if (Move_Right) // 오른쪽으로 이동
            pos.x += 0.4f * RUN_SPEED_PPS * ElapsedTime;

        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 7, false);

        if (sprite_index == 6)
        {
            sprite_index = 5;
            attack_action = false;
        }
    }
    break;

    case State::Attack_Jump: // 5
    {
        // 움직이게 될 때
        if (Y_Direction)
            pos.y += 0.05f * RUN_SPEED_PPS * ElapsedTime;
        else
            pos.y -= 0.05f * RUN_SPEED_PPS * ElapsedTime;

        if (Move_Left != Move_Right)
        {
            if (Move_Left) // 왼쪽으로 이동
                pos.x -= 0.1f * RUN_SPEED_PPS * ElapsedTime;
            else if (Move_Right) // 오른쪽으로 이동
                pos.x += 0.1f * RUN_SPEED_PPS * ElapsedTime;
        }

        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 6, false);

        if (sprite_index == 5)
        {
            sprite_index = 4;
            attack_action = false;
        }
    }
    break;

    case State::Attack_Shuriken:
    {
        static bool shuriken_triggered = false;
        if (is_air)
        {
            pos.y += (Y_Direction ? 1 : -1) * 0.5 * RUN_SPEED_PPS * ElapsedTime;

            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false); // 스프라이트 0~3 까지 있음, 4이 되면 종료하도록
            
            if (sprite_index == 3 && shuriken_triggered == false)
            {
                shuriken_triggered = true;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_SASUKE, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);

            }
            if (sprite_index == 4)
            {
                sprite_index = 3;
                attack_action = false;
                shuriken_triggered = false;
            }
        }
        else
        {
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false); // 스프라이트 0~3 까지 있음, 4가 되면 종료하도록
            
            if (sprite_index == 3 && shuriken_triggered == false)
            {
                shuriken_triggered = true;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_SASUKE, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);
            }
            if (sprite_index == 4)
            {
                sprite_index = 3;
                attack_action = false;
                shuriken_triggered = false;
            }
        }
    }
    break;

    case State::Attack_Skill_1: // 사스케 0 ~ 18, 치도리 0 ~ 17
    {
        static bool skill_1_triggered = false;

        // 스킬 애니메이션은 0~18까지 있음, 19이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 20, false);


        if (sprite_index == 1 && skill_1_triggered == false)
        {
            Object* skill_1_obj = new Attack(player_ID, CHARACTER_SASUKE, ATTACK_TYPE_SKILL_2, pos, X_Direction);
            server_ptr->Add_Skill_Object(skill_1_obj);
            skill_1_triggered = true;
        }

        // 스킬 애니메이션 끝나면
        if (sprite_index == 19)
        {
            sprite_index = 18;
            attack_action = false;
            skill_1_triggered = false;
        }

        if (7 < sprite_index && sprite_index < 18)
        {
            if (X_Direction == false) // 왼쪽으로 이동
                pos.x -= RUN_SPEED_PPS * ElapsedTime;
            else if (X_Direction) // 오른쪽으로 이동
                pos.x += RUN_SPEED_PPS * ElapsedTime;
        }
    }
    break;

    case State::Attack_Skill_2: 
    {
        static bool skill_2_triggered = false;

        // 스킬 애니메이션은 0~11까지 있음, 12이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 20, false);

        // 스킬 애니메이션 끝나면
        if (sprite_index == 19)
        {
            sprite_index = 11;
            attack_action = false;
            skill_2_triggered = false;
        }
        else if (sprite_index > 11)
        {
            sprite_index = 11;
        }

        if (sprite_index == 9 && skill_2_triggered == false)
        {
            sprite_frame_value += 1.0f;

            Position skill_2_spawn_pos;
            skill_2_spawn_pos.x = pos.x + (X_Direction * 2 - 1) * 180.0f;
            skill_2_spawn_pos.y = pos.y - 30;

            Object* skill_2_obj = new Attack(player_ID, CHARACTER_SASUKE, ATTACK_TYPE_SKILL_1, skill_2_spawn_pos, X_Direction);
            server_ptr->Add_Skill_Object(skill_2_obj);
            skill_2_triggered = true;
        }
    }
    break;

    case State::Teleport:
    {
        static bool teleport_triggered = false;

        // 스킬 애니메이션은 0~2까지 있음, 3이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 4, false);

        if (sprite_index == 1 && teleport_triggered == false)
        {
            pos.x += (!key_state.left && key_state.right) ? 200.0f : (key_state.left && !key_state.right) ? -200.0f : 0;
            pos.y += (!key_state.up && key_state.down) ? -200.0f : (key_state.up && !key_state.down) ? 200.0f : 0;

            if (pos.y < 120.0f)
                pos.y = 120.0f;

            teleport_triggered = true;
        }

        if (sprite_index == 3)
        {
            sprite_index = 2;
            attack_action = false;
            teleport_triggered = false;
        }

    }
    break;

    default:
        break;
    }

    // 공격이 끝나고 1초 이상 공격을 재입력 안하면
    if (attack_combo)
    {
        if (attack_after_time > Player_Attack_Combo_Time_Limit)
        {
            attack_combo = false;
            attack_after_time = 0.0f;
            combo_stack = 0;
        }
        else
            attack_after_time += ElapsedTime;
    }

    Set_Draw_Direction();
}

void Itachi_StateMachine::doAction(State state, float ElapsedTime)
{
    switch (state)
    {
    case State::Idle:
    {
        sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 4);
    }
    break;

    case State::Run:
    {
        sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 6);
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
            if (sprite_index < 4) // 점프 애니메이션은 반복되면 안됨 
                sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 4, false);

            if (sprite_index < 2)
                Y_Direction = true; // 상승
            else
                Y_Direction = false; // 하강

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

    case State::Attack_Normal:
    {
        // 공격 애니메이션은 4, 4, 5, 6
        if (combo_stack == 1)
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);
        else if (combo_stack == 2)
            sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);
        else if (combo_stack == 3)
            sprite_index = Get_Sprite_Index(ElapsedTime * 18.0f, 6, false);
        else if (combo_stack == 4)
            sprite_index = Get_Sprite_Index(ElapsedTime * 18.0f, 7, false);
        else
            sprite_index = 0;

        // 한대 때리는 애니메이션 끝나면
        if (combo_stack == 1 && sprite_index == 4)
        {
            sprite_index = 3;
            attack_action = false;
        }
        else if (combo_stack == 2 && sprite_index == 4)
        {
            sprite_index = 3;
            attack_action = false;
        }
        else if (combo_stack == 3 && sprite_index == 5)
        {
            sprite_index = 4;
            attack_action = false;
        }
        else if (combo_stack == 4 && sprite_index == 6)
        {
            sprite_index = 5;
            attack_action = false;
        }

    }
    break;

    case State::Attack_Run: // 5
    {
        if (Move_Left) // 왼쪽으로 이동
            pos.x -= 0.4f * RUN_SPEED_PPS * ElapsedTime;
        else if (Move_Right) // 오른쪽으로 이동
            pos.x += 0.4f * RUN_SPEED_PPS * ElapsedTime;

        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 6, false);

        if (sprite_index == 5)
        {
            sprite_index = 4;
            attack_action = false;
        }
    }
    break;

    case State::Attack_Jump: // 3
    {
        // 움직이게 될 때
        if (Y_Direction)
            pos.y += 0.05f * RUN_SPEED_PPS * ElapsedTime;
        else
            pos.y -= 0.05f * RUN_SPEED_PPS * ElapsedTime;

        if (Move_Left != Move_Right)
        {
            if (Move_Left) // 왼쪽으로 이동
                pos.x -= 0.1f * RUN_SPEED_PPS * ElapsedTime;
            else if (Move_Right) // 오른쪽으로 이동
                pos.x += 0.1f * RUN_SPEED_PPS * ElapsedTime;
        }

        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 4, false);

        if (sprite_index == 3)
        {
            sprite_index = 2;
            attack_action = false;
        }
    }
    break;

    case State::Attack_Shuriken:
    {
        static bool shuriken_triggered = false;

        if (is_air)
        {
            pos.y += (Y_Direction ? 1 : -1) * 0.5 * RUN_SPEED_PPS * ElapsedTime;

            sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 3, false); // 스프라이트 0~1 까지 있음, 2이 되면 종료하도록

            if (sprite_index == 1 && shuriken_triggered == false)
            {
                shuriken_triggered = true;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_ITACHI, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);
            }
            if (sprite_index == 2)
            {
                sprite_index = 1;
                attack_action = false;
            }
        }
        else
        {
            sprite_index = Get_Sprite_Index(ElapsedTime * 6.0f, 4, false); // 스프라이트 0~2 까지 있음, 3가 되면 종료하도록
            if (sprite_index == 2 && shuriken_triggered == false)
            {
                shuriken_triggered = true;

                Object* shuriken_obj = new Attack(player_ID, CHARACTER_ITACHI, ATTACK_TYPE_SHURIKEN, pos, X_Direction);
                server_ptr->Add_Skill_Object(shuriken_obj);
            }
            if (sprite_index == 3)
            {
                sprite_index = 2;
                attack_action = false;
            }
        }
    }
    break;

    case State::Attack_Skill_1: // 사스케 0 ~ 18, 치도리 0 ~ 17
    {
        static bool skill_1_triggered = false;

        // 스킬 애니메이션은 0~18까지 있음, 19이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 20, false);


        if (sprite_index == 1 && skill_1_triggered == false)
        {
            Object* skill_1_obj = new Attack(player_ID, CHARACTER_ITACHI, ATTACK_TYPE_SKILL_2, pos, X_Direction);
            server_ptr->Add_Skill_Object(skill_1_obj);
            skill_1_triggered = true;
        }

        // 스킬 애니메이션 끝나면
        if (sprite_index == 19)
        {
            sprite_index = 18;
            attack_action = false;
            skill_1_triggered = false;
        }

        if (7 < sprite_index && sprite_index < 18)
        {
            if (X_Direction == false) // 왼쪽으로 이동
                pos.x -= RUN_SPEED_PPS * ElapsedTime;
            else if (X_Direction) // 오른쪽으로 이동
                pos.x += RUN_SPEED_PPS * ElapsedTime;
        }
    }
    break;

    case State::Attack_Skill_2:
    {
        static bool skill_2_triggered = false;

        // 스킬 애니메이션은 0~11까지 있음, 12이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 20, false);

        // 스킬 애니메이션 끝나면
        if (sprite_index == 19)
        {
            sprite_index = 11;
            attack_action = false;
            skill_2_triggered = false;
        }
        else if (sprite_index > 8)
        {
            sprite_index = (sprite_index % 2) + 7;
        }

        if (sprite_index == 7 && skill_2_triggered == false)
        {
            sprite_frame_value += 1.0f;

            Position skill_2_spawn_pos;
            skill_2_spawn_pos.x = pos.x + (X_Direction * 2 - 1) * 180.0f;
            skill_2_spawn_pos.y = pos.y;

            Object* skill_2_obj = new Attack(player_ID, CHARACTER_SASUKE, ATTACK_TYPE_SKILL_1, skill_2_spawn_pos, X_Direction);
            server_ptr->Add_Skill_Object(skill_2_obj);
            skill_2_triggered = true;
        }
    }
    break;

    case State::Teleport:
    {
        static bool teleport_triggered = false;

        // 스킬 애니메이션은 0~3까지 있음, 4이 되면 종료하기
        sprite_index = Get_Sprite_Index(ElapsedTime * 12.0f, 5, false);

        if (sprite_index == 2 && teleport_triggered == false)
        {
            pos.x += (!key_state.left && key_state.right) ? 200.0f : (key_state.left && !key_state.right) ? -200.0f : 0;
            pos.y += (!key_state.up && key_state.down) ? -200.0f : (key_state.up && !key_state.down) ? 200.0f : 0;

            if (pos.y < 120.0f)
                pos.y = 120.0f;

            teleport_triggered = true;
        }

        if (sprite_index == 4)
        {
            sprite_index = 3;
            attack_action = false;
            teleport_triggered = false;
        }

    }
    break;
    default:
        break;
    }

    // 공격이 끝나고 1초 이상 공격을 재입력 안하면
    if (attack_combo)
    {
        if (attack_after_time > Player_Attack_Combo_Time_Limit)
        {
            attack_combo = false;
            attack_after_time = 0.0f;
            combo_stack = 0;
        }
        else
            attack_after_time += ElapsedTime;
    }


    Set_Draw_Direction();
}
//========================================================

void Player::Set_Character(int n, Server* server_ptr)
{
    selected_character_type = n;

    if (n == CHARACTER_NARUTO)
        state_machine = new Naruto_StateMachine();
    else if (n == CHARACTER_SASUKE)
        state_machine = new Sasuke_StateMachine();
    else if (n == CHARACTER_ITACHI)
        state_machine = new Itachi_StateMachine();

    if (state_machine != NULL)
    {
        state_machine->Set_Server(server_ptr);
        std::copy(this->player_ID, this->player_ID + 32, state_machine->player_ID);
    }
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

void Player::Print_info()
{
    int pos_x = this->pos.x;
    int pos_y = this->pos.y;

    std::string direction = "";
    if (this->X_Direction == false)
        direction = "left";
    else
        direction = "right";

    int sprite_index = this->sprite_index;
    std::string state = "";

    switch (this->state)
    {
    case 0:
        state = "STATE_IDLE";
        break;
    case 1:
        state = "STATE_RUN";
        break;
    case 2:
        state = "STATE_JUMP";
        break;
    case 3:
        state = "STATE_ATTACK_NORMAL_1";
        break;
    case 4:
        state = "STATE_ATTACK_NORMAL_2";
        break;
    case 5:
        state = "STATE_ATTACK_NORMAL_3";
        break;
    case 6:
        state = "STATE_ATTACK_NORMAL_4";
        break;
    case 7:
        state = "STATE_ATTACK_SHURIKEN";
        break;
    case 8:
        state = "STATE_ATTACK_SKILL_1";
        break;
    case 9:
        state = "STATE_ATTACK_SKILL_2";
        break;
    default:
        break;
    }

    std::cout << "pos x: " << pos_x << ", pos y: " << pos_y << ", " "Direction: " << direction
        << ", " << "State: " << state << ", " << "Sprite_index: " << sprite_index << std::endl;
}

int Attack::Get_Sprite_Index(float Elapsed_time, int sprite_range, bool index_loop = true)
{
    int draw_index = 0;

    sprite_frame_value += Elapsed_time;

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

// selected_character_type 1. 나루토, 2. 사스케, 3.이타치
// attack_type 1. 수리검
// attack_type 2. 나선환 / 화둔 / 화둔
// attack_type 3. 구미 / 치도리 / 아마테라스

void Attack::update(float Elapsed_time)
{
    switch (attack_type)
    {
    case 1:     // 수리검
        sprite_index = Get_Sprite_Index(Elapsed_time * 6.0f, 4);
        pos.x += (X_Direction * 2 - 1) * RUN_SPEED_PPS * Elapsed_time;
        break;
    
    case 2:     // 스킬 1      
        switch (selected_character_type)
        {
        case 1: // Naruto - 나선환
        {
            if (sprite_index < 5)
            {
                sprite_index = Get_Sprite_Index(Elapsed_time * 6.0f, 6, false); // 0, 1, 2, 3, 4
                pos.x += (X_Direction * 2 - 1) * Elapsed_time * sprite_index * RUN_SPEED_PPS / 5;
            }
            else if (sprite_index >= 5)
            {
                // 인덱스 범위 바꿀때, 기존 값 초기화
                if (sprite_frame_value >= 5.0f)
                    sprite_frame_value = 0.0f;

                sprite_index = Get_Sprite_Index(Elapsed_time * 6.0f, 4) + 5; // 5, 6, 7, 8
                pos.x += (X_Direction * 2 - 1) * RUN_SPEED_PPS * Elapsed_time;
            }
        }
        break;

        case 2: // Sasuke - 화둔
        case 3: // Itachi - 화둔
        {
            if (sprite_index < 5)
                sprite_index = Get_Sprite_Index(Elapsed_time * 6.0f, 6, false); // 0, 1, 2, 3, 4
            else if (sprite_index >= 5)
            {
                // 인덱스 범위 바꿀때, 기존 값 초기화
                if (sprite_frame_value >= 5.0f)
                    sprite_frame_value = 0.0f;

                sprite_index = Get_Sprite_Index(Elapsed_time * 6.0f, 5) + 5; // 5, 6, 7, 8, 9
                pos.x += (X_Direction * 2 - 1) * RUN_SPEED_PPS * Elapsed_time;
            }
        }
        break;
        }
        break;

    case 3:     // 스킬 2
        switch (selected_character_type)
        {
        case 1: // Naruto - 구미
        {// 제자리
            sprite_index = Get_Sprite_Index(Elapsed_time * 20.0f, 11, false);

            if (sprite_index == 10)
            {
                sprite_index = 9;
                life = false;
            }
        }
        break;

        case 2: // Sasuke - 치도리
        {
            // 스킬 애니메이션은 0~17까지 있음, 18이 되면 종료
            sprite_index = Get_Sprite_Index(Elapsed_time * 12.0f, 19, false);

            if (sprite_index == 18)
            {
                sprite_index = 17;
                life = false;
            }

            // 전진
            if(sprite_index > 6)
                pos.x += (X_Direction * 2 - 1) * RUN_SPEED_PPS * Elapsed_time;
        }
        break;

        case 3: // Itachi - 아마테라스
            // 따라가기
            break;
        }
        break;
    }

    if ((Ground_X_Min - 50) > pos.x || pos.x > (Ground_X_Max + 50))
        life = false;
}

void Attack::Print_info()
{
    int pos_x = this->pos.x;
    int pos_y = this->pos.y;

    std::string direction = "";
    if (this->X_Direction == false)
        direction = "left";
    else
        direction = "right";

    int sprite_index = this->sprite_index;

    int n = selected_character_type;
    int m = attack_type;
    int value = n * 10 + m;

    std::string attack_name = "";
    switch (value)
    {
    case 11:
        attack_name = "나루토 수리검";
        break;
    case 12:
        attack_name = "나루토 스킬 1";
        break;
    case 13:
        attack_name = "나루토 스킬 2";
        break;
    case 21:
        attack_name = "사스케 수리검";
        break;
    case 22:
        attack_name = "사스케 스킬 1";
        break;
    case 23:
        attack_name = "사스케 스킬 2";
        break;
    case 31:
        attack_name = "이타치 수리검";
        break;
    case 32:
        attack_name = "이타치 스킬 1";
        break;
    case 33:
        attack_name = "이타치 스킬 2";
        break;
    }

    std::cout << "pos x: " << pos_x << ", pos y: " << pos_y << ", " "Direction: " << direction
        << ", " << "Type: " << attack_name << ", " << "Sprite_index: " << sprite_index << std::endl;
}