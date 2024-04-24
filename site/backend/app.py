from flask import Flask, request
from flask_cors import CORS
from unidecode import unidecode
import busca as graph 

app = Flask(__name__)
CORS(app)

def formatString(text):
    return unidecode(text).title().strip()

@app.route('/')
def index():
    return 'Tem nada aqui não!'

@app.route('/g1')
# Viagem com menor duração
def graph1():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # a duração total
    WEIGHT = 'DURATION'

    origin = request.args.get('s1')  # obtém o valor do parâmetro 's1' que representa a origem
    destination = request.args.get('s2')  # obtém o valor do parâmetro 's2' que representa o destino

    origin = formatString(origin)
    destination = formatString(destination)

    # create graph
    graph_object = graph.createGraph(WEIGHT)

    # search using A*   
    travel_info = [origin, destination]
    astar_path, astar_cost = graph.AStar(graph_object, WEIGHT, travel_info) 
    
    # path transformed to string
    astar_path_formatted = graph.returnFinalPath(astar_path)

    return astar_path_formatted 

@app.route('/g2')
# Viagem com menor caminho percorrido
def graph2():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # a distancial total
    WEIGHT = 'DISTANCE'

    origin = request.args.get('s1')  # obtém o valor do parâmetro 's1' que representa a origem
    destination = request.args.get('s2')  # obtém o valor do parâmetro 's2' que representa o destino

    origin = formatString(origin)
    destination = formatString(destination)

    # create graph
    graph_object = graph.createGraph(WEIGHT)

    # search using A*   
    travel_info = [origin, destination]
    astar_path, astar_cost = graph.AStar(graph_object, WEIGHT, travel_info) 
    
    # path transformed to string
    astar_path_formatted = graph.returnFinalPath(astar_path)

    return(astar_path_formatted)

@app.route('/g3')
# Viagem com maior média das avaliações
def graph3():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # a avaliação media final
    return(request.args)

@app.route('/g4')
# Viagem com maior número de estações percorridas
def graph4():
    # o ideial é retornar:
        # a lista com as estações do caminho
        # o numero de esações que tem no caminho
        # o place-id das estações
        # o numero maz de estações obtido
    return(request.args)


if __name__ == '__main__':
    app.run(debug=True)
