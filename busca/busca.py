import os

class Grafo:
    def __init__(self):
        # Inicializa um dicionário para armazenar as listas de adjacências das estações.
        self.adjacentes = {}

    def adiciona_aresta(self, origem, destino):
        # Adiciona uma conexão bidirecional entre duas estações.
        if origem not in self.adjacentes:
            self.adjacentes[origem] = []
        if destino not in self.adjacentes[origem]:
            self.adjacentes[origem].append(destino)
        
        if destino not in self.adjacentes:
            self.adjacentes[destino] = []
        if origem not in self.adjacentes[destino]:
            self.adjacentes[destino].append(origem)

    def imprime(self):
        # Imprime todas as estações e suas conexões diretas, evitando duplicatas.
        print("Grafo de Estações de Metrô:")
        for estacao, conexoes in self.adjacentes.items():
            conexoes_unicas = list(set(conexoes))
            print(f"{estacao} -> {', '.join(conexoes_unicas)}")

    def dfs(self, inicio, fim):
        # Executa uma busca em profundidade para encontrar um caminho do inicio ao fim.
        visitados = set()
        caminho = []
        if self._dfs_recursivo(inicio, fim, visitados, caminho):
            caminho.reverse()  # Inverte a ordem do caminho ao final da busca
            return caminho
        else:
            return []

    def _dfs_recursivo(self, atual, fim, visitados, caminho):
        # Função recursiva usada pela DFS para percorrer o grafo.
        if atual == fim:
            caminho.append(atual)
            return True
        visitados.add(atual)
        for vizinho in self.adjacentes.get(atual, []):
            if vizinho not in visitados:
                if self._dfs_recursivo(vizinho, fim, visitados, caminho):
                    caminho.append(atual)
                    return True
        return False

def conectar_baldeacoes(grafo, est_por_linha):
    # Conecta estações que aparecem em mais de uma linha.
    for estacao, linhas in est_por_linha.items():
        if len(linhas) > 1:
            for i in range(len(linhas)):
                chave_i = f"{estacao} - {linhas[i]}"
                for j in range(i + 1, len(linhas)):
                    chave_j = f"{estacao} - {linhas[j]}"
                    grafo.adiciona_aresta(chave_i, chave_j)
                    #print(f"Conectado {chave_i} com {chave_j}")

def cria_grafo():
    # Cria o grafo a partir de um arquivo de texto que lista as estações e linhas.
    grafo = Grafo()
    est_por_linha = {}
    todas_as_estacoes_por_linha = {}
    dir_atual = os.getcwd()
    file_path = os.path.join(dir_atual, 'googleMapsAPI', 'stations_list', 'metro_stations.txt')

    with open(file_path, 'r') as file:
        linha_atual = None
        for linha in file:
            linha = linha.strip()
            if linha.startswith("#"):
                linha_atual = linha.strip('#').strip()
            else:
                estacao = linha.split(" - ")[0].strip()
                chave_estacao = f"{estacao} - {linha_atual}"
                if estacao not in est_por_linha:
                    est_por_linha[estacao] = []
                est_por_linha[estacao].append(linha_atual)
                if linha_atual not in todas_as_estacoes_por_linha:
                    todas_as_estacoes_por_linha[linha_atual] = []
                todas_as_estacoes_por_linha[linha_atual].append(chave_estacao)

        # Conecta sequencialmente as estações dentro de cada linha
        for linha, estacoes in todas_as_estacoes_por_linha.items():
            for i in range(len(estacoes) - 1):
                grafo.adiciona_aresta(estacoes[i], estacoes[i + 1])

    # Adiciona conexões entre diferentes linhas para estações de baldeação.
    conectar_baldeacoes(grafo, est_por_linha)
    return grafo

# Criação e uso do grafo
g2 = cria_grafo()
caminho = g2.dfs("Estação Conceição - LINHA 1 AZUL", "Estação Saúde - LINHA 1 AZUL")
print("Caminho é:", caminho)

caminho2 = g2.dfs("Estação Sé - LINHA 3 VERMELHA", "Estação Faria Lima - LINHA 4 AMARELA")
print("Caminho do g2 é:", caminho2)
