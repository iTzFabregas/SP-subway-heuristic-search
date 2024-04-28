import googlemaps
import json

import heuristic

# AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU
client = googlemaps.Client(key="NAO_RODAR")

if __name__ == "__main__":

    stations_info = []
    with open("./output/ratings.json", "r") as f:
        dados = json.load(f)

        for dado in dados:
            place_id = dado["place-id"]
            res = client.place(place_id)

            buffer = {}
            buffer["place-id"] = place_id
            buffer["response"] = res
            stations_info.append(buffer)
    
    with open("./output/places.json", "w") as f:
        json.dump(stations_info, f)

