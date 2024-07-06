from flask import Flask, request, jsonify
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

    # get place-id
    place_list = graph.returnInfo(astar_path)

    return([astar_path_formatted, round(astar_cost/60), place_list])

@app.route('/g2')
# Viagem com menor caminho percorrido
def graph2():
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

    # get place-id 
    place_list = graph.returnInfo(astar_path)

    return([astar_path_formatted, round(astar_cost/1000), place_list])

@app.route('/g3')
# Viagem com maior média das avaliações
def graph3():
    WEIGHT = 'RATING'

    origin = request.args.get('s1')  # obtém o valor do parâmetro 's1' que representa a origem
    destination = request.args.get('s2')  # obtém o valor do parâmetro 's2' que representa o destino

    origin = formatString(origin)
    destination = formatString(destination)

    # create graph different from others graphs
    graph_object = graph.createRatingsGraph(WEIGHT)

    # search using A*   
    travel_info = [origin, destination]
    max_weight_path, max_weight_cost = graph.findHeaviestPath(graph_object, travel_info)

    number_of_edges = len(max_weight_path) - 1
    max_weight_cost = max_weight_cost / number_of_edges 
    max_weight_cost_formatted = round(max_weight_cost, 2)
    
    # path transformed to string
    max_weight_path_formatted = graph.returnFinalPath(max_weight_path)

    # get place-id 
    place_list = graph.returnInfo(max_weight_path)

    return([max_weight_path_formatted, max_weight_cost_formatted, place_list])

@app.route('/g4')
# Viagem com maior número de estações percorridas
def graph4():
    WEIGHT = 'DISTANCE'

    origin = request.args.get('s1')  # obtém o valor do parâmetro 's1' que representa a origem
    destination = request.args.get('s2')  # obtém o valor do parâmetro 's2' que representa o destino

    origin = formatString(origin)
    destination = formatString(destination)

    # create graph
    graph_object = graph.createGraph(WEIGHT)

    # search using A*   
    travel_info = [origin, destination]
   
    longest_path, total_cost = graph.findLongestPath(graph_object, travel_info)
    
    longest_path_formatted = graph.returnFinalPath(longest_path)

    # get place-id 
    place_list = graph.returnInfo(longest_path)

    return([longest_path_formatted, total_cost, place_list])

@app.route('/get-json/<filename>', methods=['GET'])
def get_json(filename):
    try:
        # Baixar o arquivo do S3
        response = s3_client.get_object(Bucket=BUCKET_NAME, Key=filename)
        content = response['Body'].read().decode('utf-8')
        json_content = json.loads(content)
        return jsonify(json_content)
    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(debug=True)
