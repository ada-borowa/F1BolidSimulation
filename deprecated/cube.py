#-*- coding: utf-8 -*-

from extra.projectionViewer import ProjectionViewer
from extra.wireframe import Wireframe

if __name__ == "__main__":
    cube_nodes = [(x,y,z) for x in (50,250) for y in (50,250) for z in (50,250)]

    cube = Wireframe()
    cube.addNodes(cube_nodes)
    cube.addEdges([(n,n+4) for n in range(0,4)])   #(0,4),(1,5),(2,6),(3,7)
    cube.addEdges([(n,n+1) for n in range(0,8,2)]) #(0,1),(2,3),(4,5),(6,7)
    cube.addEdges([(n,n+2) for n in (0,1,4,5)])    #(0,2),(1,3),(4,6),(5,7)

    cube.outputNodes()
    cube.outputEdges()

    pv = ProjectionViewer(400,300)
    pv.addWireframe('cube', cube)
    pv.run()

