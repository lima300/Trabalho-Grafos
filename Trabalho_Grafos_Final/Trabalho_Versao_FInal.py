import networkx as nx
import random
import tsp
from matplotlib import pyplot as plt
from os import path
import math

# Lista contendo todos os vértices lidos do arquivo de entrada
Nodes = []
# Lista contendo os veículos lidos do arquivo de entrada
Vehicles = []
# Lista contendo todas as arestas do grafo, obtidas à partir da lista de vértices(obs: utilizada apenas para controle e testes)
Edges = []

# Classe que representa um vértice e seus atributos
class Node:
    # Construtor da classe Vértice
    def __init__(self, x, y, Id):
        # Inteiro que representa a coordenada X do vértice
        self.coordX = x
        # Inteiro que representa a coordenada Y do vértice
        self.coordY = y
        # Inteiro que identifica o vértice
        self.idNode = Id
        # Booleano que indica se o vértice já foi ou não visitado
        self.visit = False
        # Inteiro que identifica a qual região o vértice pertence
        self.region = -1
        # Inteiro que identifica a demanda do vértice, correspondente à sua região
        self.demand = -1

    # Método que retorna a coordenada X do vértice
    def getCoordX(self):
        return self.coordX

    # Método que retorna a coordenada Y do vértice
    def getCoordY(self):
        return self.coordY

    # Método que retorna o Id do vértice
    def getId(self):
        return self.idNode
    
    # Método que retorna se o vértice pode ou não ser visitado
    def getVisit(self):
        return self.visit

    # Método de atualização do atributo visit 
    def setVisit(self, b):
        self.visit = b   

    # Método de atualização do atributo region
    def setRegion(self, r):
        self.region = r

    # Método de atualização do atributo demand
    def setDemand(self, d):
        self.demand = d

# Classe que representa uma aresta por um tupla de 2 vértices e a distância entre eles
class Edge:
    # Construtor da classe aresta
    def __init__(self, V1, V2, d):
        # Aresta representada por uma tupla de 2 vértices
        self.edge = (V1, V2)
        # Distância entre os 2 vértices(peso da aresta)
        self.distance = d

    # Método que retorna o peso da aresta
    def getDistance(self):
        return self.distance
    
    # Método que retorna a aresta
    def getEdge(self):
        return self.edge

# Classe que representa um veículo
class Vehicle:
    # Construtor da classe veículo
    def __init__(self, c, Id):
        # Inteiro que representa a capacidade do veículo
        self.capacity = c
        # Inteiro que identifica o veículo
        self.Id = Id
        # Lista de vértices visitados pelo veículo
        self.roteNodes = []
        # Distância total percorrida pelo veículo
        self.totalDistance = 0

    # Método que retorna o Id do véiculo
    def getId(self):
        return self.Id

    # Método que retorna a capacidade do veículo
    def getCapacity(self):
        return self.capacity

    # Método que retorna a distância total percorrida pelo veículo
    def getDistance(self):
        return self.totalDistance

    # Método de atualização do atributo capacity
    def setCapacity(self, quant):
        self.capacity = self.capacity - quant

    # Método de atualização do atributo totalDistance
    def setDistance(self, d):
        self.totalDistance -= d

# Função que calcula a distância euclidiana entre dois vértices       
def calculaDistancia(x1, y1, x2, y2):
    return float(math.sqrt(((x2-x1)**2)+((y2-y1)**2)))

# Importa grafo do arquivo filename, a vértice 1 é a origem/garagem dos veículos
def get_graph(filename):
    # Dicionário que conterá as informações sobre quantidade de veículos, quantidade de regiões, etc.(Auxilia na leitura do arquivo)
    graph_settings = dict()
    # Caminho do arquivo para leitura
    file_path = path.relpath(filename)

    with open(file_path, "r") as data_file:

        # leitura das configurações do problema
    
        last_reader_pos = data_file.tell()
        current_line = data_file.readline()

        while current_line != "NODE_COORD_SECTION\n":
            # Lê a linha formatada como CONFIGURAÇÃO : VALOR
            (key, val) = current_line.rsplit(" : ", 1)
            # Salva VALOR no dicionário usando CONFIGURAÇÃO como chave
            graph_settings[key] = val.rstrip("\n")

            current_line = data_file.readline()


            new_reader_pos = data_file.tell()
            # Checa se cursor se moveu para tratar EOF prematuro
            if last_reader_pos == new_reader_pos:
                raise EOFError("Atingiu EOF sem encontrar NODE_COORD_SECTION")
            else:
                last_reader_pos = new_reader_pos



        # Leitura das vértices e suas coordenadas

        last_reader_pos = data_file.tell()

        for i in range(int(graph_settings["DIMENSION"])):
            current_line = data_file.readline()

            (node_number, coord) = current_line.split(" ", 1)
            (coordx, coordy) = (coord.rstrip("\n")).split(" ")

            # Instância de um vértice para ser inserido na lista
            node = Node(int(coordx), int(coordy), int(node_number))

            # Inserção do vértice na lista de vértices
            Nodes.append(node)

            new_reader_pos = data_file.tell()
            # Checa se cursor se moveu para tratar EOF prematuro
            if last_reader_pos == new_reader_pos:
                raise EOFError("Atingiu EOF antes de ler coordenadas de todas vértices")
            else:
                last_reader_pos = new_reader_pos

        # Leitura dos sets

        current_line = data_file.readline()
        last_reader_pos = data_file.tell()

        if current_line != "SET_SECTION\n":
            raise RuntimeError("Esperado \"SET_SECTION\", mas foi lido \"{}\"".format(current_line))

        for i in range(int(graph_settings["SETS"])):
            current_line = data_file.readline()
            (current_set, nodes_in_set) = current_line.split(" ", 1)
            nodes_in_set = nodes_in_set.split(" ")

            # Setando as regiões a que cada vértice pertence
            for each_node in nodes_in_set:
                for i in Nodes:
                    if i.idNode == int(each_node):
                        i.region = current_set

            new_reader_pos = data_file.tell()
            # Checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todos os sets")
            else:
                last_reader_pos = new_reader_pos



        # Leitura das demandas

        graph_settings["DEMAND_TOTAL"] = int(0)

        current_line = data_file.readline()
        last_reader_pos = data_file.tell()
    
        if current_line != "DEMAND_SECTION\n":
            raise RuntimeError("Esperado \"DEMAND_SECTION\", mas foi lido \"{}\"".format(current_line))

        for i in range(int(graph_settings["SETS"])):
            current_line = data_file.readline()
            (current_set, current_demand) = (current_line.rstrip("\n")).split(" ", 1)
            # Guarda a quantidade de demanda total do grafo para efeito de controle
            graph_settings["DEMAND_TOTAL"] += int(current_demand)

            # Setando a demanda de cada vértice de acordo com a região a que ele pertence
            for i in Nodes:
                if(int(current_set) == int(i.region)):
                    i.demand = int(current_demand)

            new_reader_pos = data_file.tell()

            # Checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todas as demandas")
            else:
                last_reader_pos = new_reader_pos



        current_line = data_file.readline()
        if current_line != "EOF":
            raise RuntimeError("Esperado \"EOF\", mas foi lido \"{}\"".format(current_line))

    # Retorna o dicionário para auxiliar em outras funções do código
    return graph_settings

# Função que adiciona todas as arestas do grafo na lista de Arestas(Edges), à partir da lista de vértices(Nodes)
def add_Edge(graph_settings):
    i = 0
    j = 0
    # Percorre a lista de vértices(Nodes)
    while(i < int(graph_settings["DIMENSION"])):
        j = 0
        # Percorre a lista de vértices(Nodes)
        while(j < int(graph_settings["DIMENSION"])):   
            # Verifica se os dois vértices não pertencem a mesma região pois não é necessário ter arestas entre vértices de uma mesma região,
            # além de verificar se os vértices que se encontram na iteração de cada repetição não são os mesmos
            if i != j and Nodes[i].region != Nodes[j].region:
                # Distância entre os dois vértices
                distancia = calculaDistancia(Nodes[i].coordX, Nodes[i].coordY, Nodes[j].coordX, Nodes[j].coordY)
                # Instância de uma aresta
                aresta = Edge(int(Nodes[i].idNode), int(Nodes[j].idNode), float(distancia))
                # Inserção da aresta na lista de Arestas
                Edges.append(aresta)
            j += 1
        i += 1

# Função que adiciona a quantidade de veículos lidos do arquivo na lista de veículos(Vehicles)
def add_Vehicle(graph_settings):
    for i in range(int(graph_settings["VEHICLES"])):
        Vehicles.append(Vehicle(int(graph_settings["CAPACITY"]), int(i)))

# Função que percorre a lista de vértices imprimindo seus atributos
def print_Node():
    tam = len(Nodes)
    i = 0
    while(i < tam):
        print(Nodes[i].idNode, Nodes[i].coordX, Nodes[i].coordY, Nodes[i].visit, Nodes[i].region, Nodes[i].demand)
        i += 1

# Função que percorre a lista de veículos imprimindo seus atributos
def print_Vehicles():
    tamV = len(Vehicles)
    i = 0
    while(i < tamV):
        print("ID:", Vehicles[i].Id , "Capacidade restante:", Vehicles[i].capacity, "Rota dos vértices:", Vehicles[i].roteNodes, "Distância total percorrida:", Vehicles[i].totalDistance)
        i += 1

# Função que percorre a lista de arestas imprimindo seus atributos
def print_Edges():
    tam = len(Edges)
    i = 0
    while(i < tam):
        print(Edges[i].edge, Edges[i].distance)
        i += 1

# Função que verifica se ainda existe regiões possíveis de serem visitadas por determinado veículo(utilizada para controle)
# obs: A variável c recebida por parâmetro é um indice da lista de veículos
def exist_Region_Not_Visit(c):
    # variável que será retornada e indicará se existe ou não região possível de ser visitada
    exist = False
    i = 0
    tamN = len(Nodes)
    while(i < tamN):
        # Verifica se existe algum vértice pertencente a uma região que ainda não foi visitada e se a demanda do vértice
        # é possível de ser atendida pelo véiculo em questão
        if(Nodes[i].visit == False and Nodes[i].demand <= Vehicles[c].capacity):
            exist = True
        i += 1
    return exist

# Função que utiliza do algoritmo tsp Vizinho Mais Próximo com algumas modificações para solução do problema
def Nearest_Neighbor_Heuristic(graph_settings):
    e = 0
    # Tamanho da lista de arestas
    tamE = len(Edges)
    # Variável de controle que contém o peso da maior aresta do grafo
    maxDistance = 0
    # Procura e atribui à variável maxDistance o valor do peso da aresta de maior peso do grafo(obs: peso == distância)
    while(e < tamE):
        if(float(Edges[e].distance) > float(maxDistance)):
            maxDistance = float(Edges[e].distance)
        e += 1   
    # Tamanho da lista de vértices
    tamNodes = len(Nodes)    
    a = 0
    # Tamanho da lista de veículos
    tamVehicles = len(Vehicles)
    # Marca o vértice 1(origem/garagem) como visitado
    Nodes[0].visit = True
    # Percorre a lista de véículos
    while(a < tamVehicles):
        # Variável que contém a demanda total percorrida no momento pelo veículo em questão
        somDemand = int(0)
        # Lista de controle que contém todos os vértices que ainda não foram visitados, mas que a demanda é maior que a
        # capacidade atual do veículo em questão
        listAux = []
        # Variável que guarda o id do nó que será inserido na rota do veículo na iteração atual(obs: iniciando do vertice 1(origem/garagem))
        vInsert = int(1)
        # Variável que guarda o id do nó que foi inserido na rota do veículo na última iteração
        vInsertAux = int(1)
        # Adiciona o vértice 1(origem/garagem na rota do veículo), indicando a partida do veículo do vértice 1.
        Vehicles[a].roteNodes.append(int(1))
        i = 0
        # Enquanto existe região possível de ser visitada pelo veículo atual e a demanda total percorrida no momento pelo veículo não
        # seja maior ou igual à demanda total do grafo, dividido pela quantidade de veículos(obs: a segunda condição do while 
        # é para efeito de que todos os carros tentem entregar na média a mesma quantidade de demanda), procura um vértice para ser
        # inserido na rota do véículo. Caso o vértice encontrado ainda possa ser visitado, mas a sua demanda seja maior que a capacidade
        # atual do veículo, ele é inserido na lista auxiliar listAux, e será procurado o seguinte vértice mais próximo do último vértice
        # inserido na rota do veículo, até que a demanda do vértice encontrado seja possível de ser atendida pelo veículo.
        while(exist_Region_Not_Visit(a) == True and int(somDemand) < int(int(graph_settings["DEMAND_TOTAL"])/int(graph_settings["VEHICLES"]))):
            # Variável de controle que ajuda na comparação e identificação do vértice mais próximo do último vértice inserido na rota do veículo
            vMinDistance = float(maxDistance)
            j = 0
            # Percorre a lista de nós atualizando sempre o vértice mais próximo do último vértice a ser inserido na rota do veículo
            while(j < tamNodes):
                # Verifica se o id do último vértice inserido não é igual ao id do vértice da iteração,
                # também verifica se o vértice da iteração pode ser visitado, e se ele não está na lista de vértices
                # em que a demanda é maior que a capacidade atual do veículo
                if(int(Nodes[vInsertAux-1].idNode) != int(Nodes[j].idNode) and Nodes[j].visit == False and Nodes[j].idNode not in listAux):
                    # Verifica se o vértice da iteração atual tem menor distância para o último vértice inserido na rota do veículo
                    # em relação à menor distância encontrada no momento na iteração
                    if(float(vMinDistance) > calculaDistancia(int(Nodes[vInsertAux-1].coordX), int(Nodes[vInsertAux-1].coordY), int(Nodes[j].coordX), int(Nodes[j].coordY))):
                        # Atualiza menor distância
                        vMinDistance = calculaDistancia(int(Nodes[vInsertAux-1].coordX), int(Nodes[vInsertAux-1].coordY), int(Nodes[j].coordX), int(Nodes[j].coordY))
                        # Atualiza o vértice de menor distância em relação ao último vértice inserido na rota do veículo
                        vInsert = int(Nodes[j].idNode)
                j += 1
            
            # Verifica se o vértice encontrado(vértice mais próximo do último vértice a ser inserido na rota do véiculo) pode ser visitado,
            # e se a demanda dele é possível de ser atendida pelo veículo
            if(Nodes[vInsert-1].visit == False and Vehicles[a].capacity >= Nodes[vInsert-1].demand):
                # Insere o vértice na rota do veículo
                Vehicles[a].roteNodes.append(Nodes[vInsert-1].idNode)
                # Atualiza o último vértice a ser inserido na rota do veículo
                vInsertAux = vInsert
                # Atualiza a distância total percorrida pelo carro
                Vehicles[a].totalDistance += vMinDistance
                # Atualiza a demanda total atendida pelo carro
                somDemand += int(Nodes[vInsert-1].demand)
                r = 0
                # Percorre a lista de vértices atualizando todos os vértices de mesma região do vértice inserido na rota do veículo,
                # marcando-os também como visitados
                while(r < tamNodes):
                    # Verifica se o vértice da iteração pertence à mesma região do último vértice inserido na rota do veículo
                    if(Nodes[vInsert-1].region == Nodes[r].region):
                        # Atualiza o vértice como visitado
                        Nodes[r].visit = True
                    r += 1
                # Atualiza a variável de controle da distância, novamente para o valor do peso(distância) da aresta de maior peso,
                # para que possa ser encontrada a menor distância na próxima iteração
                vMinDistance = float(maxDistance)
                # Atualiza o vértice inserido na rota do veículo como visitado
                Nodes[vInsert-1].visit = True
                # Atualiza a capacidade atual do veículo, subtraindo da demanda do vértice inserido em sua rota
                Vehicles[a].capacity -= Nodes[vInsert-1].demand
            # Caso o vértice encontrado para ser inserido na rota do veículo ainda não tenha sido visitado,
            # mas a sua demanda seja maior que a capacidade atual do veículo, ele é inserido em uma lista de controle(listAux),
            # para que não possa mais ser selecionado para inserção na rota do veículo em questão
            else:
                # Vértice não visitado de demanda maior que a capacidade atual do veículo inserido na lista de controle
                listAux.append(Nodes[vInsert-1].idNode)
        
        # Variável que pega a posição do último vértice inserido na rota do veículo
        posFinal = len(Vehicles[a].roteNodes) - 1
        # Variável que pega o valor do id do último vértice inserido na rota do veículo
        idFinal = Vehicles[a].roteNodes[posFinal]
        # Atualiza a distância total percorrida pelo veículo, adicionando a distância do último vértice inserido em sua rota para a origem/garagem.
        Vehicles[a].totalDistance += calculaDistancia(int(Nodes[idFinal-1].coordX), int(Nodes[idFinal-1].coordY), int(Nodes[0].coordX), Nodes[0].coordY)
        # Final da rota do veículo, vértice 1 inserido no final da rota do veículo, indicando o retorno para a origem/garagem
        Vehicles[a].roteNodes.append(int(1))
        a += 1

# Calcula e retorna a somatória total da distância percorrida por todos os carros no grafo
def calcula_distancia_total():
    distanciaTotal = int(0)
    for i in Vehicles:
        distanciaTotal += i.totalDistance
    
    return distanciaTotal

def main():
    # Variável que armazena as informações contidas no dicionário de dados
    graph_settings = get_graph("./data/problemas-grupo1/problema1.txt")
    # Adiciona os veículos na lista de veículos
    add_Vehicle(graph_settings)
    # Adiciona as arestas na lista de arestas
    add_Edge(graph_settings)
    # Determina a rota de cada veículo, atendendo à todas as regiões
    Nearest_Neighbor_Heuristic(graph_settings)
    # Imprime a lista de veículos e seus atributos(id, capacidade restante, rota de vértices e distância total percorrida)
    print_Vehicles()
    # Imprime a lista de Vértices
    # print_Node()
    # Imprime a lista de Arestas
    # print_Edges()
    print("A distancia total percorrida pelos carros foi de :", calcula_distancia_total())
    
main()
