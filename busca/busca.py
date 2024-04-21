import json
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import os

# stations entry
starting_node = "Estacao Saude"
target_node = "Estacao Santa Cruz"

# file path
distances_file_path = "../googleMapsAPI/output/distances.json"
durations_file_path = "../googleMapsAPI/output/durations.json"
ratings_file_path = "../googleMapsAPI/output/ratings.json"

# generate the heuristic file 
os.chdir("../googleMapsAPI/") 
python_interpreter = 'python3'
python_program = './heuristic.py'
subprocess.run(f'python3 {python_program} "{target_node}"', shell=True, check=True)

heuristic_path = "../googleMapsAPI/output/heuristics/" + target_node.replace(" ", "") + "_heuristic.json"

# create graph
G_distance = nx.DiGraph()
G_duration = nx.DiGraph()
G_rating = nx.DiGraph()
 
def createGraph():
    # open json 
    with open(distances_file_path, 'r') as f:
        data = json.load(f)
    
    # full graph
    for item in data:
        origin = item['origin'].split(', ')[0].strip()
        destination = item['destination'].split(', ')[0].strip()
        distance = item['real-distance']
        G_distance.add_node(origin)
        G_distance.add_node(destination)
        G_distance.add_edge(origin, destination, weight=distance)
        G_distance.add_edge(destination, origin, weight=distance)

def showFinalPath(path):
    for i in range(len(path) - 1):
        print(path[i] + " ➡ ", end="")
    print(path[-1]) 

def dfs(starting_node, target_node):
    # search in graph
    dfs_path = list(nx.dfs_edges(G_distance, source=starting_node))
    total_cost = 0
    path = [starting_node]
    for edge in dfs_path:
        total_cost += G_distance[edge[0]][edge[1]]['weight']
        path.append(edge[1])
        if edge[1] == target_node:
            break
    showFinalPath(path)
    print("Custo total do caminho:", total_cost)
    return path

def heuristic(origin, destination):
    with open(heuristic_path, 'r') as f:
        data = json.load(f)
    for item in data:
        current_station = item['station'].split(', ')[0].strip()
        if (current_station == origin):
            return item['heuristic-distance']
    return 0

def AStar(starting_node, target_node):
    path = nx.astar_path(G_distance, starting_node, target_node, 
                         heuristic=heuristic,
                         weight='weight')
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += G_distance[path[i]][path[i+1]]['weight']

    showFinalPath(path)
    print("Custo total do caminho:", total_cost)
    return path


def plotGraph(path):
    plt.figure(figsize=(16, 12))
    
    pos = nx.circular_layout(G_distance)
   
    nx.draw_networkx_nodes(G_distance, pos, nodelist=path, node_size=500, node_color='skyblue')
    edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(G_distance, pos, edgelist=edges, edge_color='red', width=2)
    nx.draw_networkx_labels(G_distance, pos, font_size=8)
    edge_labels = nx.get_edge_attributes(G_distance, 'weight')
    nx.draw_networkx_edge_labels(G_distance, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Graph Visualization with Path Highlighted")
    plt.show()

createGraph()
print("BUSCA NAO INFORMADA")
dfs_path = dfs(starting_node, target_node)
print("================================")
print("BUSCA INFORMADA")
astar_path = AStar(starting_node, target_node)

#plotGraph(dfs_path)
#plotGraph(astar_path)
