#-*- coding: utf-8 -*-

import math

def addVectors((angle1, length1), (angle2, length2)):
    """Adds two vectors."""
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)


