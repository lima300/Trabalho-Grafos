import networkx as nx
import random
import tsp
from matplotlib import pyplot as plt
from os import path
import math

class Node:
    def __init__(self, x, y, Id):
         self.coordX = x
         self.coordY = y
         self.idNode = Id
         self.visit = False
         self.region = -1
         self.demand = -1

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

    def setDemand(self, d):
        self.demand = d

class Edge:
    def __init__(self, V1, V2, d):
         self.edge = (V1, V2)
         self.distance = d

    def getDistance(self):
         return self.distance

    def getEdge(self):
         return self.edge

# class Set:
#     def __init__(self, Id, d):
#         self.lixt = []
#         self.idSet = Id
#         self.demand = d
#         self.visit = False

#     def getLixt(self):
#         return self.lixt

#     def getidSet(self):
#         return self.idSet

#     def getDemand(self):
#         return self.demand

#     def getVisit(self):
#         return self.visit

#     def setVisit(self, b):
#         self.visit = b

class Vehicle:
    def __init__(self, c, Id):
        self.capacity = c
        self.Id = Id
        self.roteNodes = []
        self.totalDistance = 0

    def getId(self):
        return self.Id

    def setCapacity(self, quant):
        self.capacity = self.capacity - quant

    def getCapacity(self):
        return self.capacity
        
def calculaDistancia(x1, y1, x2, y2):
    return float(math.sqrt(((x2-x1)**2)+((y2-y1)**2)))

# importa grafo do arquivo filename, a vértice 1 é a garagem dos veículos
def get_graph(filename):
    graph_settings = dict()
    file_path = path.relpath(filename)

    with open(file_path, "r") as data_file:

        # leitura das configurações do problema
    
        last_reader_pos = data_file.tell()
        current_line = data_file.readline()

        while current_line != "NODE_COORD_SECTION\n":
            # lê a linha formatada como CONFIGURAÇÃO : VALOR
            (key, val) = current_line.rsplit(" : ", 1)
            # salva VALOR no dicionário usando CONFIGURAÇÃO como chave
            graph_settings[key] = val.rstrip("\n")

            current_line = data_file.readline()


            new_reader_pos = data_file.tell()
            # checa se cursor se moveu para tratar EOF prematuro
            if last_reader_pos == new_reader_pos:
                raise EOFError("Atingiu EOF sem encontrar NODE_COORD_SECTION")
            else:
                last_reader_pos = new_reader_pos



        # leitura das vértices e suas coordenadas

        last_reader_pos = data_file.tell()

        for i in range(int(graph_settings["DIMENSION"])):
            current_line = data_file.readline()

            (node_number, coord) = current_line.split(" ", 1)
            (coordx, coordy) = (coord.rstrip("\n")).split(" ")

            node = Node(int(coordx), int(coordy), int(node_number))

            Nodes.append(node)

            new_reader_pos = data_file.tell()
            # checa se cursor se moveu para tratar EOF prematuro
            if last_reader_pos == new_reader_pos:
                raise EOFError("Atingiu EOF antes de ler coordenadas de todas vértices")
            else:
                last_reader_pos = new_reader_pos

        # leitura dos sets

        current_line = data_file.readline()
        last_reader_pos = data_file.tell()

        if current_line != "SET_SECTION\n":
            raise RuntimeError("Esperado \"SET_SECTION\", mas foi lido \"{}\"".format(current_line))

        for i in range(int(graph_settings["SETS"])):
            current_line = data_file.readline()
            (current_set, nodes_in_set) = current_line.split(" ", 1)
            nodes_in_set = nodes_in_set.split(" ")

            for each_node in nodes_in_set:
                for i in Nodes:
                    if i.idNode == int(each_node):
                        i.region = current_set

            new_reader_pos = data_file.tell()
            # checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todos os sets")
            else:
                last_reader_pos = new_reader_pos



        # leitura das demandas

        graph_settings["DEMAND_TOTAL"] = int(0)

        current_line = data_file.readline()
        last_reader_pos = data_file.tell()
    
        if current_line != "DEMAND_SECTION\n":
            raise RuntimeError("Esperado \"DEMAND_SECTION\", mas foi lido \"{}\"".format(current_line))

        for i in range(int(graph_settings["SETS"])):
            current_line = data_file.readline()
            (current_set, current_demand) = (current_line.rstrip("\n")).split(" ", 1)
            graph_settings["DEMAND_TOTAL"] += int(current_demand)

            for i in Nodes:
                if(int(current_set) == int(i.region)):
                    i.demand = int(current_demand)

            new_reader_pos = data_file.tell()

            # checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todas as demandas")
            else:
                last_reader_pos = new_reader_pos



        current_line = data_file.readline()
        if current_line != "EOF":
            raise RuntimeError("Esperado \"EOF\", mas foi lido \"{}\"".format(current_line))

    return graph_settings

def add_Edge(graph_settings):
    i = 0
    j = 0
    while(i < int(graph_settings["DIMENSION"])):
        j = 0
        while(j < int(graph_settings["DIMENSION"])):     
            if i != j and Nodes[i].region != Nodes[j].region:
                distancia = calculaDistancia(Nodes[i].coordX, Nodes[i].coordY, Nodes[j].coordX, Nodes[j].coordY)
                aresta = Edge(int(Nodes[i].idNode), int(Nodes[j].idNode), float(distancia))
                Edges.append(aresta)
            j += 1
        i += 1

def add_Vehicle(graph_settings):
    for i in range(int(graph_settings["VEHICLES"])):
        Vehicles.append(Vehicle(int(graph_settings["CAPACITY"]), int(i)))


def print_Node():
    tam = len(Nodes)
    i = 0
    while(i < tam):
        print(Nodes[i].idNode, Nodes[i].coordX, Nodes[i].coordY, Nodes[i].visit, Nodes[i].region, Nodes[i].demand)
        i += 1

def print_Vehicles():
    tamV = len(Vehicles)
    i = 0
    while(i < tamV):
        print(Vehicles[i].Id, Vehicles[i].capacity, Vehicles[i].roteNodes, Vehicles[i].totalDistance)
        i += 1

def print_Edges():
    tam = len(Edges)
    i = 0
    while(i < tam):
        print(Edges[i].edge, Edges[i].distance)
        i += 1

Nodes = []
Vehicles = []
Edges = []

def exist_Region_Not_Visit(c):
    exist = False
    i = 0
    tamN = len(Nodes)
    while(i < tamN):
        if(Nodes[i].visit == False and Nodes[i].demand <= Vehicles[c].capacity):
            exist = True
        i += 1
    return exist

def Nearest_Neighbor_Heuristic(graph_settings):
    somDemand = int(0)
    e = 0
    tamE = len(Edges)
    maxDistance = 0
    while(e < tamE):
        if(float(Edges[e].distance) > float(maxDistance)):
            maxDistance = float(Edges[e].distance)
        e += 1   
    menDemand = Nodes[0].demand   
    tamN = len(Nodes)    
    a = 0
    tamV = len(Vehicles)
    Nodes[0].visit = True
    while(a < tamV):
        condAux = []
        capacity = False
        vInsert = int(1)
        vInsertAux = int(1)
        Vehicles[a].roteNodes.append(int(1))
        i = 0
        while(exist_Region_Not_Visit(a) == True):
            vMinDistance = float(maxDistance)
            j = 0
            while(j < tamN):
                if(int(Nodes[vInsertAux-1].idNode) != int(Nodes[j].idNode) and Nodes[j].visit == False and Nodes[j].idNode not in condAux):
                    if(float(vMinDistance) > calculaDistancia(int(Nodes[vInsertAux-1].coordX), int(Nodes[vInsertAux-1].coordY), int(Nodes[j].coordX), int(Nodes[j].coordY))):
                        vMinDistance = calculaDistancia(int(Nodes[vInsertAux-1].coordX), int(Nodes[vInsertAux-1].coordY), int(Nodes[j].coordX), int(Nodes[j].coordY))
                        vInsert = int(Nodes[j].idNode)
                j += 1
            
            if(Nodes[vInsert-1].visit == False and Vehicles[a].capacity >= Nodes[vInsert-1].demand):
                Vehicles[a].roteNodes.append(Nodes[vInsert-1].idNode)
                vInsertAux = vInsert
                Vehicles[a].totalDistance += vMinDistance
                somDemand += int(Nodes[vInsert-1].demand)
                r = 0
                tamR = len(Nodes)
                while(r < tamR):
                    if(Nodes[vInsert-1].region == Nodes[r].region):
                        Nodes[r].visit = True
                    r += 1
                vMinDistance = float(maxDistance)
                Nodes[vInsert-1].visit = True
                Vehicles[a].capacity -= Nodes[vInsert-1].demand
            else:
                condAux.append(Nodes[vInsert-1].idNode)
        
        Vehicles[a].roteNodes.append(int(1))
        a += 1
    for a in Vehicles:
        tam = len(a.roteNodes)
        a.totalDistance += calculaDistancia(int(Nodes[int(a.roteNodes[tam-2])-1].coordX), int(Nodes[int(a.roteNodes[tam-2])-1].coordY), int(Nodes[0].coordX), int(Nodes[0].coordY))

def calcula_distancia_total():
    distanciaTotal = int(0)
    for i in Vehicles:
        distanciaTotal += i.totalDistance
    
    return distanciaTotal

def main():
    graph_settings = get_graph("./data/problemas-grupo2/problema12.txt")
    add_Vehicle(graph_settings)
    add_Edge(graph_settings)
    Nearest_Neighbor_Heuristic(graph_settings)
    print_Vehicles()
    print_Node()
    # print_Edges()
    print("A distancia total percorrida pelos carros foi de :", calcula_distancia_total())
    
main()
