import googlemaps
import json

client = googlemaps.Client(key="AIzaSyBoxKHJNAVlH4Mc8UQAFnC6SrZtaLSgAEg")

# geocode_result = client.geocode("Rua Vergueiro, 1000, São Paulo, SP")

with open("metro_stations.txt", "r") as f:
    stations_list = f.readlines()
    for line in stations_list:
        if (line[0] == "#"):
            print(line)
        # TO-DO: calcular a distância

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