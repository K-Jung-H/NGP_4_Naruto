// Collider.h
#pragma once
#include "Object.h"
#include <vector>
#include <memory>

// Bounding Box 구조체 정의
struct BoundingBox
{
    float left;
    float right;
    float top;
    float bottom;
};

class Collider 
{
public:
    static BoundingBox GetBoundingBox(const Player& player);
    static BoundingBox GetBoundingBox(const Attack& attack);
    static bool CheckCollision(const BoundingBox& bb1, const BoundingBox& bb2);
    static void HandleCollision(Player* player, Attack* attack, std::vector<std::shared_ptr<Attack>>& attacks);
};
