import networkx as nx
import random
import tsp
from matplotlib import pyplot as plt
from os import path


# importa grafo do arquivo filename, a vértice 1 é a garagem dos veículos
def get_graph(filename):
    graph = nx.Graph()
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

            graph.add_node(int(node_number), pos = (int(coordx), int(coordy)))


            new_reader_pos = data_file.tell()
            # checa se cursor se moveu para tratar EOF prematuro
            if last_reader_pos == new_reader_pos:
                raise EOFError("Atingiu EOF antes de ler coordenadas de todas vértices")
            else:
                last_reader_pos = new_reader_pos


        # leitura dos sets

        graph_settings["SETS_SETTINGS"] = dict()
        graph_settings["NODE_SET"] = [None] * (int(graph_settings["DIMENSION"]) + 1)
        graph_settings["SET_COLOR"] = [None] * (int(graph_settings["SETS"]))
        graph_settings["NODE_COLOR"] = [None] * (int(graph_settings["DIMENSION"]))

        current_line = data_file.readline()
        last_reader_pos = data_file.tell()

        if current_line != "SET_SECTION\n":
            raise RuntimeError("Esperado \"SET_SECTION\", mas foi lido \"{}\"".format(current_line))

        for i in range(int(graph_settings["SETS"])):
            current_line = data_file.readline()
            (current_set, nodes_in_set) = current_line.split(" ", 1)
            nodes_in_set = nodes_in_set.split(" ")

            # queremos uma lista de vértices para cada set
            graph_settings["SETS_SETTINGS"][current_set]= {"NODES": list()}
            graph_settings["SET_COLOR"][i] = int(random.random() * 0xFFFFFF)

            for each_node in nodes_in_set:
                graph_settings["SETS_SETTINGS"][current_set]["NODES"].append(int(each_node))
                # se each_node == -1, significa que já foram lidos todos desse set
                if int(each_node) != -1:
                    graph_settings["NODE_COLOR"][(int(each_node) - 1)] = graph_settings["SET_COLOR"][i]
                    graph_settings["NODE_SET"][int(each_node)] = int(current_set)

        
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
            graph_settings["SETS_SETTINGS"][current_set]["DEMAND"] = current_demand


            new_reader_pos = data_file.tell()

            # checa se o cursor se moveu para tratar EOF prematuro
            if new_reader_pos == last_reader_pos:
                raise EOFError("Atingiu EOF antes de ler todas as demandas")
            else:
                last_reader_pos = new_reader_pos

    # tam = len(Are    # tam = len(Arestas)
    # i = 0
    # while(i < tam):
    #     print(Arestas[i].edge, Arestas[i].distance)
    #     i += 1stas)
    # i = 0
    # while(i < tam):
    #     print(Arestas[i].edge, Arestas[i].distance)
    #     i += 1

        current_line = data_file.readline()
        if current_line != "EOF":
            raise RuntimeError("Esperado \"EOF\", mas foi lido \"{}\"".format(current_line))



        return (graph, graph_settings)



def main():
    (graph, graph_settings) = get_graph("./data/problemas-grupo1/problema7.txt")
    pos = nx.get_node_attributes(graph, "pos")
    a = 0
    for i in range(int(graph_settings["DIMENSION"])):
        a = a + 1
        n = 1
        for i in range(int(graph_settings["DIMENSION"])):
            if (n != a):
                graph.add_edges_from([(a,n)])
                n = n + 1
    nx.draw(graph, pos, node_color = graph_settings["NODE_COLOR"])
    plt.show()

    print(graph_settings)


main()