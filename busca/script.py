import subprocess
import os

def executar_busca(origem, destino, modo):
    # Comando para executar busca.py
    comando = ['python3', 'busca.py']

    # Abrindo o processo
    with subprocess.Popen(comando, stdout=subprocess.PIPE, stderr=subprocess.STDOUT, stdin=subprocess.PIPE, text=True) as processo:
        # Enviando inputs para o processo
        processo.stdin.write(origem + '\n')
        processo.stdin.write(destino + '\n')
        processo.stdin.write(modo + '\n')
        processo.stdin.flush()

        # Recebendo a saída do processo e exibindo
        dados_saida = processo.stdout.readlines()

        # Escrevendo saída em um arquivo output-modo.txt dentro da pasta dados
        nome_arquivo = os.path.join("dados", f"output-{modo}.txt")  # Nome do arquivo com base no modo escolhido e no diretório "dados"
        with open(nome_arquivo, 'a') as arquivo:  # Abrindo em modo de adição ('a')
            arquivo.write(f"{origem}\n\n")
            arquivo.write(f"{destino}\n\n")

            # Adicionando custo e nós expandidos com o nome do método
            for linha in dados_saida:
                if "Caminho" not in linha:  # Ignorar linhas com o caminho
                    arquivo.write(linha)

            arquivo.write("\n\n")  # Adicionando espaços extras entre os resultados para separá-los

    print(f"Dados salvos em '{nome_arquivo}'.")

    # Chamar separacao.py para processar os dados
    subprocess.run(['python3', 'separacao.py', modo])

    # Chamar stem-plot.py para plotar os gráficos para os modos especificados
    subprocess.run(['python3', 'stem-plot.py', *["distância", "tempo", "avaliação"]])

def main():
    # Carregar as estações do arquivo
    with open("/home/yudiaramos/SP-subway-heuristic-search/googleMapsAPI/stations_list/metro_stations.txt", 'r') as arquivo_estacoes:
        estacoes = [linha.strip() for linha in arquivo_estacoes if linha.strip() and "Estacao" in linha]

    # Executa a busca para todas as combinações de origem e destino
    for origem in estacoes:
        for destino in estacoes:
            if origem != destino:  # Garantir que a origem e o destino sejam diferentes
                for modo in ["distância", "tempo", "avaliação"]:
                    # Verificar se a estação já foi incluída nos arquivos de saída
                    if not any(origem in linha for linha in open(f"dados/output-{modo}.txt").readlines()):
                        executar_busca(origem, destino, modo)

    print("Busca concluída.")

if __name__ == "__main__":
    main()

