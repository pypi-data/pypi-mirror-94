import requests
from bs4 import BeautifulSoup


def download_bus_schedule(bus_number):
    bus_stops_two_directions = []
    URL = "http://www.m2.rozkladzik.pl/warszawa/rozklad_jazdy.html?l=" + bus_number
    r = requests.get(URL)
    soup = BeautifulSoup(r.content, 'html5lib')
    for s in soup.select(".holo-list"):
        bus_stops = []
        for f in s.findAll("li"):
            if f.text not in bus_stops:
                bus_stops.append(f.text.lower())
        bus_stops_two_directions.append(bus_stops)
    return bus_stops_two_directions, list(set().union(*bus_stops_two_directions))