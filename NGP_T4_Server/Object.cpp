#include "stdafx.h"
#include "Object.h"
//========================================================
// ���� �ӽ�
void StateMachine::start()
{
    enterState(currentState);
}

void StateMachine::update() {
    // ���� ���¿� ���� ������ ����
    doAction(currentState);
}

void StateMachine::handleEvent(int event)
{
    switch (currentState)
    {
    case State::Idle:
        if (event == 1) { // right_down
            changeState(State::Run);
        }
        else if (event == 2) { // attack_down
            changeState(State::Attack);
        }
        break;

    case State::Run:
        if (event == 0) { // stop
            changeState(State::Idle);
        }
        else if (event == 3) { // jump
            changeState(State::Jump);
        }
        break;

    case State::Jump:
        if (event == 0) { // jump_end
            changeState(State::Idle);
        }
        break;

    case State::Attack:
        if (event == 0) { // attack_end
            changeState(State::Idle);
        }
        break;

      
    }
}

void StateMachine::draw()
{
    // ���� ���¿� ���� �׸���
    drawState(currentState);
}

void StateMachine::changeState(State newState)
{
    exitState(currentState);
    currentState = newState;
    enterState(currentState);
}

void StateMachine::enterState(State state)
{
    switch (state) {
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

void StateMachine::exitState(State state)
{
    // ���� ���� �� ���� ó��
}

void StateMachine::doAction(State state)
{
    switch (state) {
    case State::Idle:
        std::cout << "Doing Idle Action" << std::endl;
        break;
    case State::Run:
        std::cout << "Doing Run Action" << std::endl;
        break;
    case State::Jump:
        std::cout << "Doing Jump Action" << std::endl;
        break;
    case State::Attack:
        std::cout << "Doing Attack Action" << std::endl;
        break;
    }
}

void StateMachine::drawState(State state)
{
    switch (state) {
    case State::Idle:
        std::cout << "Drawing Idle State" << std::endl;
        break;
    case State::Run:
        std::cout << "Drawing Run State" << std::endl;
        break;
    case State::Jump:
        std::cout << "Drawing Jump State" << std::endl;
        break;
    case State::Attack:
        std::cout << "Drawing Attack State" << std::endl;
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

void Player::key_update()
{

    state_machine.update();
}

void Attack::update()
{
    // ��ġ �̵�
}

