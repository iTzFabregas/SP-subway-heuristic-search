import googlemaps
import json

client = googlemaps.Client(key="AIzaSyBoxKHJNAVlH4Mc8UQAFnC6SrZtaLSgAEg")

# geocode_result = client.geocode("Rua Vergueiro, 1000, São Paulo, SP")

stations_dist = []

with open("small_list_station.txt", "r") as f:
    stations_list = f.readlines()
    n = len(stations_list)
    for station_1 in range(n):
        station_2 = station_1 + 1

        if (stations_list[station_1][0] == "#"): continue
        if (station_2 >= n): break
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

'''
directions_result = client.directions("Estação Tatuape",
                                    "Estação Corinthians - Itaquera",
                                    mode="transit",
                                    transit_mode="subway")

# print(directions_result)
for etapa in directions_result[0]["legs"][0]["steps"]:
    print(f"Instrução: {etapa['html_instructions']}")
    print(f"Distância: {etapa['distance']['text']}")
    print(f"Duração: {etapa['duration']['text']}")
    print()

with open("res.json", "w") as f:
    json.dump(directions_result, f)
'''