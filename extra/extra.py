#-*- coding: utf-8 -*-

import math

def addVectors((angle1, length1), (angle2, length2)):
    """Adds two vectors."""
    x = math.sin(angle1) * length1 + math.sin(angle2) * length2
    y = math.cos(angle1) * length1 + math.cos(angle2) * length2
    length = math.hypot(x, y)
    angle = 0.5 * math.pi - math.atan2(y, x)
    return (angle, length)

class Vector3d:

    def __init__(self, x, y, z):
        self.x = x
        self.y = y
        self.z = z

    def addVectors3d(self, other):
        self.x += other.x
        self.y += other.y
        self.z += other.z

    #rotation along all axes, math magic
    def rotateX(self, radians):
        y      = self.y
        z      = self.z
        d      = math.hypot(y, z)
        theta  = math.atan2(y, z) + radians
        self.z = d * math.cos(theta)
        self.y = d * math.sin(theta)

    def rotateY(self, radians):
        x      = self.x
        z      = self.z
        d      = math.hypot(x, z)
        theta  = math.atan2(x, z) + radians
        self.z = d * math.cos(theta)
        self.x = d * math.sin(theta)

    def rotateZ(self, radians):
        x      = self.x
        y      = self.y
        d      = math.hypot(y, x)
        theta  = math.atan2(y, x) + radians
        self.x = d * math.cos(theta)
        self.y = d * math.sin(theta)

