import googlemaps
import json

# Crie um objeto Client usando sua chave de API
client = googlemaps.Client(key="AIzaSyBoxKHJNAVlH4Mc8UQAFnC6SrZtaLSgAEg")

# Crie a requisição para a API de geocodificação
# geocode_result = client.geocode("Rua Vergueiro, 1000, São Paulo, SP")

directions_result = client.directions("Estação Tatuape",
                                    "Estação Corinthians - Itaquera",
                                    mode="transit",
                                    transit_mode="subway")

# Obtenha o resultado da requisição
# print(directions_result)
for etapa in directions_result[0]["legs"][0]["steps"]:
    print(f"Instrução: {etapa['html_instructions']}")
    print(f"Distância: {etapa['distance']['text']}")
    print(f"Duração: {etapa['duration']['text']}")
    print()

with open("res.json", "w") as f:
    json.dump(directions_result, f)

