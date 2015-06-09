#-*- coding: utf-8 -*-

from node import *
from edge import *

#defined as variable height in construction.py
springLength = 80
#ground is determined from the top of the screen
groundLvl = 360

class Wireframe:
    def __init__(self):
        self.nodes = []
        self.edges = []
        self.springs = []
        self.ground = False
        #gravity
        self.gravity = (math.pi, 0.001)
        #spring
        self.k = 0.01
        self.spring = (math.pi, 0)
        #absorber
        self.beta = 0.01
        self.absorber = (math.pi, 0)
        #gravity, spring, absorber: constants to be determined!

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

    def scale(self, (centre_x, centre_y), scale):
        """ Scale the wireframe from the centre of the screen """

        for node in self.nodes:
            node.x = centre_x + scale * (node.x - centre_x)
            node.y = centre_y + scale * (node.y - centre_y)
            node.z *= scale
            node.speed *= scale
        self.ground = centre_y + scale * (self.ground - centre_y)

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
            node.z = cz + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def rotateY(self, (cx,cy,cz), radians):
        for node in self.nodes:
            x      = node.x - cx
            z      = node.z - cz
            d      = math.hypot(x, z)
            theta  = math.atan2(x, z) + radians
            node.z = cz + d * math.cos(theta)
            node.x = cx + d * math.sin(theta)

    def rotateZ(self, (cx,cy,cz), radians):
        for node in self.nodes:
            x      = node.x - cx
            y      = node.y - cy
            d      = math.hypot(y, x)
            theta  = math.atan2(y, x) + radians
            node.x = cx + d * math.cos(theta)
            node.y = cy + d * math.sin(theta)

    def checkGround(self):
        """Checks if any node is touching ground y = 320"""

        self.ground = False

        for node in self.nodes:
            if node.y > groundLvl:
                self.ground = True

    def checkSprings(self):
        #checks only one spring, cause the rest is the same
        edge = self.springs[0]
        length = math.sqrt(math.pow(edge.start.x - edge.stop.x, 2) + math.pow(edge.start.y - edge.stop.y, 2) +
                           math.pow(edge.start.z - edge.stop.z, 2))
        # spring F = -kx
        self.spring = (math.pi, -self.k*(springLength - length))
        #going down, absorber F = beta*v
        if math.pi/2 < edge.start.angle < 3*math.pi/2:
            absForce = -self.beta * edge.start.speed
        #going up
        else:
            absForce = self.beta * edge.start.speed
        self.absorber = (math.pi, absForce)

    def move(self):
        #evaluates position in (x,y) of every node
        for node in self.nodes:
            #gravity
            (node.angle, node.speed) = addVectors((node.angle, node.speed), self.gravity)
            #bouncing off the ground for tires and suspension
            if self.ground == True and node.part != 'body':
                node.angle = math.pi-node.angle
            if node.part == 'body':
                #adds spring and absorber influence to the body nodes
               (node.angle, node.speed) = addVectors((node.angle, node.speed), self.spring)
               (node.angle, node.speed) = addVectors((node.angle, node.speed), self.absorber)
            #changes position
            node.x += math.sin(node.angle) * node.speed
            node.y -= math.cos(node.angle) * node.speed

