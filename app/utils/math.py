from math import sin, cos, sqrt, atan2, radians


# def get_euclidean_distance(item1, item2):
#     lat1 = radians(item1['lat'])
#     lng1 = radians(item1['lng'])
#     lat2 = radians(item2['lat'])
#     lng2 = radians(item2['lng'])
#
#     # approximate radius of earth in km
#     R = 6373.0
#
#     dlon = lng2 - lng1
#     dlat = lat2 - lat1
#
#     a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
#     c = 2 * atan2(sqrt(a), sqrt(1 - a))
#
#     distance = R * c
#
#     return distance * 1000


def get_euclidean_distance(item1, item2):
    lat1 = radians(item1['lat'])
    lng1 = radians(item1['lng'])
    lat2 = radians(item2['lat'])
    lng2 = radians(item2['lng'])

    # approximate radius of earth in km
    R = 6373.0

    x1 = R * cos(lat1) * cos(lng1)
    y1 = R * cos(lat1) * sin(lng1)
    z1 = R * sin(lat1)

    x2 = R * cos(lat2) * cos(lng2)
    y2 = R * cos(lat2) * sin(lng2)
    z2 = R * sin(lat2)

    distance = sqrt(pow(x2-x1, 2) + pow(y2-y1, 2) + pow(z2-z1, 2))

    return distance * 1000
