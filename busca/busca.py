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
 
def createGraph(graph):
    # open json 
    with open(distances_file_path, 'r') as f:
        data = json.load(f)
    
    # full graph
    for item in data:
        origin = item['origin'].split(', ')[0].strip()
        destination = item['destination'].split(', ')[0].strip()
        distance = item['real-distance']
        # take the last element of itens and convert to flaot 
        weight_key = list(item.keys())[-1]
        weight = float(item[weight_key])
        
        graph.add_node(origin)
        graph.add_node(destination)
        graph.add_edge(origin, destination, weight=weight)
        graph.add_edge(destination, origin, weight=weight)

def showFinalPath(path):
    for i in range(len(path) - 1):
        print(path[i] + " ➡ ", end="")
    print(path[-1]) 

def dfs(graph):
    # search in graph
    dfs_path = list(nx.dfs_edges(graph, source=starting_node))
    total_cost = 0
    path = [starting_node]
    for edge in dfs_path:
        total_cost += graph[edge[0]][edge[1]]['weight']
        path.append(edge[1])
        if edge[1] == target_node:
            break

    return path, total_cost

def heuristic(origin, destination):
    with open(heuristic_path, 'r') as f:
        data = json.load(f)
    for item in data:
        current_station = item['station'].split(', ')[0].strip()
        if (current_station == origin):
            return item['heuristic-distance']
    return 0

def AStar(graph):
    path = nx.astar_path(graph, starting_node, target_node, 
                         heuristic=heuristic,
                         weight='weight')
    total_cost = 0
    for i in range(len(path) - 1):
        total_cost += graph[path[i]][path[i+1]]['weight']

    return path, total_cost


def plotGraph(graph, path):
    plt.figure(figsize=(16, 12))
    
    pos = nx.circular_layout(graph)
   
    nx.draw_networkx_nodes(graph, pos, nodelist=path, node_size=500, node_color='skyblue')
    edges = [(path[i], path[i+1]) for i in range(len(path)-1)]
    nx.draw_networkx_edges(graph, pos, edgelist=edges, edge_color='red', width=2)
    nx.draw_networkx_labels(graph, pos, font_size=8)
    edge_labels = nx.get_edge_attributes(graph, 'weight')
    nx.draw_networkx_edge_labels(graph, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Graph Visualization with Path Highlighted")
    plt.show()

def showOutput(index, dfs_path, astar_path, dfs_cost, astar_cost):
    # get terminal width 
    terminal_width = os.get_terminal_size().columns
    # print full terminal width
    print("=" * terminal_width)
    print(str(index) + " GRAPH")
    print()

    print("---- BUSCA NAO INFORMADA")
    showFinalPath(dfs_path)
    print("Custo total: " + str(dfs_cost))
    
    print() 

    print("---- BUSCA INFORMADA")
    showFinalPath(astar_path)
    print("Custo total: " + str(astar_cost))

    print("=" * terminal_width)

def main():
    index = ['DISTANCE', 'DURATION', 'RATINGS'] 
    for i in range (1):
        createGraph(G_distance)
        
        dfs_path, dfs_cost = dfs(G_distance)
        astar_path, astar_cost = AStar(G_distance)
        
        showOutput(index[i], dfs_path, astar_path, dfs_cost, astar_cost)

        plotGraph(G_distance, dfs_path)
        plotGraph(G_distance, astar_path)

if __name__ == "__main__":
    main()

