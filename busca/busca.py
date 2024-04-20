import os
import json
from collections import deque

class Grafo:
    def __init__(self):
        # Inicializa um dicionário para armazenar a lista de adjacências.
        self.adjacentes = {}

    def adiciona_aresta(self, origem, destino, distancia):
        # Adiciona uma aresta bidirecional com a distância entre os nós ao grafo.
        if origem not in self.adjacentes:
            self.adjacentes[origem] = {}
        self.adjacentes[origem][destino] = distancia
        
        if destino not in self.adjacentes:
            self.adjacentes[destino] = {}
        self.adjacentes[destino][origem] = distancia

    def imprime(self):
        # Imprime todas as conexões do grafo formatadas para fácil leitura.
        print("Grafo de Estações de Metrô:")
        for estacao, conexoes in self.adjacentes.items():
            print(f"{estacao} -> {', '.join(f'{v} ({d})' for v, d in conexoes.items())}")

    def bfs(self, inicio, fim):
        # Executa uma busca em largura (BFS) para encontrar um caminho e a distância total.
        fila = deque([(inicio, 0)])  # Cada entrada da fila é uma tupla (nó, distância acumulada)
        visitados = {inicio: (None, 0)}  # Dicionário para rastrear de onde viemos e a distância acumulada

        while fila:
            atual, dist_atual = fila.popleft()
            if atual == fim:
                break
            for vizinho, dist in self.adjacentes[atual].items():
                nova_dist = dist_atual + dist
                if vizinho not in visitados or nova_dist < visitados[vizinho][1]:
                    fila.append((vizinho, nova_dist))
                    visitados[vizinho] = (atual, nova_dist)  # Guarda de onde viemos para este vizinho e a distância acumulada

        if fim not in visitados:
            return [], 0  # Retorna lista vazia se não há caminho

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

        return caminho, dist_total

    def dfs(self, inicio, fim):
        # Executa uma busca em profundidade (DFS) para encontrar um caminho e a soma das distâncias.
        visitados = set()
        caminho = []
        dist_total = self._dfs_recursivo(inicio, fim, visitados, caminho, 0)
        if dist_total is not None:
            caminho.reverse()  # Inverte a ordem do caminho ao final da busca
            return caminho, dist_total
        else:
            return [], 0

    def _dfs_recursivo(self, atual, fim, visitados, caminho, dist_acumulada):
        # Auxiliar recursiva da DFS que realiza a busca e acumula a distância.
        if atual == fim:
            caminho.append(atual)
            return dist_acumulada
        visitados.add(atual)
        for vizinho, distancia in self.adjacentes.get(atual, {}).items():
            if vizinho not in visitados:
                resultado = self._dfs_recursivo(vizinho, fim, visitados, caminho, dist_acumulada + distancia)
                if resultado is not None:
                    caminho.append(atual)
                    return resultado
        return None

def ler_distancias():
    # Lê um arquivo JSON contendo as distâncias entre as estações e retorna um dicionário.
    dir_atual = os.getcwd()
    file_json = os.path.join(dir_atual, 'googleMapsAPI', 'dist.json')
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
    avaliacoes = {item["station_real"]: item["rating"] for item in dados}
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

# Criação e uso do grafo
g = cria_grafo_dist()
#g.imprime()  # Imprime o grafo completo com distâncias
caminho, dist = g.dfs("Estacao Conceicao", "Estacao Santos-Imigrantes")
#print("Caminho:", caminho)
#print("Distancia:", dist)

caminho, dist = g.bfs("Estacao Conceicao", "Estacao Santos-Imigrantes")
#print("Caminho:", caminho)
#print("Distancia:", dist)

print("busca baseada no tempo de viagem!!!")
g2 = cria_grafo_duracao()
#g2.imprime()
caminho2, time2 = g2.dfs("Estação Luz", "Estação Capão Redondo")
print("Caminho:", caminho2)
print("Tempo:", time2, "seg")
caminho2, time2 = g2.bfs("Estação Luz", "Estação Capão Redondo")
print("Caminho:", caminho2)
print("Tempo:", time2, "seg")

print("busca baseada no tempo de viagem e na avaliação da estação!!!")
g3 = cria_grafo_duracao_avaliacao()
#g3.imprime()
caminho3, time3 = g3.bfs("Estação Luz", "Estação Capão Redondo")
print("Caminho:", caminho3)
print("Tempo:", time3, "seg")