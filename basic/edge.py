#-*- coding: utf-8 -*-

import math

class Edge:
    """Edges starting and stopping with node. k is redundant atm """

    def __init__(self, start, stop, k):
        self.start = start
        self.stop = stop
        self.length = math.sqrt(math.pow(start.x - stop.x, 2) + math.pow(start.y - stop.y, 2) + math.pow(start.z - stop.z, 2))
        self.k = k

