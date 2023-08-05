"""Module that finds locations where buses exceed 50 km/h"""
import os
import pandas as pd
import warbusses.coors_functions as wcf

path = os.getcwd()
path_to_data = os.path.join(path, 'data')
df = pd.read_csv(os.path.join(path_to_data, 'speed.csv'), low_memory=False, index_col=0)
df = df[(df > 50).any(1)]

buses_above_50 = list(df.index)
buses_above_50 = list(set([x[:3] for x in buses_above_50]))

df2 = pd.read_csv(os.path.join(path_to_data, 'coordinates_speed.csv'),
                  low_memory=False, index_col=0)
locations_above_50 = []
p = list(enumerate(zip(df.values, df2.values)))

for i in p:
    for k in range(57):
        if i[1][0][k] > 50:
            locations_above_50.append(i[1][1][k])

numbers_loc = [0] * len(locations_above_50)

k = 0
for i in locations_above_50:
    for j in locations_above_50:
        try:
            if wcf.distance(i, j) < 0.5:
                numbers_loc[k] += 1
        except TypeError:
            continue
    k += 1
max_value = max(numbers_loc)
max_index = numbers_loc.index(max_value)

print(locations_above_50)
print(locations_above_50[max_index])
