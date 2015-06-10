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
        self.groundFront = False
        self.groundBack = False
        #gravity
        self.gravityVector = Vector3d(0, 0.03, 0)
        #spring
        self.response = 2.0
        self.k = 0.004
        self.springForceVectorFront = Vector3d(0,0,0)
        self.springForceVectorRear = Vector3d(0,0,0)
        #absorber
        self.beta = 0.1
        self.absorberForceVectorFront = Vector3d(0,0,0)
        self.absorberForceVectorRear = Vector3d(0,0,0)
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

    def checkGround(self):
        """Checks if any node is touching ground y = 320"""

        self.groundFront = False
        self.groundBack = False

        for i, node in enumerate(self.nodes):
            if self.roadFun(node.x) <= node.y and self.frontTireIndexesRight[0] <= i < self.frontTireIndexesRight[1]:
                self.groundFront = True
                break
        for i, node in enumerate(self.nodes):
            if self.roadFun(node.x) <= node.y and self.rearTireIndexesRight[0] <= i < self.rearTireIndexesRight[1]:
                self.groundBack = True
                break

    def checkSprings(self):
        #checks only one spring, cause the rest is the same
        edge = self.springs[0]
        length = math.sqrt(math.pow(edge.start.x - edge.stop.x, 2) + math.pow(edge.start.y - edge.stop.y, 2) +
                           math.pow(edge.start.z - edge.stop.z, 2))
        # spring F = -kx
        forceLength = self.springLength-length
        self.springForceVectorFront = Vector3d(edge.start.x - edge.stop.x, edge.start.y - edge.stop.y, edge.start.z - edge.stop.z).unitVector().mul(forceLength).mul(self.k)

        #going down, absorber F = beta*v

        diffSpeed = edge.start.speedVector.mul(-1).add(edge.stop.speedVector)
        self.absorberForceVectorFront = diffSpeed.mul(self.beta)

        diffSpeed = edge.start.speedVector.mul(-1).add(edge.stop.speedVector)
        self.absorberForceVectorFront = diffSpeed.mul(self.beta)

        edge = self.springs[2]
        length = math.sqrt(math.pow(edge.start.x - edge.stop.x, 2) + math.pow(edge.start.y - edge.stop.y, 2) +
                           math.pow(edge.start.z - edge.stop.z, 2))
        # spring F = -kx
        forceLength = self.springLength-length
        self.springForceVectorRear = Vector3d(edge.start.x - edge.stop.x, edge.start.y - edge.stop.y, edge.start.z - edge.stop.z).unitVector().mul(forceLength).mul(self.k)

        diffSpeed = edge.start.speedVector.mul(-1).add(edge.stop.speedVector)
        self.absorberForceVectorRear = diffSpeed.mul(self.beta)


    def _hitedGroundSpeed(self, groundVector, speedVector):
        scalar = -2 * (groundVector.unitVector()).dot(speedVector)
        scalar = -abs(scalar)
        ret = (groundVector.unitVector()).mul(scalar).add(speedVector)
        return ret


    def move(self):
        #evaluates position in (x,y) of every node

        anc1 = self.nodes[self.ancor1index]
        anc3 = self.nodes[self.ancor3index]

        C = Vector3d(anc3.x-anc1.x, anc3.y-anc1.y, anc3.z-anc1.z)

        for i, node in enumerate(self.nodes):
            # if node.part == 'body':
            #     continue
            #gravity
            #bouncing off the ground for tires and suspension
            if self.groundFront == True and (self.frontTireIndexesRight[0] <= i < self.frontTireIndexesRight[1] or self.frontTireIndexesLeft[0] <= i < self.frontTireIndexesLeft[1]):
                pass
                node.speedVector = node.speedVector.add(self.gravityVector)
                node.speedVector = self._hitedGroundSpeed(self.groundVector, node.speedVector)
            elif self.groundBack == True and (self.rearTireIndexesRight[0] <= i < self.rearTireIndexesRight[1] or self.rearTireIndexesLeft[0] <= i < self.rearTireIndexesLeft[1]):
                node.speedVector = self._hitedGroundSpeed(self.groundVector, node.speedVector)
                node.speedVector = node.speedVector.add(self.gravityVector)
            elif (self.frontTireIndexesRight[0] <= i < self.frontTireIndexesRight[1] or self.frontTireIndexesLeft[0] <= i < self.frontTireIndexesLeft[1]):
                node.speedVector = node.speedVector.add(self.gravityVector)
                node.speedVector = node.speedVector.add(self.springForceVectorFront.mul(-1*self.response))
                node.speedVector = node.speedVector.add(self.absorberForceVectorFront.mul(-1*self.response))
            elif (self.rearTireIndexesRight[0] <= i < self.rearTireIndexesRight[1] or self.rearTireIndexesLeft[0] <= i < self.rearTireIndexesLeft[1]):
                node.speedVector = node.speedVector.add(self.gravityVector)
                node.speedVector = node.speedVector.add(self.absorberForceVectorRear.mul(-1*self.response))
                node.speedVector = node.speedVector.add(self.springForceVectorRear.mul(-1*self.response))
            elif i in [self.ancor1index, self.ancor2index]:
                node.speedVector = node.speedVector.add(self.gravityVector)
                node.speedVector = node.speedVector.add(self.springForceVectorFront) # TODO
                node.speedVector = node.speedVector.add(self.absorberForceVectorFront)
            elif i in [self.ancor3index, self.ancor4index]:
                node.speedVector = node.speedVector.add(self.gravityVector)
                node.speedVector = node.speedVector.add(self.springForceVectorRear) # TODO
                node.speedVector = node.speedVector.add(self.absorberForceVectorRear)
            else:
                node.speedVector = node.speedVector.add(self.gravityVector)
                node.speedVector = node.speedVector.add(self.springForceVectorRear) # TODO
                node.speedVector = node.speedVector.add(self.absorberForceVectorRear)

            #changes position
            node.x += node.speedVector.x
            node.y += node.speedVector.y
            node.z += node.speedVector.z

        anc1new = self.nodes[self.ancor1index]
        anc3new = self.nodes[self.ancor3index]

        Cnew = Vector3d(anc3new.x-anc1new.x, anc3new.y-anc1new.y, anc3new.z-anc1new.z)

        cosangle = Cnew.cos(C)
        # print cosangle, C.cos(Cnew)
        angle = -math.acos(cosangle)

        for i, node in enumerate(self.nodes):
            if node.part == 'body':
                # adds spring and absorber influence to the body nodes
                pass
                # node.speedVector = node.speedVector.add(self.springForceVectorFront) # TODO
                # node.speedVector = node.speedVector.add(self.absorberForceVectorFront)

                if i in [self.ancor1index, self.ancor2index, self.ancor3index, self.ancor4index]:
                    continue

                a = Vector3d(node.x-anc1.x, node.y-anc1.y, node.z-anc1.z)
                a.rotateZ(angle)

                node.x = anc1new.x + a.x
                node.y = anc1new.y + a.y
                node.z = anc1new.z + a.z

