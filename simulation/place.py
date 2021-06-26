from coordinate import Coordinate


class Place:
    next_id = 0

    def __init__(self, name, coordinate):
        self.id = Place.next_id
        Place.next_id += 1

        self.name = name
        self.coordinate = coordinate

    @staticmethod
    def from_file(filename):
        places = []
        f = open(filename, "r")
        lines = f.readlines()
        f.close()

        for line in lines:
            tokens = line.split(";")
            name = tokens[0]
            latitude = float(tokens[1])
            longitude = float(tokens[2].replace("\n", ""))
            places.append(Place(name, Coordinate(latitude, longitude)))

        return places[0], places[1:]

    def __eq__(self, other):
        return self.coordinate == other.coordinate and self.name == other.name

    def __str__(self):
        return "Place: %s | %s | %s" % (self.id, self.coordinate.__str__(), self.name)


def print_places(places):
    for place in places:
        print(place)
