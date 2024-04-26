import googlemaps
import json

import heuristic

client = googlemaps.Client(key='AIzaSyA_prM8fOfjOLNI_pDa0w1IO0L5ePMMaaU')

stations_dist = []
stations_durat = []
stations_latlon = [{}]

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


            buffer_distance = {}
            buffer_duration = {}
            buffer_latlon1 = {}
            buffer_latlon2 = {}
            for i in directions_result[0]['legs'][0]['steps']:
                if i['travel_mode'] != 'TRANSIT': continue
                
                buffer_distance['origin'] = buffer_duration['origin'] = stations_list[station_1]
                buffer_distance['destination'] = buffer_duration['destination'] = stations_list[station_2]
                buffer_distance['real-distance'] = i['distance']['value']
                buffer_duration['real-duration'] = i['duration']['value']


                start_in = end_in = False
                for dic in stations_latlon:
                    if stations_list[station_1] in dic.values(): start_in = True
                    if stations_list[station_2] in dic.values(): end_in = True

                if not start_in:
                    buffer_latlon1['station'] = stations_list[station_1]
                    buffer_latlon1['lat'] = i['start_location']['lat']
                    buffer_latlon1['lon'] = i['start_location']['lng']
                    stations_latlon.append(buffer_latlon1)

                if not end_in:
                    buffer_latlon2['station'] = stations_list[station_2]
                    buffer_latlon2['lat'] = i['end_location']['lat']
                    buffer_latlon2['lon'] = i['end_location']['lng']
                    stations_latlon.append(buffer_latlon2)


            stations_dist.append(buffer_distance)
            stations_durat.append(buffer_duration)

    with open('./output/distances.json', 'w') as f:
        json.dump(stations_dist, f)
        
    with open('./output/durations.json', 'w') as f:
        json.dump(stations_durat, f)
    
    stations_latlon.pop(0)
    with open('./output/buffer/latitude_longitude.json', 'w') as f:
        json.dump(stations_latlon, f)