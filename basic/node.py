#-*- coding: utf-8 -*-

from extra.extra import Vector3d

class Node:
    """Points in space with x,y,z coordinates."""

    def __init__(self, coordinates0, coordinates1, coordinates2, part):
        self.x = coordinates0
        self.y = coordinates1
        self.z = coordinates2
        self.x_transformed = self.x
        self.y_transformed = self.y
        self.z_transformed = self.z
        #part defines part of bolid: body, tire, tire-anchor, spring-connector or road
        self.part = part
        self.speedVector = Vector3d(-3.0, 0, 0)
        self.speedVector_transformed = Vector3d(self.speedVector)


    def parpendicularToGroundSpeedVector(self, groundVector):
        scalar = (groundVector.unitVector()).dot(self.speedVector)
        return groundVector.unitVector().mul(scalar)