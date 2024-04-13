import googlemaps
import json
from math import radians, sin, asin, cos, sqrt

client = googlemaps.Client(key="")

stations_dist = []
stations_latlon = []


def find_heuristic(directions_result):

    origin_lat = radians(directions_result[0]["legs"][0]["start_location"]["lat"])
    dest_lat = radians(directions_result[0]["legs"][0]["end_location"]["lat"])

    origin_lng = radians(directions_result[0]["legs"][0]["start_location"]["lng"])
    dest_lng = radians(directions_result[0]["legs"][0]["end_location"]["lng"])

    return haversine(origin_lat, dest_lat, origin_lng, dest_lng)

def haversine(origin_lat, dest_lat, origin_lng, dest_lng):
    r = 6_371

    del_lat = origin_lat - dest_lat
    del_lng = origin_lng - dest_lng

    a = sin(del_lat/2) * sin(del_lat/2) + cos(radians(origin_lat)) * cos(radians(dest_lat)) * sin(del_lng/2) * sin(del_lng/2)
    c = 2 * asin(sqrt(a))

    return  1000 * r * c




if __name__ == "__main__":
    with open("./stations_list/small_list_station.txt", "r") as f:
        stations_list = f.readlines()
        n = len(stations_list)

        for station_1 in range(n):
            station_2 = station_1 + 1

            if (station_2 >= n): break
            if (stations_list[station_1][0] == "#"): continue
            if (stations_list[station_2][0] == "#"): continue

            directions_result = client.directions(stations_list[station_1],
                                                stations_list[station_2],
                                                mode="transit",
                                                transit_mode="subway")

            buffer = {}
            buffer['origin'] = stations_list[station_1]
            buffer['destination'] = stations_list[station_2]
            buffer['real-distance'] = directions_result[0]["legs"][0]["distance"]["value"]
            buffer['heuristic-distance'] = find_heuristic(directions_result)  
            
            stations_dist.append(buffer)

    with open("./output/dist.json", "w") as f:
        json.dump(stations_dist, f)
