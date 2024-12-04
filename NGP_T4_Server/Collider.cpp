#pragma once
#include "stdafx.h"
#include "Collider.h"

bool BoundingBox::intersects(BoundingBox* other)
{
    if (this->active && other->active)
        return !(right < other->left || left > other->right || bottom > other->top || top < other->bottom);

    return false;
}