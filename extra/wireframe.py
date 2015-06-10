#-*- coding: utf-8 -*-

from basic.node import Node
from basic.edge import Edge
from extra import addVectors, Vector3d
from construction.construction import roadFun
import math
import time


class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.springs = []
        self.ground = False
        #gravity
        self.gravityVector = Vector3d(0, 0.01, 0)
        #spring
        self.response = 2.0
        self.k = 0.005
        self.springForceVector = Vector3d(0,0,0)
        #absorber
        self.beta = 0.05
        self.absorberForceVector = Vector3d(0,0,0)
        #gravity, spring, absorber: constants to be determined!

        #defined as variable height in construction.py
        self.springLength = 80
        #ground is determined from the top of the screen
        self.groundLvl = 360 # TODO deprecated
        self.groundVector = Vector3d(0, self.groundLvl, 0)
        self.roadFun = roadFun

    #adding wireframe elements
    def addNodes(self, nodeList):
        for node in nodeList:
            self.nodes.append(Node(node[0], node[1], node[2], node[3]))

    def addEdges(self, edgeList):
        for (start, stop, k) in edgeList:
            self.edges.append(Edge(self.nodes[start], self.nodes[stop], k))

    def addSpring(self, start, stop, k=1):
        self.springs.append(Edge(self.nodes[start], self.nodes[stop], k))

    #printing wireframe elements
    def outputNodes(self):
        print "\n --- Nodes --- "
        for i, node in enumerate(self.nodes):
            print " %d: (%.2f, %.2f, %.2f)" % (i, node.x, node.y, node.z)

    def outputEdges(self):
        print "\n --- Edges --- "
        for i, edge in enumerate(self.edges):
            print " %d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z),
            print "to (%.2f, %.2f, %.2f)" % (edge.stop.x,  edge.stop.y,  edge.stop.z)

    def outputSprings(self):
        print "\n --- Springs --- "
        for i, edge in enumerate(self.springs):
            print " %d: (%.2f, %.2f, %.2f)" % (i, edge.start.x, edge.start.y, edge.start.z),
            print "to (%.2f, %.2f, %.2f)" % (edge.stop.x,  edge.stop.y,  edge.stop.z)


    def translate(self, axis, d):
        """ Add constant 'd' to the coordinate 'axis' of each node of a wireframe """

        if axis in ['x', 'y', 'z']:
            for node in self.nodes:
                setattr(node, axis, getattr(node, axis) + d)

    def translate3d(self, vector):

        for node in self.nodes:
            node.x += vector.x
            node.y += vector.y
            node.z += vector.z

    # def scale(self, (centre_x, centre_y), scale):
    #     """ Scale the wireframe from the centre of the screen """
    #     # TODO
    #
    #     # for node in self.nodes:
    #     #     node.x = centre_x + scale * (node.x - centre_x)
    #     #     node.y = centre_y + scale * (node.y - centre_y)
    #     #     node.z *= scale
    #     #     node.speed *= scale
    #     # self.ground = centre_y + scale * (self.ground - centre_y)

    def findCentre(self):
        """ Find the centre of the wireframe. """

        num_nodes = len(self.nodes)
        meanX = sum([node.x for node in self.nodes]) / num_nodes
        meanY = sum([node.y for node in self.nodes]) / num_nodes
        meanZ = sum([node.z for node in self.nodes]) / num_nodes

        return (meanX, meanY, meanZ)

    #rotation along all axes, math magic
    def rotateX(self, (cx,cy,cz), radians):
        for node in self.nodes:
            y      = node.y - cy
            z      = node.z - cz
            d      = math.hypot(y, z)
            theta  = math.atan2(y, z) + radians
            node.z_transformed = cz + d * math.cos(theta)
            node.y_transformed = cy + d * math.sin(theta)


    def rotateY(self, (cx,cy,cz), radians):
        for node in self.nodes:
            x      = node.x - cx
            z      = node.z - cz
            d      = math.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node.z_transformed = cz + d * math.cos(theta)
            node.x_transformed = cx + d * math.sin(theta)

    def rotateZ(self, (cx,cy,cz), radians):
        for node in self.nodes:
            x      = node.x_transformed - cx
            y      = node.y_transformed - cy
            d      = math.hypot(y, x)
            theta  = math.atan2(y, x) + radians
            node.x_transformed = cx + d * math.cos(theta)
            node.y_transformed = cy + d * math.sin(theta)

    def checkGround(self): #TODO obrót
        """Checks if any node is touching ground y = 320"""

        self.ground = False

        for node in self.nodes:
            if self.roadFun(node.x) <= node.y and node.part=='tire':
                self.ground = True
                break



    def checkSprings(self):
        #checks only one spring, cause the rest is the same
        edge = self.springs[0]
        length = math.sqrt(math.pow(edge.start.x - edge.stop.x, 2) + math.pow(edge.start.y - edge.stop.y, 2) +
                           math.pow(edge.start.z - edge.stop.z, 2))
        # spring F = -kx
        forceLength = self.springLength-length
        self.springForceVector = Vector3d(edge.start.x - edge.stop.x, edge.start.y - edge.stop.y, edge.start.z - edge.stop.z).unitVector().mul(forceLength).mul(self.k)

        #going down, absorber F = beta*v

        diffSpeed = edge.start.speedVector.mul(-1).add(edge.stop.speedVector)

        self.absorberForceVector = diffSpeed.mul(self.beta)

    def _hitedGroundSpeed(self, groundVector, speedVector):
        scalar = -2 * (groundVector.unitVector()).dot(speedVector)
        return (groundVector.unitVector()).mul(scalar).add(speedVector)


    def move(self):
        #evaluates position in (x,y) of every node
        for node in self.nodes:
            #gravity
            node.speedVector = node.speedVector.add(self.gravityVector)
            #bouncing off the ground for tires and suspension
            if self.ground == True and node.part != 'body':
                pass
                node.speedVector = self._hitedGroundSpeed(self.groundVector, node.speedVector)
            if node.part == 'body':
                # adds spring and absorber influence to the body nodes
                pass
                node.speedVector = node.speedVector.add(self.springForceVector)
                node.speedVector = node.speedVector.add(self.absorberForceVector)
            else:
                node.speedVector = node.speedVector.add(self.springForceVector.mul(-1*self.response))
                node.speedVector = node.speedVector.add(self.absorberForceVector.mul(-1*self.response))

            #changes position
            tempPosition = Vector3d(node.x, node.y, node.z).add(node.speedVector)
            node.x = tempPosition.x
            node.y = tempPosition.y
            node.z = tempPosition.z

