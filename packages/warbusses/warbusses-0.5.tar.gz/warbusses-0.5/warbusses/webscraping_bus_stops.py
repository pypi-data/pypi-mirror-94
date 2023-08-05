"""Module that downloads bus stops for a particular line from www.m2.rozkladzik.pl/warszawa/"""
import requests
from bs4 import BeautifulSoup


def download_bus_schedule(bus_number):
    URL = "http://www.m2.rozkladzik.pl/warszawa/rozklad_jazdy.html?l=" + bus_number
    r = requests.get(URL)
    soup = BeautifulSoup(r.content,
                         'html5lib')

    bus_stops_1 = []
    bus_stops_2 = []

    directions = soup.find_all("ul", {"class": "holo-list"})

    for stop in directions[0].find_all("a"):
        if stop.text.lower().strip() not in bus_stops_1:
            bus_stops_1.append(stop.text.lower().strip())

    for stop in directions[1].find_all("a"):
        if stop.text.lower().strip() not in bus_stops_2:
            bus_stops_2.append(stop.text.lower().strip())

    bus_stops_two_directions = [bus_stops_1, bus_stops_2]

    return bus_stops_two_directions, sorted(bus_stops_two_directions[0] + list(set(bus_stops_two_directions[1])
                                                                        - set(bus_stops_two_directions[0])))