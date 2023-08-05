import pandas as pd
import os
import json

path = os.getcwd()
path_to_data = os.path.join(path, 'data')

with open(os.path.join(path_to_data, 'bus_stops.txt')) as json_file:
    data = json.loads(json_file.read())

lista = data['result']

zespol = []
slupek = []
nazwa_zespolu = []
id_ulicy = []
szer_geo = []
dlug_geo = []
kierunek = []

for d in lista:
    slownik = d['values']
    for i in slownik:
        if 'zespol' in i.values():
            zespol.append(i['value'])
        elif 'slupek' in i.values():
            slupek.append(i['value'])
        elif 'nazwa_zespolu' in i.values():
            nazwa_zespolu.append(i['value'])
        elif 'id_ulicy' in i.values():
            id_ulicy.append(i['value'])
        elif 'szer_geo' in i.values():
            szer_geo.append(i['value'])
        elif 'dlug_geo' in i.values():
            dlug_geo.append(i['value'])
        elif 'kierunek' in i.values():
            kierunek.append(i['value'])
        else:
            continue
df = pd.DataFrame(list(zip(zespol, slupek, nazwa_zespolu, id_ulicy, szer_geo, dlug_geo, kierunek)),
                  columns=['zespol', 'slupek', 'nazwa_zespolu', 'id_ulicy', 'szer_geo', 'dlug_geo', 'kierunek'])

# potrzebujemy wlasciwie tylko zespol, slupek i wspolrzedne
df=df[['zespol', 'slupek','nazwa_zespolu', 'szer_geo', 'dlug_geo']]

df.to_csv(os.path.join(path_to_data, 'bus_stops.csv'),encoding='utf-8')
