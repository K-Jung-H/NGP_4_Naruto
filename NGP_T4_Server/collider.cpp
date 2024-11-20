#include "Collider.h"
#include <iostream>
#include <algorithm>

// �÷��̾��� Bounding Box ��ȯ �Լ�
BoundingBox Collider::GetBoundingBox(const Player& player)
{
    BoundingBox bb;
    bb.left = player.pos.x - 20;
    bb.right = player.pos.x + 20;
    bb.top = player.pos.y + 40;
    bb.bottom = player.pos.y - 40;
    return bb;
}

// ���� ��ü�� Bounding Box ��ȯ �Լ�
BoundingBox Collider::GetBoundingBox(const Attack& attack) 
{
    BoundingBox bb;
    bb.left = attack.pos.x - 10;
    bb.right = attack.pos.x + 10;
    bb.top = attack.pos.y + 10;
    bb.bottom = attack.pos.y - 10;
    return bb;
}

// Bounding Box �浹 �˻� �Լ�
bool Collider::CheckCollision(const BoundingBox& bb1, const BoundingBox& bb2)
{
    return !(bb1.right < bb2.left || bb1.left > bb2.right ||
        bb1.top < bb2.bottom || bb1.bottom > bb2.top);
}

// �浹 ó�� �Լ�
void Collider::HandleCollision(Player* player, Attack* attack, std::vector<std::shared_ptr<Attack>>& attacks) 
{
    if (attack->attack_type == ATTACK_TYPE_SHURIKEN) 
    {
        player->hp -= attack->damage;
        std::cout << "Player " << player->player_ID << " hit by shuriken. HP: " << player->hp << std::endl;
    }
    else if (attack->attack_type == ATTACK_TYPE_SKILL_1)
    {
        player->hp -= attack->damage * 2;
        std::cout << "Player " << player->player_ID << " hit by Skill 1. HP: " << player->hp << std::endl;
    }
    else if (attack->attack_type == ATTACK_TYPE_SKILL_2)
    {
        player->hp -= attack->damage * 3;
        std::cout << "Player " << player->player_ID << " hit by Skill 2. HP: " << player->hp << std::endl;
    }

    // ���� ��ü ���� (����Ʈ���� ����)
    auto it = std::find_if(attacks.begin(), attacks.end(), [attack](const std::shared_ptr<Attack>& a) { return a.get() == attack; });
    if (it != attacks.end()) 
    {
        attacks.erase(it);
    }
}