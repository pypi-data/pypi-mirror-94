import requests
import os
import time

path = os.getcwd()
path_to_data = os.path.join(path, 'data')
hold_list = []


def extends():
    response = requests.get(
        "https://api.um.warszawa.pl/api/action/busestrams_get/?resource_id= f2e5503e-927d-4ad3-9500-4ab9e55deb59&apikey=eab89a39-4594-46b6-94cf-89eb29f728d5&type=1")
    resp = response.json()
    hold_list.extend(resp['result'])

starttime = time.time()
i = 0
while (i < 60):
    extends()
    time.sleep(60.0 - ((time.time() - starttime) % 60.0))
    i = i + 1

with open(os.path.join(path_to_data, 'bus_streams.txt'), 'w') as f:
    for item in hold_list:
        f.write("%s\n" % item)
