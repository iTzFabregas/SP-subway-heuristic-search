import googlemaps
import json

import heuristic

client = googlemaps.Client(key='AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU')

stations_dist = []
stations_latlon = []

if __name__ == '__main__':

    with open('./stations_list/metro_stations.txt', 'r') as f:
        stations_list = [line.rstrip('\n') for line in f.readlines()]
        n = len(stations_list)

        for station_1 in range(n):
            station_2 = station_1 + 1

            if (station_2 >= n): break
            if (stations_list[station_1][0] == '#'): continue
            if (stations_list[station_2][0] == '#'): continue

            directions_result = client.directions(stations_list[station_1],
                                                stations_list[station_2],
                                                mode='transit',
                                                transit_mode='subway')


            buffer_duration = {}
            buffer_latlon = {}
            for i in directions_result[0]['legs'][0]['steps']:
                if i['travel_mode'] != 'TRANSIT': continue
                
                buffer_duration['origin'] = buffer_latlon['origin'] = stations_list[station_1]
                buffer_duration['destination'] = buffer_latlon['destination'] = stations_list[station_2]
                buffer_duration['real-duration'] = i['duration']['value']

                buffer_latlon['start-lat'] = i['start_location']['lat']
                buffer_latlon['start-lon'] = i['start_location']['lng']
                buffer_latlon['end-lat'] = i['end_location']['lat']
                buffer_latlon['end-lon'] = i['end_location']['lng']

            stations_dist.append(buffer_duration)
            stations_latlon.append(buffer_latlon)

    with open('./output/durations.json', 'w') as f:
        json.dump(stations_dist, f)

    with open('./output/latitude_longitude.json', 'w') as f:
        json.dump(stations_latlon, f)