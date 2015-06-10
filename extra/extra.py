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

    def add(self, other):
        return Vector3d(self.x + other.x, self.y + other.y, self.z + other.z)

    #rotation along all axes, math magic
    def rotateX(self, radians):
        y      = self.y
        z      = self.z
        d      = math.hypot(y, z)
        theta  = math.atan2(y, z) + radians
        self.z = d * math.cos(theta)
        self.y = d * math.sin(theta)
        return self

    def rotateY(self, radians):
        x      = self.x
        z      = self.z
        d      = math.hypot(x, z)
        theta  = math.atan2(x, z) + radians
        self.z = d * math.cos(theta)
        self.x = d * math.sin(theta)
        return self

    def rotateZ(self, radians):
        x      = self.x
        y      = self.y
        d      = math.hypot(y, x)
        theta  = math.atan2(y, x) + radians
        self.x = d * math.cos(theta)
        self.y = d * math.sin(theta)
        return self

    def dot(self, second):
        return self.x*second.x + self.y*second.y + self.z*second.z

    def mul(self, scalar):
        return Vector3d(scalar*self.x, scalar*self.y, scalar*self.z)

    def norm(self):
        return math.sqrt(self.x*self.x + self.y*self.y + self.z*self.z)

    def unitVector(self):
        norm = self.norm()
        return Vector3d(self.x/float(norm), self.y/float(norm), self.z/float(norm))

    def cos(self, second):
        numerator = self.dot(second)
        denominator = self.norm() * second.norm()
        return numerator/denominator

    def rotateX(self, radians):
        d      = math.hypot(self.y, self.z)
        theta  = math.atan2(self.y, self.z) + radians
        self.z = d * math.cos(theta)
        self.y = d * math.sin(theta)


    def rotateY(self, radians):
        d      = math.hypot(self.x, self.z)
        theta  = math.atan2(self.x, self.z) + radians
        self.z = d * math.cos(theta)
        self.x = d * math.sin(theta)

    def rotateZ(self, radians):
        d      = math.hypot(self.y, self.x)
        theta  = math.atan2(self.y, self.x) + radians
        self.x = d * math.cos(theta)
        self.y = d * math.sin(theta)

class Point:

    def __init__(self, x, y):
        self.x = x
        self.y = y

def findGroundVectorAfterRotation(C, D):
    F = Point(0,0)
    C = Point(C[0], C[1])
    D = Point(D[0], D[1])

    a = (C.y - D.y)/(C.x - D.x)
    b = C.y - C.x*a

    ap = -a
    bp = D.y - a*D.x

    aq = a
    bq = F.y - aq*F.x

    x = (bq - bp)/(ap - aq)
    y = ap * x + bp

    return (x, y)

