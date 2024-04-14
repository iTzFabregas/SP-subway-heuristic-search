import googlemaps
import json

import heuristic

client = googlemaps.Client(key="")

# stations_res = []
stations_dist = []

if __name__ == "__main__":

    with open("./stations_list/metro_stations.txt", "r") as f:
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
            for i in directions_result[0]["legs"][0]["steps"]:
                if i["travel_mode"] != "TRANSIT": continue
                buffer['real-distance'] = i["distance"]["value"]

            stations_dist.append(buffer)
            # stations_res.append(directions_result)

    with open("./output/distances.json", "w") as f:
        json.dump(stations_dist, f)

    # with open("./output/res.json", "w") as f:
    #     json.dump(stations_res, f)