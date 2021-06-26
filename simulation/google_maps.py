from coordinate import Coordinate


class Google_maps:
    url = "https://www.google.com/maps/dir/?api=1&travelmode=driving&dir_action=navigate"
    waypoints = []

    @staticmethod
    def addWaipoint(latitude, longitude):
        Google_maps.waypoints.append(Coordinate(latitude, longitude))

    @staticmethod
    def buildUrl():
        origin = Google_maps.waypoints[0]
        Google_maps.waypoints.pop(0)
        Google_maps.url += "&origin=%s,%s" % (
            origin.latitude, origin.longitude)

        destination = Google_maps.waypoints[-1]
        Google_maps.waypoints.pop(-1)

        for i in range(0, len(Google_maps.waypoints)):
            if i == 0:
                Google_maps.url += "&waypoints=%s,%s" % (
                    Google_maps.waypoints[i].latitude, Google_maps.waypoints[i].longitude)
            else:
                Google_maps.url += "|%s,%s" % (
                    Google_maps.waypoints[i].latitude, Google_maps.waypoints[i].longitude)

        Google_maps.url += "&destination=%s,%s" % (
            destination.latitude, destination.longitude)

        url = Google_maps.url
        Google_maps.url = "https://www.google.com/maps/dir/?api=1&dir_action=navigate&travelmode=driving"
        Google_maps.waypoints = []
        return url.replace("|", "%7C")
