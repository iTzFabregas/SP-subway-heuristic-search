import googlemaps
import json
import csv

import heuristic

client = googlemaps.Client(key="")

stations_dist = []
stations_latlon = []

if __name__ == "__main__":

    with open("./stations_list/all_stations.txt", "r") as f:
        stations_list = [line.rstrip('\n') for line in f.readlines()]
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
            # buffer['heuristic-distance'] = heuristic.find_heuristic(directions_result)  # testing heurist values

            stations_dist.append(buffer)

    with open("./output/dist.json", "w") as f:
        json.dump(stations_dist, f)