import json
import networkx as nx
import subprocess
import os
import googlemaps

def fetchPlaceID(place_id):
    client = googlemaps.Client(key="AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU")
    response = client.place(place_id)
    return response

def returnPlaceID(stations):
    """ 
    Return a list of place-id values
    
    Args: 
        stations (list): list of string stations 

    Returns: 
        list: all place-id values in a list
    
    Raises:
        none
    """

    # open file ratings
    with open("ratings.json", 'r') as f:
        data = json.load(f)
  
    # get place-id by match stations 
    places_list = []
    place_id_list = []
    for station in stations:
        for item in data:
            station_rating = item.get('station').split(', ')[0].strip() 
            if (station == station_rating):
                place_id_list.append(item.get('place-id'))
                response = fetchPlaceID(item.get('place-id'))
                places_list.append(response)

    return place_id_list, places_list

def returnFinalPath(path):
    """ 
    Return a string that represents the final path.
    The final path includes all stations separated by an arrow 
    
    Args: 
        path (list): list of string stations 

    Returns: 
        string: final path including all stations formatted  
    
    Raises:
        none
    """

    # format final path 
    final_path = "" 
    for i in range(len(path) - 1):
        final_path += path[i] + " ➡ "
    final_path += path[-1]

    return final_path

def getJsonData(GRAPH_TYPE):
    """ 
    Return a dict type including all data from json file

    Args: 
        GRAPH_TYPE (string): string that represents which file shall be open 

    Returns: 
        dict: contain all data from json file  
    
    Raises:
        none
    """

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

    with open(path, 'r') as f:
        data = json.load(f)
   
    return data

def createGraph(GRAPH_TYPE):
    """ 
    Return a graph type from networkx library 

    Args: 
        GRAPH_TYPE (string): string that represents which file shall be open
        in getJsonData() function

    Returns: 
        graph: graph from networkx library  
    
    Raises:
        none
    """

    graph = nx.DiGraph()
    
    data = getJsonData(GRAPH_TYPE) 
  
    # full graph
    for item in data:
        # format origin and destination 
        origin = item['origin'].split(', ')[0].strip()
        destination = item['destination'].split(', ')[0].strip()
        
        # take the last key value in itens and convert to flaot 
        weight_key = list(item.keys())[-1]
        weight = float(item[weight_key])

        # add nodes and edges
        graph.add_node(origin)
        graph.add_node(destination)
        graph.add_edge(origin, destination, weight=weight)
        graph.add_edge(destination, origin, weight=weight)

    return graph

def heuristic(origin, destination, heuristic_type):
    """ 
    Open the file with the json containing all heuristic information and return the value given 
    an origin and destination nodes

    Args: 
        origin (string): represents the start node of the trip 
        destination (string): represents the target node of the trip 
        heuristic_type (string): string that represents which heuristic type 
        shall be used

    Returns: 
        float: heuristic value  
    
    Raises:
        none
    """

    # generate the heuristic file 
    heuristic_path =  "./heuristics/" + destination.replace(" ", "") + "_heuristic.json"

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
    """ 
    Search for the best path given a graph of stations using A* algorithm

    Args: 
        graph: graph type from networkx library
        heuristic_type (string): string that represents which heuristic type 
        shall be used
        travel_info (list): contains origin and destination information

    Returns: 
        list: final path founded by A* 

    Raises:
        none
    """

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
