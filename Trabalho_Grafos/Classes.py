import math

class Node:
    def __init__(self, x, y, Id):
         self.coordX = x
         self.coordY = y
         self.idNode = Id
         self.visit = False
         self.region = -1

    def getCoordX(self):
         return self.coordX

    def getCoordY(self):
         return self.coordY

    def getId(self):
         return self.idNode
     
    def getVisit(self):
         return self.visit
     
    def setVisit(self, b):
         self.visit = b   

    def setRegion(self, r):
        self.region = r

class Edge:
    def __init__(self, V1, V2, d):
         self.edge = (V1, V2)
         self.distance = d

    def getDistance(self):
         return self.distance

    def getEdge(self):
         return self.edge

class Set:
    def __init__(self, Id, d):
        self.lixt = []
        self.idSet = Id
        self.demand = d
        self.visit = False

    def getLixt(self):
        return self.lixt

    def getidSet(self):
        return self.idSet

    def getDemand(self):
        return self.demand

    def getVisit(self):
        return self.visit

    def setVisit(self, b):
        self.visit = b

class Vehicle:
    def __init__(self, c, Id):
        self.capacity = c
        self.Id = Id
        self.rote = []

    def getId(self):
        return self.Id

    def setCapacity(self, quant):
        self.capacity = self.capacity - quant

    def getCapacity(self):
        return self.capacity
        

def calculaDistancia(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))







