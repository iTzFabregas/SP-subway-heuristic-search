import googlemaps
import json

client = googlemaps.Client(key="")

stations_dist = []

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
        buffer['distance'] = directions_result[0]["legs"][0]["distance"]["value"]
        
        stations_dist.append(buffer)

with open("dist.json", "w") as f:
    json.dump(stations_dist, f)
