#pragma once

struct BoundingBox
{
    bool active = true;

    float left;
    float right;
    float top;
    float bottom;


    BoundingBox() 
    {
        active = true;
        left = 0;
        right = 0;
        top = 0;
        bottom = 0;
    };
    ~BoundingBox() {};

    bool intersects(BoundingBox* other);
};
