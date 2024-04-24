import json
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import os
import sys
import json
from collections import deque
import heapq
import subprocess

class Grafo:
    def __init__(self):
        # Inicializa um dicionário para armazenar a lista de adjacências.
        self.adjacentes = {}
        self.heuristics = {}

    def carrega_heuristicas(self, station):
        #chama o script que gera a heurística ()
        os.chdir("googleMapsAPI/")
        python_interpreter = 'python_3'
        python_program = './heuristic.py'
        subprocess.run(f'python3 {python_program} "{station}"', shell=True, check=True)

        file_path = "../googleMapsAPI/output/heuristics/" + station.replace(" ", "") + "_heuristic.json"
        with open(file_path, 'r') as file:
            data = json.load(file)
            for item in data:
                self.heuristics[item['station']] = {
                    'duration': item['heuristic-duration'],
                    'distance': item['heuristic-distance'],
                    'time'    : 0
                }

    def adiciona_aresta(self, origem, destino, distancia):
        # Adiciona uma aresta bidirecional com a distância entre os nós ao grafo.
        if origem not in self.adjacentes:
            self.adjacentes[origem] = {}
        self.adjacentes[origem][destino] = distancia

        if destino not in self.adjacentes:
            self.adjacentes[destino] = {}
        self.adjacentes[destino][origem] = distancia

    def a_star(self, start, goal, heuristic_type='distance'):
        open_set = []
        heapq.heappush(open_set, (0 + self.heuristics[start][heuristic_type], start))
        came_from = {}
        cost_so_far = {start: 0}
        expanded_nodes = 0

        while open_set:
            #expande o nó com maior prioridade (menor custo com heuristica)
            current = heapq.heappop(open_set)[1]
            expanded_nodes += 1

            if current == goal:
                # chegou no destino, finaliza
                break

            for neighbor in self.adjacentes[current]:
                #para cada vizinho do nó atual, calcula o custo
                new_cost = cost_so_far[current] + self.adjacentes[current][neighbor]
                if neighbor not in cost_so_far or new_cost < cost_so_far[neighbor]:
                    cost_so_far[neighbor] = new_cost
                    priority = new_cost + self.heuristics[neighbor][heuristic_type] #calcula custo com a heuristica
                    heapq.heappush(open_set, (priority, neighbor)) #coloca na lista de prioridade
                    came_from[neighbor] = current

        return came_from, cost_so_far, expanded_nodes

    def imprime(self):
        # Imprime todas as conexões do grafo formatadas para fácil leitura.
        print("Grafo de Estações de Metrô:")
        for estacao, conexoes in self.adjacentes.items():
            print(f"{estacao} -> {', '.join(f'{v} ({d})' for v, d in conexoes.items())}")

    def bfs(self, inicio, fim):
        # Executa uma busca em largura (BFS) para encontrar um caminho e a distância total.
        fila = deque([(inicio, 0)])  # Cada entrada da fila é uma tupla (nó, distância acumulada)
        visitados = {inicio: (None, 0)}  # Dicionário para rastrear de onde viemos e a distância acumulada
        expanded = 0

        while fila:
            atual, dist_atual = fila.popleft()
            expanded +=1
            if atual == fim:
                break
            for vizinho, dist in self.adjacentes[atual].items():
                nova_dist = dist_atual + dist
                if vizinho not in visitados or nova_dist < visitados[vizinho][1]:
                    fila.append((vizinho, nova_dist))
                    visitados[vizinho] = (atual, nova_dist)  # Guarda de onde viemos para este vizinho e a distância acumulada

        if fim not in visitados:
            return [], 0, expanded  # Retorna lista vazia se não há caminho

        # Reconstruir o caminho a partir do fim até o início e calcular a distância total
        caminho = []
        dist_total = 0
        passo = fim
        while passo is not None:
            caminho.append(passo)
            passo, dist_passo = visitados[passo]
            if passo is not None:
                dist_total += self.adjacentes[passo][caminho[-1]]  # Soma a distância do passo atual ao próximo nó no caminho
        caminho.reverse()

        return caminho, dist_total, expanded

    def dfs(self, inicio, fim):
        # Executa uma busca em profundidade (DFS) para encontrar um caminho e a soma das distâncias.
        visitados = set()
        caminho = []
        expanded = [0]
        dist_total = self._dfs_recursivo(inicio, fim, visitados, caminho, 0, expanded)
        if dist_total is not None:
            caminho.reverse()  # Inverte a ordem do caminho ao final da busca
            return caminho, dist_total, expanded[0]
        else:
            return [], 0, expanded[0]

    def _dfs_recursivo(self, atual, fim, visitados, caminho, dist_acumulada, expanded):
        # Auxiliar recursiva da DFS que realiza a busca e acumula a distância.
        if atual == fim:
            caminho.append(atual)
            return dist_acumulada
        visitados.add(atual)
        expanded[0] +=1
        for vizinho, distancia in self.adjacentes.get(atual, {}).items():
            if vizinho not in visitados:
                resultado = self._dfs_recursivo(vizinho, fim, visitados, caminho, dist_acumulada + distancia, expanded)
                if resultado is not None:
                    caminho.append(atual)
                    return resultado
        return None

def ler_distancias():
    # Lê um arquivo JSON contendo as distâncias entre as estações e retorna um dicionário.
    dir_atual = os.getcwd()
    file_json = os.path.join(dir_atual, 'googleMapsAPI','output', 'distances.json')
    with open(file_json, 'r') as file:
        dados = json.load(file)
    distancias = {}
    for item in dados:
        origem = item["origin"].split(" - ")[0]  # Remove a localização adicional no nome da estação
        destino = item["destination"].split(" - ")[0]
        dist = item["real-distance"]
        distancias[(origem, destino)] = dist
    return distancias

def cria_grafo_dist():
    # Cria o grafo a partir das distâncias lidas do JSON.
    grafo = Grafo()
    distancias = ler_distancias()
    for (origem, destino), dist in distancias.items():
        grafo.adiciona_aresta(origem, destino, dist)
    return grafo


def ler_duracoes():
    # Lê um arquivo JSON contendo os tempos de duração entre as estações e retorna um dicionário.
    dir_atual = os.getcwd()
    file_json = os.path.join(dir_atual, 'googleMapsAPI', 'output', 'durations.json')
    with open(file_json, 'r') as file:
        dados = json.load(file)
    duracoes = {}
    for item in dados:
        if "origin" in item and "destination" in item and "real-duration" in item:
            origem = item["origin"].split(" - ")[0]
            destino = item["destination"].split(" - ")[0]
            duracao = item["real-duration"]
            duracoes[(origem, destino)] = duracao
        else:
            print("Erro: Item faltando dados necessários:", item)
    return duracoes

def cria_grafo_duracao():
    # Cria o grafo a partir das durações lidas do JSON.
    grafo = Grafo()
    duracoes = ler_duracoes()
    for (origem, destino), duracao in duracoes.items():
        grafo.adiciona_aresta(origem, destino, duracao)
    return grafo


def ler_avaliacoes():
    # Lê o arquivo JSON com as avaliações das estações e retorna um dicionário.
    dir_atual = os.getcwd()
    file_json = os.path.join(dir_atual, 'googleMapsAPI', 'output', 'ratings.json')
    with open(file_json, 'r') as file:
        dados = json.load(file)
    avaliacoes = {item["real_station"]: item["rating"] for item in dados}
    return avaliacoes

def cria_grafo_duracao_avaliacao():
    grafo = Grafo()
    duracoes = ler_duracoes()
    avaliacoes = ler_avaliacoes()
    coef_tempo = 1.0  # Coeficiente para o tempo
    coef_avaliacao = 3.5  # Coeficiente para a avaliação (maior impacto de avaliações mais altas)

    for (origem, destino), duracao in duracoes.items():
        if origem in avaliacoes and destino in avaliacoes:
            media_avaliacoes = (avaliacoes[origem] + avaliacoes[destino]) / 2
            peso = coef_tempo * duracao + coef_avaliacao * (5 - media_avaliacoes)  # Ajuste para que maior avaliação diminua o peso
        else:
            peso = coef_tempo * duracao  # Caso não haja avaliação, usa apenas a duração
        grafo.adiciona_aresta(origem, destino, peso)
    return grafo

def reconstruir_caminho(came_from, start, goal):
    current = goal
    path = []
    while current != start:
        path.append(current)
        current = came_from[current]
    path.append(start)
    path.reverse()
    return path

origem = input("Escreva a estação de origem: ")
destino = input("Escreva a estação de destino: ")
modo = input("Escolha o modo de busca (distância, tempo ou avaliação): ")
#Criação e uso do grafo
if modo == 'distância':
    g = cria_grafo_dist()
    print("Modo melhor distância escolhido!")

elif modo == 'tempo':
    g = cria_grafo_duracao()
    print("Modo melhor tempo escolhido!")

elif modo == 'avaliação':
    g = cria_grafo_duracao_avaliacao()
    print("Modo melhor avaliação escolhido!")

else:
    print("Modo não existente")
    sys.exit()

g.carrega_heuristicas(destino)

origem += ", Sao Paulo, Brasil"
destino += ", Sao Paulo, Brasil"

print("\n DFS: ")
caminho, dist, expandidos = g.dfs(origem, destino)
print("Caminho dfs:", caminho)
print("Custo dfs:", dist)
print("Nós Expandidos:", expandidos)

print("\n BFS: ")
caminho, dist, expandidos = g.bfs(origem, destino)
print("Caminho bfs:", caminho)
print("Custo bfs:", dist)
print("Nós Expandidos:", expandidos)

print("\n A*:")
if modo == 'distância':
    came_from, costs, nodes_expanded = g.a_star(origem, destino, 'distance')

elif modo == 'tempo':
    came_from, costs, nodes_expanded = g.a_star(origem, destino, 'duration')

else:
    came_from, costs, nodes_expanded = g.a_star(origem, destino, 'time')

path = reconstruir_caminho(came_from, origem, destino)
print('Caminho A*:', path)
print('Custo A*:', costs[destino])
print('Nós expandidos:', nodes_expanded)

os.chdir('output/heuristics')
subprocess.run('rm *.json', shell=True, check=True)
