import os
import matplotlib.pyplot as plt
import numpy as np

# Função para ler os valores do arquivo
def ler_valores(nome_arquivo):
    with open(nome_arquivo, 'r') as file:
        valores = [int(valor.strip()) for valor in file.readlines()]
    return valores

# Função para plotar os gráficos
def plotar_graficos(modo):
    # Montar os caminhos dos arquivos
    pasta_dados = "dados"
    arquivo_custos = os.path.join(pasta_dados, f"custos-{modo}.txt")
    arquivo_nos_expandidos = os.path.join(pasta_dados, f"nos_expandidos-{modo}.txt")

    # Ler os valores dos arquivos
    valores_custos = ler_valores(arquivo_custos)
    valores_nos_expandidos = ler_valores(arquivo_nos_expandidos)

    # Selecionar apenas os primeiros 50 valores para cada método
    dfs = valores_nos_expandidos[::3][:50]  # Valores para DFS (a cada 3 valores)
    bfs = valores_nos_expandidos[1::3][:50]  # Valores para BFS (a cada 3 valores, começando do segundo)
    a_star = valores_nos_expandidos[2::3][:50]  # Valores para A* (a cada 3 valores, começando do terceiro)

    # Configurar as barras
    barWidth = 0.25
    r1 = np.arange(len(dfs))
    r2 = [x + barWidth for x in r1]
    r3 = [x + barWidth for x in r2]

    # Plotar as barras
    plt.bar(r1, dfs, color='blue', width=barWidth, edgecolor='grey', label='DFS')
    plt.bar(r2, bfs, color='green', width=barWidth, edgecolor='grey', label='BFS')
    plt.bar(r3, a_star, color='red', width=barWidth, edgecolor='grey', label='A*')

    # Adicionar legendas
    plt.xlabel('Execução', fontweight='bold')
    plt.ylabel('Nós Expandidos', fontweight='bold')
    plt.title(f'Nós Expandidos por Execução - {modo.upper()}', fontweight='bold')
    plt.xticks([r + barWidth for r in range(len(dfs))], range(1, len(dfs) + 1))

    # Exibir a legenda e os gráficos
    plt.legend()
    plt.show()

if __name__ == "__main__":
    modos = ["distância", "tempo", "avaliação"]

    for modo in modos:
        plotar_graficos(modo)

