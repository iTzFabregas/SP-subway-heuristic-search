import googlemaps
import json

import heuristic

client = googlemaps.Client(key="AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU")

if __name__ == "__main__":

    stations_ratings = []
    with open("./output/buffer/latitude_longitude.json", "r") as f:
        dados = json.load(f)

        for dado in dados:
            station = dado["station"]
            res = client.places(station, (dado["lat"], dado["lon"]))
        
            buffer = {}
            buffer["station"] = station
            buffer["real_station"] = res["results"][0]["name"]
            buffer["rating"] = res["results"][0]["rating"]
            buffer["address"] = res["results"][0]["formatted_address"]
            stations_ratings.append(buffer)
    
    with open("./output/ratings.json", "w") as f:
        json.dump(stations_ratings, f)

