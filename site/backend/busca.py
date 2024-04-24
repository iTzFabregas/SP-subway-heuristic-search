import json
import networkx as nx
import subprocess
import os

def getJsonData(GRAPH_TYPE):
    # file path
    distances_file_path = "../../googleMapsAPI/output/distances.json"
    durations_file_path = "../../googleMapsAPI/output/durations.json"
    ratings_file_path = "../../googleMapsAPI/output/ratings.json"

    data_paths = [distances_file_path, durations_file_path, durations_file_path]
    index = ['DISTANCE', 'DURATION', 'RATING']
    
    for i in range(len(data_paths)):
        if (GRAPH_TYPE == index[i]):
            path = data_paths[i]
            break

    print(path) 
    with open(path, 'r') as f:
        data = json.load(f)
   
    return data

def createGraph(GRAPH_TYPE):
    graph = nx.DiGraph()
    
    data = getJsonData(GRAPH_TYPE) 
  
    # full graph
    for item in data:
        # format origin and destination 
        origin = item['origin'].split(', ')[0].strip()
        destination = item['destination'].split(', ')[0].strip()
        print(origin) 
        # take the last key value in itens and convert to flaot 
        weight_key = list(item.keys())[-1]
        weight = float(item[weight_key])

        graph.add_node(origin)
        graph.add_node(destination)
        graph.add_edge(origin, destination, weight=weight)
        graph.add_edge(destination, origin, weight=weight)

    return graph

def returnFinalPath(path):
    final_path = "" 
    for i in range(len(path) - 1):
        final_path += path[i] + " ➡ "
    final_path += path[-1]
    return final_path

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

def bfs(graph):
    # search in graph
    bfs_path = list(nx.bfs_edges(graph, source=starting_node))
    total_cost = 0
    path = [starting_node]
    for edge in bfs_path:
        total_cost += graph[edge[0]][edge[1]]['weight']
        path.append(edge[1])
        if edge[1] == target_node:
            break

    return path, total_cost

def heuristic(origin, destination, heuristic_type):
    # generate the heuristic file 
    python_interpreter = 'python3'
    python_program = './heuristic.py'
    heuristic_path =  destination.replace(" ", "") + "_heuristic.json"

    # Execute o script heuristic.py
    subprocess.run(f'{python_interpreter} {python_program} "{destination}"', shell=True, check=True)

    # open heuristic file
    with open(heuristic_path, 'r') as f:
        data = json.load(f)
   
    # return values 
    for item in data:
        current_station = item['station'].split(', ')[0].strip()
        if (current_station == origin):
            if heuristic_type == 'DISTANCE':
                return item['heuristic-distance']
            else:
                return item['heuristic-duration']

def AStar(graph, heuristic_type, travel_info):
    starting_node = travel_info[0]
    target_node = travel_info[1]
    path = nx.astar_path(graph, 
                         starting_node, 
                         target_node, 
                         heuristic=lambda n1, n2: heuristic(n1, n2, heuristic_type),  
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

def showOutput(index, dfs_path, bfs_path, astar_path, dfs_cost, bfs_cost, astar_cost):
    # get terminal width 
    terminal_width = os.get_terminal_size().columns
    # print full terminal width
    print("=" * terminal_width)
    print(str(index) + " GRAPH")
    print()

    print("---- BUSCA NAO INFORMADA")
    print("- DFS")
    showFinalPath(dfs_path)
    print("Custo total: " + str(dfs_cost))
   
    print()
    print("- BFS")
    showFinalPath(bfs_path)
    print("Custo total: " + str(bfs_cost))
    

    print() 

    print("---- BUSCA INFORMADA")
    showFinalPath(astar_path)
    print("Custo total: " + str(astar_cost))

    print("=" * terminal_width)
    print()

def main():
    index = ['DISTANCE', 'DURATION', 'RATINGS'] 
    graph_list = [G_distance, G_duration, G_rating] 
    data_paths = [distances_file_path, durations_file_path, durations_file_path]
    rating_permissions = [False, False, True]
    for i in range(len(graph_list)):
        createGraph(graph_list[i], data_paths[i], rating_permissions[i])
        
        dfs_path, dfs_cost = dfs(graph_list[i])
        bfs_path, bfs_cost = bfs(graph_list[i])
        astar_path, astar_cost = AStar(graph_list[i], index[i])
        
        showOutput(index[i], dfs_path, bfs_path, astar_path, dfs_cost, bfs_cost, astar_cost)
