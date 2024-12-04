#pragma once

struct BoundingBox
{
    bool active = true;

    float left;
    float right;
    float top;
    float bottom;


    BoundingBox() {};
    ~BoundingBox() {};

    bool intersects(BoundingBox* other);
};
