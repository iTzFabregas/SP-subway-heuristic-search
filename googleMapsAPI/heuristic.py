import googlemaps
import json
import csv
import sys
from math import radians, sin, atan2, cos, sqrt, pow

# AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU
client = googlemaps.Client(key="NAO_RODAR")

def find_heuristic(dest_station):

    heuristic_list = []
    with open("./stations_list/metro_stations.txt", "r") as f:
        stations_list = [line.rstrip('\n') for line in f.readlines()]

        for origin_station in stations_list:
            if (origin_station[0] == "#"): continue

            directions_result = client.directions(origin_station, dest_station)

            ori_lat = directions_result[0]["legs"][0]["start_location"]["lat"]
            ori_log = directions_result[0]["legs"][0]["start_location"]["lng"]
            dest_lat = directions_result[0]["legs"][0]["end_location"]["lat"]
            dest_log = directions_result[0]["legs"][0]["end_location"]["lng"]
            curr_duration, curr_distance = haversine(ori_lat, dest_lat, ori_log, dest_log)
            
            buffer = {}
            buffer['station'] = origin_station
            buffer['heuristic-duration'] = curr_duration
            buffer['heuristic-distance'] = curr_distance            
            heuristic_list.append(buffer)

    return heuristic_list


def haversine(origin_lat, dest_lat, origin_lng, dest_lng):
    r = 6_371

    del_lat = radians(origin_lat) - radians(dest_lat)
    del_lng = radians(origin_lng) - radians(dest_lng)

    a = pow(sin(del_lat/2),2) + cos(origin_lat) * cos(dest_lat) * pow(sin(del_lng/2),2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return r * c / 80 * 3600, 1000 * r * c



if __name__ == "__main__":
    stations_list = []
    with open("./stations_list/metro_stations.txt", "r") as f1:
        stations_list = [line.rstrip('\n') for line in f1.readlines()]
    
    for station in stations_list:
        if station[0] == '#': continue
        heuristic_list = find_heuristic(station)
                
        file_name = "./output/heuristics/" + station.split(', ')[0].replace(" ", "") + "_heuristic.json"
        with open(file_name, "w") as f2:
            json.dump(heuristic_list, f2)