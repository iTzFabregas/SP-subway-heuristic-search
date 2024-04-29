import os
import matplotlib.pyplot as plt
import sys

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

    # Separar os valores para cada método
    dfs = valores_nos_expandidos[::3]  # Valores para DFS (a cada 3 valores)
    bfs = valores_nos_expandidos[1::3]  # Valores para BFS (a cada 3 valores, começando do segundo)
    a_star = valores_nos_expandidos[2::3]  # Valores para A* (a cada 3 valores, começando do terceiro)

    # Plotar cada método em um gráfico separado
    plt.figure(figsize=(10, 6))

    # Gráfico para DFS
    plt.subplot(3, 1, 1)
    plt.plot(range(1, len(dfs) + 1), dfs, marker='o', color='blue')
    for x, y in enumerate(dfs, 1):
        plt.text(x, y, str(y), color='blue', ha='center', va='bottom')
    plt.title('DFS')
    plt.xlabel('Execução')
    plt.ylabel('Nós Expandidos')

    # Gráfico para BFS
    plt.subplot(3, 1, 2)
    plt.plot(range(1, len(bfs) + 1), bfs, marker='o', color='green')
    for x, y in enumerate(bfs, 1):
        plt.text(x, y, str(y), color='green', ha='center', va='bottom')
    plt.title('BFS')
    plt.xlabel('Execução')
    plt.ylabel('Nós Expandidos')

    # Gráfico para A*
    plt.subplot(3, 1, 3)
    plt.plot(range(1, len(a_star) + 1), a_star, marker='o', color='red')
    for x, y in enumerate(a_star, 1):
        plt.text(x, y, str(y), color='red', ha='center', va='bottom')
    plt.title('A*')
    plt.xlabel('Execução')
    plt.ylabel('Nós Expandidos')

    # Ajustar layout
    plt.tight_layout()

    # Exibir os gráficos
    plt.show()

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Por favor, forneça o modo como argumento (distância, tempo ou avaliação).")
        sys.exit(1)
    modo = sys.argv[1]
    plotar_graficos(modo)

