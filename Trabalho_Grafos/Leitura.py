import networkx as nx
import random
import tsp
from matplotlib import pyplot as plt
from os import path
from Classes import *

# importa grafo do arquivo filename, a vértice 1 é a garagem dos veículos
def get_graph(filename):
    # graph = nx.Graph()
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

        # return (graph, graph_settings)

Nodes = []
Sets = []
Veiculos = []
Arestas = []

def main():
    graph_settings = get_graph("./data/problemas-grupo1/problema4.txt")

    tam = len(Nodes)
    i = 0
    while(i < tam):
        print(Nodes[i].idNode, Nodes[i].coordX, Nodes[i].coordY, Nodes[i].region)
        i += 1

    SetAux = sorted(Sets, key = Set.getDemand, reverse=True)
    tam = len(SetAux)
    i = 0
    while(i < tam):
        print(SetAux[i].idSet, SetAux[i].demand, SetAux[i].lixt)
        i += 1

    for i in range(int(graph_settings["VEHICLES"])):
        Veiculos.append(Vehicle(int(graph_settings["CAPACITY"]), int(i)))

    tam = len(Veiculos)
    i = 0
    while(i < tam):
        print(Veiculos[i].capacity)
        i += 1

    i = 0
    j = 0
    tamSets = len(Sets)

    while(i < int(graph_settings["DIMENSION"])):
        j = i
        while(j < int(graph_settings["DIMENSION"])):     
            if i != j and Nodes[i].region != Nodes[j].region:
                distancia = calculaDistancia(Nodes[i].coordX, Nodes[i].coordY, Nodes[j].coordX, Nodes[j].coordY)
                aresta = Edge(Nodes[i].idNode, Nodes[j].idNode, distancia)
                Arestas.append(aresta)
            j += 1
        i += 1

    tam = len(Arestas)
    i = 0
    while(i < tam):
        print(Arestas[i].edge, Arestas[i].distance)
        i += 1

    i = 0
    tamV = len(Veiculos)
    while(i < tamV):
        for j in SetAux:
            if(int(Veiculos[i].capacity) < j.demand):
                break
            if(j.visit == False):
                Veiculos[i].rote.append(j.idSet)
                Veiculos[i].capacity -= int(j.demand)
                j.visit = True

        for j in SetAux:
            if(int(Veiculos[i].capacity >= j.demand and j.visit == False)):
                Veiculos[i].rote.append(j.idSet)
                Veiculos[i].capacity -= int(j.demand)
                j.visit = True
            if(int(Veiculos[i].capacity == 0)):
                break

        i += 1

    

    i = 0
    while(i < tamV):
        print(Veiculos[i].Id, Veiculos[i].rote, Veiculos[i].capacity)
        i += 1

main()
