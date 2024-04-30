import os
import matplotlib.pyplot as plt
import numpy as np

# Função para ler os valores do arquivo
def ler_valores(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        valores = [int(valor.strip()) for valor in file.readlines()]
    return valores

# Função para calcular a média dos valores
def calcular_media(valores):
    return sum(valores) / len(valores) if valores else 0

# Função para plotar os gráficos
def plotar_graficos(modo):
    # Montar os caminhos dos arquivos
    pasta_dados = "dados"
    arquivo_custos = os.path.join(pasta_dados, f"custos-{modo}.txt")
    arquivo_nos_expandidos = os.path.join(pasta_dados, f"nos_expandidos-{modo}.txt")

    # Ler os valores dos arquivos
    valores_nos_expandidos = ler_valores(arquivo_nos_expandidos)

    # Calcular as médias dos valores para cada método de busca
    dfs = calcular_media(valores_nos_expandidos[::3])  # Média para DFS (a cada 3 valores)
    bfs = calcular_media(valores_nos_expandidos[1::3])  # Média para BFS (a cada 3 valores, começando do segundo)
    a_star = calcular_media(valores_nos_expandidos[2::3])  # Média para A* (a cada 3 valores, começando do terceiro)

    # Configurar as barras
    methods = ['DFS', 'BFS', 'A*']
    barWidth = 0.4
    r = np.arange(len(methods))

    # Plotar as barras
    plt.bar(r, [dfs, bfs, a_star], color=['blue', 'green', 'red'], width=barWidth, edgecolor='grey')

    # Adicionar legendas
    plt.xlabel('Método de Busca', fontweight='bold')
    plt.ylabel('Média de Nós Expandidos', fontweight='bold')
    plt.title(f'Média de Nós Expandidos por Método de Busca - {modo.upper()}', fontweight='bold')
    plt.xticks([r for r in range(len(methods))], methods)

    # Exibir os gráficos
    plt.show()

if __name__ == "__main__":
    modos = ["distância", "tempo", "avaliação"]

    for modo in modos:
        plotar_graficos(modo)

