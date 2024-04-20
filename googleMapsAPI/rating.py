import googlemaps
import json

import heuristic

client = googlemaps.Client(key="AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU")

if __name__ == "__main__":

    stations_ratings = [{}]
    with open("./output/latitude_longitude.json", "r") as f:
        dados = json.load(f)

        for dado in dados:
            start_station = dado["origin"]
            end_station = dado["destination"]

            res1 = client.places(start_station, (dado["start-lat"], dado["start-lon"]))
            res2 = client.places(end_station, (dado["end-lat"], dado["end-lon"]))

        
            start_in = end_in = False
            for dic in stations_ratings:
                if start_station in dic.values(): start_in = True
                if end_station in dic.values(): end_in = True

            buffer = {}   
            if not start_in:
                buffer["station_name"] = start_station
                buffer["station_real"] = res1["results"][0]["name"]
                buffer["rating"] = res1["results"][0]["rating"]
                buffer["address"] = res1["results"][0]["formatted_address"]
                stations_ratings.append(buffer)

            buffer = {}
            if not end_in:
                buffer["station_name"] = end_station
                buffer["station_real"] = res2["results"][0]["name"]
                buffer["rating"] = res2["results"][0]["rating"]
                buffer["address"] = res2["results"][0]["formatted_address"]
                stations_ratings.append(buffer)
    
    stations_ratings.pop(0)
    with open("./output/ratings.json", "w") as f:
        json.dump(stations_ratings, f)

