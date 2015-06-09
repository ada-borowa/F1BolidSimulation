#-*- coding: utf-8 -*-

import math

# ------>x
# |
# |
# |
# |
# \/y

def body_nodes():
    nodes = [
        #0-5 lewy bok czesci A
        (230, 300, 70), (300, 300, 100), (500, 300, 100),
        (230, 230, 70), (300, 230, 100), (500, 230, 100),
        #6-11 prawy bok czesci A
        (230, 300, -70), (300, 300, -100), (500, 300, -100),
        (230, 230, -70), (300, 230, -100), (500, 230, -100),
        #12-15 czesc B - 0, 3, 6, 9 juz jest
        (130, 300, 40), (130, 260, 40), (130, 300, -40), (130, 260, -40),
        #16-19 czesc A tylna sciana
        (500, 300, 60), (500, 230, 60), (500, 300, -60), (500, 230, -60),
        #20-23, czesc C - 16-19 juz jest
        (570, 300, 50), (570,230, 50), (570, 300, -50), (570, 230, -50),
        #24-27, polaczenie czesci C i E, do 21, 23
        (575, 220, 50), (580, 220, 50), (575, 220, -50), (580, 220, -50),
        #28-35, czesc E, laczone do 24-27
        (575, 220, 100), (580, 220, 100), (575, 220, -100), (580, 220, -100),
        (575, 170, 100), (580, 170, 100), (575, 170, -100), (580, 170, -100),
        #36-37, czesc B, laczenie do D
        (160, 300, 49), (160, 300, -49),
        #38-41, polaczesnie czesci B i D
        (160, 305, 49), (130, 305, 40), (160, 305, -49), (130, 305, -40),
        #42-49, czesc D, laczone do 38-42
        (160, 305, 100), (130, 305, 100), (160, 305, -100), (130, 305, -100),
        (160, 310, 100), (130, 310, 100), (160, 310, -100), (130, 310, -100)
    ]
    nodes = [node + ('body',) for node in nodes]
    return nodes

def body_edges():
    edges = [
        #lewy bok czesci A
        (0, 1), (1, 2), (3, 4), (4, 5), (0, 3), (1, 4), (2, 5),
        #prawy bok czesci A
        (6, 7), (7, 8), (9, 10), (10, 11), (6, 9), (7, 10), (8, 11),
        #reszta polaczen czesci A
        (0, 6), (1, 7), (3, 9), (4, 10), (2, 16), (5, 17), (16, 17),
        (16, 18), (17, 19), (18, 19), (8, 18), (11, 19),
        # czesc B
        (12, 13), (13, 15), (15, 14), (14, 12), (3, 13), (9, 15),
        (0, 36), (36, 12), (6, 37), (37, 14),
        # czesc C
        (16, 20), (17, 21), (18, 22), (19, 23), (20, 21), (21, 23),
        (23, 22), (22, 20),
        # C + E
        (21, 24), (21, 25), (24, 25), (23, 26), (23, 27), (26, 27),
        (24, 26), (25, 27),
        # czesc E
        (24, 28), (28, 29), (29, 25), (27, 31), (31, 30), (30, 26),
        (28, 32), (29, 33), (30, 34), (31, 35),
        (32, 33), (33, 35), (34, 35), (32, 34),
        # B + D
        (12, 39), (14, 41), (36, 38), (37, 40), (40, 41), (38, 39), (36, 37),
        # czesc D
        (40, 42), (42, 43), (43, 41), (41, 39), (39, 45), (45, 44), (44, 38), (38, 40),
        (47, 46), (46, 48), (48, 49), (49, 47), (43, 47), (42, 46), (44, 48), (45, 49)
    ]

    edges = [edge + (1,) for edge in edges]
    return edges

def tire(anchor, anchor_nr, dist, radius, width, direction, begin):
    spoke = 0.8
    spring = 0.6
    connector = 10
    height = 80
    if direction == 'left':
        dist *= -1
        width *= -1
        connector *= -1
    nodes = []
    edges = []
    #bolid - spring connection
    nodes.append((anchor[0], anchor[1], anchor[2]+dist, 'body'))
    #spring
    nodes.append((anchor[0], anchor[1]+height, anchor[2]+dist, 'spring_connector'))
    #spring - tire connector, this node i also tire node (node no 3)
    tireAnchor1 = (anchor[0], anchor[1]+height, anchor[2]+dist+connector, 'tire_anchor')
    nodes.append(tireAnchor1)
    #second tire node (node no 4)
    tireAnchor2 = (anchor[0], anchor[1]+height, anchor[2]+dist+connector+width, 'tire_anchor')
    nodes.append(tireAnchor2)
    edges.extend(((anchor_nr, begin+1, 1), (begin+1, begin+2, spring), (begin+2, begin+3, 1), (begin+3, begin+4, 1)))
    #Tire is connected to nodes 3 and 4, creating:
    alpha = 0
    beta = math.pi/180
    nr = begin+5
    for i in range(1, 359):
        x = tireAnchor1[0] + radius * math.cos(alpha)
        y = tireAnchor1[1] - radius * math.sin(alpha)
        #print "%d %d" % (x, y)
        nodes.extend(((x, y, tireAnchor1[2], 'tire'), (x, y, tireAnchor2[2], 'tire')))
        edges.extend(((begin+3, nr, spoke), (begin+4, nr + 1, spoke), (nr, nr + 1, 1)))
        if i > 1:
            edges.extend(((nr, nr - 2, 1), (nr + 1, nr - 1, 1)))
        nr += 2
        alpha += beta
    nr -= 2
    edges.extend(((nr, begin+5, 1), (nr + 1, begin+6, 1)))
    return (nodes, edges)

def road(position):
    nodes = []
    edges = []
    for i in range(0, 800, 2):
        nodes.extend(((i, position, 150, 'road'), (i, position, -150, 'road')))
        edges.append((i, i + 1, 10))
    return (nodes, edges)