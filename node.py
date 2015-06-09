#-*- coding: utf-8 -*-

import math
from extra import *

class Node:
    """Points in space with x,y,z coordinates."""

    def __init__(self, coordinates0, coordinates1, coordinates2, part):
        self.x = coordinates0
        self.y = coordinates1
        self.z = coordinates2
        #part defines part of bolid: body, tire, tire-anchor, spring-connector or road
        self.part = part
        self.speed = -0.5
        self.angle = math.pi/2






