import json
import networkx as nx
import matplotlib.pyplot as plt
import subprocess
import os

starting_node = "Estacao Saude"
target_node = "Estacao Santa Cruz"

# file path
file_path = "../googleMapsAPI/output/distances.json"

# generate the heuristic file 
os.chdir("../googleMapsAPI/") 
python_interpreter = 'python3'
python_program = './heuristic.py'
subprocess.run(f'python3 {python_program} "{target_node}"', shell=True, check=True)

heuristic_path = "../googleMapsAPI/output/heuristics/" + target_node.replace(" ", "") + "_heuristic.json"

# create graph
G = nx.DiGraph()
 
def createGraph():
    # open json 
    with open(file_path, 'r') as f:
        data = json.load(f)
    
    # full graph
    for item in data:
        origin = item['origin'].split(', ')[0].strip()
        destination = item['destination'].split(', ')[0].strip()
        distance = item['real-distance']
        G.add_node(origin)
        G.add_node(destination)
        G.add_edge(origin, destination, weight=distance)
        G.add_edge(destination, origin, weight=distance)

def showPath(path):
    for i in range(len(path) - 1):
        print(path[i] + " ➡ ", end="")
    print(path[-1]) 

def dfs(starting_node, target_node):
    # search in graph
    dfs_path = list(nx.dfs_edges(G, source=starting_node))
    total_cost = 0
    path = [starting_node]
    for edge in dfs_path:
        total_cost += G[edge[0]][edge[1]]['weight']
        path.append(edge[1])
        if edge[1] == target_node:
            break
    showPath(path)
    print("Custo total do caminho:", total_cost)

def heuristic(origin, destination):
    with open(heuristic_path, 'r') as f:
        data = json.load(f)
    for item in data:
        current_station = item['station'].split(', ')[0].strip()
        if (current_station == origin):
            return item['heuristc']
    return 0

def AStar(starting_node, target_node):
    path = nx.astar_path(G, starting_node, target_node, 
                         heuristic=heuristic,
                         weight='weight')
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += G[path[i]][path[i+1]]['weight']

    showPath(path)
    print("Custo total do caminho:", total_cost)


def plotGraph():
    plt.figure(figsize=(16, 12))
    
    pos = nx.circular_layout(G)
    
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Graph Visualization with Edge Weights")
    plt.show()


createGraph()
dfs(starting_node, target_node)
print("========")
AStar(starting_node, target_node)
#plotGraph()
