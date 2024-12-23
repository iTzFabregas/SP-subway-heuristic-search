import json
import networkx as nx
import subprocess
import os
import googlemaps
import boto3
from dotenv import load_dotenv

load_dotenv(override=True)

# Configurações AWS
s3_client = boto3.client(
    's3',
    aws_access_key_id=os.getenv('AWS_ACCESS_KEY_ID'),
    aws_secret_access_key=os.getenv('AWS_SECRET_ACCESS_KEY'),
    region_name=os.getenv('AWS_REGION')
)

BUCKET_NAME = os.getenv('AWS_BUCKET_NAME')

def returnInfo(stations):
    """ 
    Return a list of places information
    
    Args: 
        stations (list): list of string stations 

    Returns: 
        list: all places information
    
    Raises:
        none
    """

    # get file ratings and places
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key='json_files/ratings.json')
    content = response['Body'].read().decode('utf-8')
    data1 = json.loads(content)

    response = s3_client.get_object(Bucket=BUCKET_NAME, Key='json_files/places.json')
    content = response['Body'].read().decode('utf-8')
    data2 = json.loads(content)
  
    # get place-id by match stations 
    places_list = []
    for station in stations:
        for item in data1:
            station_rating = item.get('station').split(', ')[0].strip() 
            if (station == station_rating):
                place_id = item['place-id']
                for info in data2:
                    if info['place-id'] == place_id:
                        places_list.append(info['response'])

    return places_list

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
    distances_file_path = "json_files/distances.json"
    durations_file_path = "json_files/durations.json"
    ratings_file_path = "json_files/ratings.json"

    data_paths = [distances_file_path, durations_file_path, ratings_file_path]
    index = ['DISTANCE', 'DURATION', 'RATING']
    
    for i in range(len(data_paths)):
        if (GRAPH_TYPE == index[i]):
            path = data_paths[i]
            break

    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=path)
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
   
    return data

def createRatingsGraph(GRAPH_TYPE):
    graph = nx.DiGraph()

    rating_data = getJsonData(GRAPH_TYPE)
    travel_data = getJsonData('DISTANCE')

    # full graph
    for item in travel_data:
        # format origin and destination 
        origin = item['origin'].split(', ')[0].strip()
        destination = item['destination'].split(', ')[0].strip()
       
        weight = 0 
        nodes_traveled = 0 
        
        for rating_item in rating_data:
            station = rating_item.get('station').split(', ')[0].strip()
            # get rating origin and in another iteration
            # get rating destination and sum both
            if station in origin or station in destination:
                weight += rating_item.get('rating')
                nodes_traveled += 1
            # the of origin and destination's rating is complete
            if nodes_traveled == 2:
                break
        
        #calculate arithmetic average
        weight *= 0.5 
        
        graph.add_node(origin)
        graph.add_node(destination)
        graph.add_edge(origin, destination, weight=weight)
        graph.add_edge(destination, origin, weight=weight)

    return graph


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
    heuristic_path =  "heuristics/" + destination.replace(" ", "") + "_heuristic.json"

    # open heuristic file
    response = s3_client.get_object(Bucket=BUCKET_NAME, Key=heuristic_path)
    content = response['Body'].read().decode('utf-8')
    data = json.loads(content)
   
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

def findLongestPath(graph, travel_info):
    origin = travel_info[0]
    destination = travel_info[1]

    max_path = []
    max_len = 0

    for path in nx.all_simple_paths(graph, origin, destination):
        len_path = len(path)
        if len_path > max_len:
            max_path = path 
            max_len = len_path 

    return max_path, len(max_path) 

def findHeaviestPath(graph, travel_info):
    origin = travel_info[0]
    destination =  travel_info[1]

    max_path = None
    max_cost = float('-inf')

    for path in nx.all_simple_paths(graph, origin, destination):
        cost = 0
        for u, v in zip(path[:-1], path[1:]):
            cost += graph[u][v]['weight']
        if cost > max_cost:
            max_path = path
            max_cost = cost

    return max_path, max_cost
