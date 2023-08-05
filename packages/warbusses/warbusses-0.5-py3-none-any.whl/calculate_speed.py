"""Module that finds locations where buses exceed 50 km/h"""
import os
import pandas as pd
from coordinate_functions import distance

path = os.getcwd()
path_to_data = os.path.join(path, 'data')
df = pd.read_csv(os.path.join(path_to_data, 'speed.csv'), low_memory=False, index_col=0)
df = df[(df > 50).any(1)]
buses_above_50 = list(df.index)
buses_above_50 = list(set([x[:3] for x in buses_above_50]))

df2 = pd.read_csv(os.path.join(path_to_data, 'coordinates_speed.csv'),
                  low_memory=False, index_col=0)
list_above_50 = []
p = list(enumerate(zip(df.values, df2.values)))

for i in p:
    for k in range(57):
        if i[1][0][k] > 50:
            list_above_50.append(i[1][1][k])

locations = [0] * len(list_above_50)

k = 0
for i in list_above_50:
    for j in list_above_50:
        try:
            if distance(i, j) < 0.5:
                locations[k] += 1
        except TypeError:
            continue
    k += 1
max_value = max(locations)
max_index = locations.index(max_value)
print(list_above_50[max_index])
