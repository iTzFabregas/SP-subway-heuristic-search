import json
import networkx as nx
import matplotlib.pyplot as plt

# file path
file_path = "../googleMapsAPI/dist.json"

# create graph
G = nx.DiGraph()
 
def createGraph():
    # open json 
    with open(file_path, 'r') as f:
        data = json.load(f)
    
   
    # full graph
    for item in data:
        origin = item['origin'].split(' -')[0].strip()
        destination = item['destination'].split(' -')[0].strip()
        distance = item['real-distance']
        G.add_node(origin)
        G.add_node(destination)
        G.add_edge(origin, destination, weight=distance)

def searchGraph(starting_node, target_node):
    # search in graph
    dfs_path = list(nx.dfs_edges(G, source=starting_node))
    
    if target_node in [starting_node] + [edge[1] for edge in dfs_path]:
        print("O nó final foi alcançado.")
        path_to_target = nx.shortest_path(G, source=starting_node, target=target_node)
        print("Caminho encontrado:", path_to_target)
       
        total_cost = 0
        for i in range(len(path_to_target) - 1):
            total_cost += G[path_to_target[i]][path_to_target[i+1]]['weight']
        print("Custo total do caminho:", total_cost)
    else:
        print("O nó final não foi alcançado.")

def plotGraph():
    plt.figure(figsize=(8, 6))
    
    pos = nx.circular_layout(G)
    
    nx.draw_networkx_nodes(G, pos, node_size=500, node_color='skyblue')
    nx.draw_networkx_edges(G, pos, edge_color='gray')
    nx.draw_networkx_labels(G, pos, font_size=8)
    edge_labels = nx.get_edge_attributes(G, 'weight')
    nx.draw_networkx_edge_labels(G, pos, edge_labels=edge_labels, font_size=8)
    
    plt.title("Graph Visualization with Edge Weights")
    plt.show()


starting_node = "Estacao Santana"
target_node = "Estacao Portuguesa-Tiete (ex Tiete)"
createGraph()
searchGraph(starting_node, target_node)
plotGraph()
