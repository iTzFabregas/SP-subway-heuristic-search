import re
import os
import sys

def extrair_nos_expandidos(arquivo_entrada, arquivo_saida, modo):
    # Padrão para encontrar os números dos nós expandidos
    padrao_nos_expandidos = re.compile(r'\bNós Expandidos\b: (\d+)')

    # Lista para armazenar os valores dos nós expandidos
    nos_expandidos = []

    # Caminho para o arquivo de entrada
    caminho_arquivo_entrada = os.path.join("dados", arquivo_entrada)

    # Abrir arquivo de entrada e procurar por padrões
    with open(caminho_arquivo_entrada, 'r') as entrada:
        for linha in entrada:
            # Procurar por padrões de nós expandidos
            resultado = padrao_nos_expandidos.search(linha)
            if resultado:
                nos_expandidos.append(resultado.group(1))

    # Caminho para o arquivo de saída
    caminho_arquivo_saida = os.path.join("dados", arquivo_saida)

    # Escrever os valores dos nós expandidos em um novo arquivo
    with open(caminho_arquivo_saida, 'w') as saida:
        for valor in nos_expandidos:
            saida.write(f"{valor}\n")

    print(f"Os valores dos nós expandidos foram escritos em {caminho_arquivo_saida} com sucesso!")

def extrair_custos(arquivo_entrada, arquivo_saida, modo):
    # Padrão para encontrar os números dos custos
    padrao_custos = re.compile(r'\bCusto\b: (\d+)')

    # Lista para armazenar os valores dos custos
    custos = []

    # Caminho para o arquivo de entrada
    caminho_arquivo_entrada = os.path.join("dados", arquivo_entrada)

    # Abrir arquivo de entrada e procurar por padrões
    with open(caminho_arquivo_entrada, 'r') as entrada:
        for linha in entrada:
            # Procurar por padrões de custos
            resultado = padrao_custos.search(linha)
            if resultado:
                custos.append(resultado.group(1))

    # Caminho para o arquivo de saída
    caminho_arquivo_saida = os.path.join("dados", arquivo_saida)

    # Escrever os valores dos custos em um novo arquivo
    with open(caminho_arquivo_saida, 'w') as saida:
        for valor in custos:
            saida.write(f"{valor}\n")

    print(f"Os valores dos custos foram escritos em {caminho_arquivo_saida} com sucesso!")

def escolher_arquivo(modo):
    if modo.lower() not in ['distância', 'tempo', 'avaliação']:
        print("Modo de busca inválido. Por favor, escolha entre 'distância', 'tempo' ou 'avaliação'.")
        return
    arquivo_entrada = f"output-{modo.lower()}.txt"
    arquivo_saida_nos_expandidos = f"nos_expandidos-{modo.lower()}.txt"
    arquivo_saida_custos = f"custos-{modo.lower()}.txt"

    if modo.lower() == 'distância':
        extrair_nos_expandidos(arquivo_entrada, arquivo_saida_nos_expandidos, modo)
        extrair_custos(arquivo_entrada, arquivo_saida_custos, modo)
    elif modo.lower() == 'tempo':
        extrair_nos_expandidos(arquivo_entrada, arquivo_saida_nos_expandidos, modo)
        extrair_custos(arquivo_entrada, arquivo_saida_custos, modo)
    elif modo.lower() == 'avaliação':
        extrair_nos_expandidos(arquivo_entrada, arquivo_saida_nos_expandidos, modo)
        extrair_custos(arquivo_entrada, arquivo_saida_custos, modo)

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Por favor, forneça o modo como argumento (distância, tempo ou avaliação).")
        sys.exit(1)
    modo = sys.argv[1]
    escolher_arquivo(modo)

