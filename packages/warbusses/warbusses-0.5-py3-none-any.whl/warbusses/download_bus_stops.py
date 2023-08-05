"""Module that downloads bus_stops.txt file from api.um.warszawa.pl"""
import os
import json
import requests

path = os.getcwd()
path_to_data = os.path.join(path, 'data')


def extends():
    """Function that downloads bus stop data"""
    response = requests.get(
        '''https://api.um.warszawa.pl/api/action/dbstore_get?id=
            ab75c33d-3a26-4342-b36a-6e5fef0a3ac3&apikey=eab89a39-4594-46b6-94cf-89eb29f728d5''')
    resp = response.json()
    with open(os.path.join(path_to_data, 'bus_stops.txt'), 'w', encoding='utf-8') as outfile:
        json.dump(resp, outfile)


if __name__ == "__main__":
    extends()
