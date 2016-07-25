"""
A simple quadtree that we'll use to solve the TSP in a suboptimal but efficient way
"""
import logging
class Tree(object):
    hilbert_map = {
        'a': {(0, 0): (0, 'd'), (0, 1): (1, 'a'), (1, 0): (3, 'b'), (1, 1): (2, 'a')},
        'b': {(0, 0): (2, 'b'), (0, 1): (1, 'b'), (1, 0): (3, 'a'), (1, 1): (0, 'c')},
        'c': {(0, 0): (2, 'c'), (0, 1): (3, 'd'), (1, 0): (1, 'c'), (1, 1): (0, 'b')},
        'd': {(0, 0): (0, 'a'), (0, 1): (3, 'c'), (1, 0): (1, 'd'), (1, 1): (2, 'd')},
    }
    def __init__(self, rect, level):
        #logging.info(rect)
        self.rect = rect
        self.level = level
        self.objects = []
        if level > 0:
            nextLevel = level - 1
            self.nodes = {
                    "NW": Tree(Rect(rect.left, rect.top, rect.midpoint[0], rect.midpoint[1]), nextLevel), 
                    "SW": Tree(Rect(rect.left, rect.midpoint[1], rect.midpoint[0], rect.bottom), nextLevel), 
                    "NE": Tree(Rect(rect.midpoint[0], rect.top, rect.right, rect.midpoint[1]), nextLevel),
                    "SE": Tree(Rect(rect.midpoint[0], rect.midpoint[1], rect.right, rect.bottom), nextLevel)
            }
        else: 
            self.nodes = None
    
    def point_to_hilbert(x, y, order=16):
        current_square = 'a'
        position = 0
        for i in range(order - 1, -1, -1):
            position <<= 2
            quad_x = 1 if x & (1 << i) else 0
            quad_y = 1 if y & (1 << i) else 0
            quad_position, current_square = hilbert_map[current_square][(quad_x, quad_y)]
            position |= quad_position
        return position

    def getObjects(self):
        if self.nodes is None:
            return self.objects
        return self.nodes['NW'].getObjects() + self.nodes['NE'].getObjects() + self.nodes['SW'].getObjects() + self.nodes['SE'].getObjects()
        
                
    def addObject(self, x, y, obj):
        if self.nodes is None:
            self.objects.append(obj)
        else:
            h = "W"
            v = "N"
            if x > self.rect.midpoint[0]:
                h = "E"
            if y > self.rect.midpoint[1]:
                v = "S"

            key = "%s%s" % (v, h)

            self.nodes[key].addObject(x, y, obj)

class Rect(object):
    def __init__(self, x1, y1, x2, y2):
        self.left = x1
        self.top = y1
        self.right = x2
        self.bottom = y2

        self.width = abs(x2-x1)
        self.height = abs(y2-y1)
        self.midpoint = (x1+self.width/2, y1+self.height/2)

    def __str__(self):
        return "Recatangle: (%f, %f) (%f, %f)  %fX%f" %(self.left,self.top,self.right,self.bottom,self.width, self.height)