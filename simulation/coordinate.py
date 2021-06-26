from math import cos, asin, sqrt


class Coordinate:
    next_id = 0

    def __init__(self, latitude, longitude):
        self.id = Coordinate.next_id
        Coordinate.next_id += 1

        self.latitude = latitude
        self.longitude = longitude

    def __eq__(self, other):
        return self.latitude == other.latitude and self.longitude == other.longitude

    def __str__(self):
        return "(%f, %f)" % (self.latitude, self.longitude)


def haversine(coordinate1, coordinate2):
    p = 0.017453292519943295
    a = 0.5 - cos((coordinate2.latitude - coordinate1.latitude) * p)/2 + cos(coordinate1.latitude * p) * \
        cos(coordinate2.latitude * p) * \
        (1 - cos((coordinate2.longitude - coordinate1.longitude) * p)) / 2
    return 12742 * asin(sqrt(a))
