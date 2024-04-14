import os
import json

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
            print(f"{estacao} -> {', '.join(f'{v} ({d}m)' for v, d in conexoes.items())}")

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

# Criação e uso do grafo
g = cria_grafo_dist()
g.imprime()  # Imprime o grafo completo com distâncias
caminho, dist = g.dfs("Estacao Conceicao", "Estacao Saude")
print("Caminho:", caminho)  # Imprime o caminho encontrado e a distância total
print("Distancia:", dist)

caminho2, dist2 = g.dfs("Estacao Conceicao", "Estacao Santos-Imigrantes")
print("Caminho:", caminho2)
print("Distancia:", dist2)
