#include "stdafx.h"
#include "Object.h"
//========================================================
// ���� �ӽ�
void StateMachine::start()
{
    enterState(currentState, 0);
}

void StateMachine::update() 
{
    // ���� ���¿� ���� ������ ����
    doAction(currentState);

    if (currentState == State::Jump)
    {
        Sleep(1000);
        changeState(State::Idle, EVENT_NONE);
    }
}

void StateMachine::handleEvent(int key_event)
{
    switch (currentState)
    {
    case State::Idle:
        if (key_event == EVENT_MOVE_LEFT_KEY_DOWN || key_event == EVENT_MOVE_RIGHT_KEY_DOWN)
        { 
            changeState(State::Run, key_event);
        }
        else if (key_event == EVENT_MOVE_UP_KEY_DOWN)
        {
            changeState(State::Jump, key_event);
        }
        break;

        break;

    case State::Run:
        if (key_event == EVENT_MOVE_LEFT_KEY_UP || key_event == EVENT_MOVE_RIGHT_KEY_UP)
        { 
            changeState(State::Idle, key_event);
        }
        else if (key_event == EVENT_MOVE_UP_KEY_DOWN)
        { 
            changeState(State::Jump, key_event);
        }
        break;

    case State::Jump:
        if (key_event == 0) 
        {
        }
        break;

    case State::Attack:
        if (key_event == 0) 
        { 
            changeState(State::Idle, key_event);
        }
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
    if (key_event == EVENT_MOVE_LEFT_KEY_DOWN)
        X_Direction = LEFT;
    else if(key_event == EVENT_MOVE_RIGHT_KEY_DOWN)
        X_Direction = RIGHT;

    switch (state)
    {
    case State::Idle:
        std::cout << "Entering Idle State" << std::endl;
        break;
    case State::Run:
        std::cout << "Entering Run State" << std::endl;
        break;
    case State::Jump:
        std::cout << "Entering Jump State" << std::endl;
        break;
    case State::Attack:
        std::cout << "Entering Attack State" << std::endl;
        break;
    }
}

void StateMachine::exitState(State state, int key_event)
{
    // ���� ���� �� ���� ó��
}

void StateMachine::doAction(State state)
{
    switch (state)
    {
    case State::Idle:
        std::cout << "Doing Idle Action" << std::endl;
        break;
    case State::Run:
        std::cout << "Doing Run Action";
        if (X_Direction == LEFT)
            std::cout << " - Left" << std::endl;
        else
            std::cout << " - Right" << std::endl;
        break;
    case State::Jump:
        std::cout << "Doing Jump Action" << std::endl;
        break;
    case State::Attack:
        std::cout << "Doing Attack Action" << std::endl;
        break;
    }
}

//========================================================

void Player::update()
{
    state_machine.update();
    // ���¿� ���� ������Ʈ 
    // Ű �˻� �켱�ϱ�
}

void Player::key_update(int key_event)
{
    state_machine.handleEvent(key_event);
}

void Attack::update()
{
    // ��ġ �̵�
}

