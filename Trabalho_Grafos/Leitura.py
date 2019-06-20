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
        self.roteRegion = []
        self.roteNodes = []
        self.totalDistance = 0

    def getId(self):
        return self.Id

    def setCapacity(self, quant):
        self.capacity = self.capacity - quant

    def getCapacity(self):
        return self.capacity
        
def calculaDistancia(x1, y1, x2, y2):
    return math.sqrt(((x2-x1)**2)+((y2-y1)**2))

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

            aux = []

            for each_node in nodes_in_set:
                for i in Nodes:
                    if i.idNode == int(each_node):
                        i.region = current_set
                if int(each_node) != -1:
                    aux.append(int(each_node))

            sett = Set(current_set, 0)
            tam = len(aux)
            i = 0
            while(i < tam):
                sett.lixt.append(aux[i])
                i += 1
            
            Sets.append(sett)

            new_reader_pos = data_file.tell()
            # checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todos os sets")
            else:
                last_reader_pos = new_reader_pos



        # leitura das demandas

        current_line = data_file.readline()
        last_reader_pos = data_file.tell()
    
        if current_line != "DEMAND_SECTION\n":
            raise RuntimeError("Esperado \"DEMAND_SECTION\", mas foi lido \"{}\"".format(current_line))

        for i in range(int(graph_settings["SETS"])):
            current_line = data_file.readline()
            (current_set, current_demand) = (current_line.rstrip("\n")).split(" ", 1)

            Sets[i].demand = int(current_demand)


            new_reader_pos = data_file.tell()

            # checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todas as demandas")
            else:
                last_reader_pos = new_reader_pos



        current_line = data_file.readline()
        if current_line != "EOF":
            raise RuntimeError("Esperado \"EOF\", mas foi lido \"{}\"".format(current_line))
    
        a = 0
        for i in range(int(graph_settings["DIMENSION"])):
            a = a + 1
            n = 1

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
        print(Nodes[i].idNode, Nodes[i].coordX, Nodes[i].coordY, Nodes[i].visit, Nodes[i].region)
        i += 1

def print_Set():
    SetAux = sorted(Sets, key = Set.getDemand, reverse = True)
    tam = len(SetAux)
    i = 0
    while(i < tam):
        print(SetAux[i].idSet, SetAux[i].demand, SetAux[i].visit, SetAux[i].lixt)
        i += 1

def print_Vehicles():
    tamV = len(Vehicles)
    i = 0
    while(i < tamV):
        print(Vehicles[i].Id, Vehicles[i].roteRegion, Vehicles[i].capacity, Vehicles[i].totalDistance)
        i += 1

def print_Edges():
    tam = len(Edges)
    i = 0
    while(i < tam):
        print(Edges[i].edge, Edges[i].distance)
        i += 1

def rote_Region():
    SetAux = sorted(Sets, key = Set.getDemand, reverse = True)
    i = 0

    tamV = len(Vehicles)
    while(i < tamV):
        # Vehicles[i].roteRegion.append(int(1))
        for j in SetAux:
            if(int(Vehicles[i].capacity) < j.demand):
                break
            if(j.visit == False):
                Vehicles[i].roteRegion.append(int(j.idSet))
                Vehicles[i].capacity -= int(j.demand)
                j.visit = True

        for j in SetAux:
            if(int(Vehicles[i].capacity >= j.demand and j.visit == False)):
                Vehicles[i].roteRegion.append(int(j.idSet))
                Vehicles[i].capacity -= int(j.demand)
                j.visit = True
            if(int(Vehicles[i].capacity == 0)):
                break
        # Vehicles[i].roteRegion.append(int(1))

        i += 1

def rote_Node():
    i = 0
    tamV = len(Vehicles)
    while(i < tamV):
        Vehicles[i].roteNodes.append(int(1))   
        j = 0
        tamVR = len(Vehicles[i].roteRegion)
        while(j < tamVR):
            k = 0
            tamS = len(Sets)
            atualNode = (int(1))
            while(k < tamS):
                value = 0
                if(int(Vehicles[i].roteRegion[j]) == int(Sets[k].idSet)):
                    achou = False
                    l = 0
                    tamSN = len(Sets[k].lixt)
                    mindistanceAux = 0
                    while(l < tamSN):
                        m = 0
                        tamE = len(Edges)
                        while(m < tamE):
                            if(Edges[m].edge == (int(atualNode), int(Sets[k].lixt[l])) and achou == False):
                                mindistance = float(Edges[m].distance)
                                mindistanceAux = mindistance
                                value = int(Sets[k].lixt[l]) 
                                achou = True
                            if(Edges[m].edge == (int(atualNode), int(Sets[k].lixt[l])) and mindistance > float(Edges[m].distance)):
                                mindistance = float(Edges[m].distance)
                                mindistanceAux = mindistance
                                value = int(Sets[k].lixt[l])    
                            m += 1
                        l += 1
                    Vehicles[i].totalDistance += float(mindistanceAux)  
                    Vehicles[i].roteNodes.append(value)
                indice = len(Vehicles[i].roteNodes) - 1
                atualNode = int(Vehicles[i].roteNodes[indice])
                k += 1
            j += 1
        Vehicles[i].roteNodes.append(int(1))
        i += 1

def print_rote_Node():
    i = 0
    tamV = len(Vehicles)
    while(i < tamV):
        print(Vehicles[i].roteNodes)
        i += 1

Nodes = []
Sets = []
Vehicles = []
Edges = []

def main():
    graph_settings = get_graph("./data/problemas-grupo1/problema4.txt")
    add_Edge(graph_settings)
    add_Vehicle(graph_settings)
    rote_Region()
    rote_Node()
    print_Vehicles()
    print_rote_Node()
    # print_Set()
    # print_Edges()

main()
