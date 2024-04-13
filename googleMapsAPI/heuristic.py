from math import radians, sin, atan2, cos, sqrt, pow

def find_heuristic(directions_result):

    origin_lat = radians(directions_result[0]["legs"][0]["start_location"]["lat"])
    dest_lat = radians(directions_result[0]["legs"][0]["end_location"]["lat"])

    origin_lng = radians(directions_result[0]["legs"][0]["start_location"]["lng"])
    dest_lng = radians(directions_result[0]["legs"][0]["end_location"]["lng"])


    return haversine(origin_lat, dest_lat, origin_lng, dest_lng)

def haversine(origin_lat, dest_lat, origin_lng, dest_lng):
    r = 6_371

    del_lat = origin_lat - dest_lat
    del_lng = origin_lng - dest_lng

    a = pow(sin(del_lat/2),2) + cos(origin_lat) * cos(dest_lat) * pow(sin(del_lng/2),2)
    c = 2 * atan2(sqrt(a), sqrt(1-a))

    return  1000 * r * c