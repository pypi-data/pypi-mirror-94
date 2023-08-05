import pandas as pd
import os
from coordinate_functions import middle_coors, distance, diff_between_dates

path = os.getcwd()
path_to_data = os.path.join(path, 'data')

df = pd.read_csv(os.path.join(path_to_data, 'bus_coordinates.csv'), low_memory=False)
df[['Lines', 'VehicleNumber']] = df[['Lines', 'VehicleNumber']].astype(str)
df['linevehic'] = df[['Lines', 'VehicleNumber']].apply(lambda x: ''.join(x), axis=1)
df = df.drop(['Lines', 'VehicleNumber'], axis=1)
df = df.set_index('linevehic')

dfn = df.stack().reset_index()
dfn.columns = ['idx', 'time', 'coor']
dfn.sort_values(['idx', 'time'], inplace=True)

n = 2
lista_series, lista_coord = [], []
for i in range(57):
    res_dict, coord_dict = dict(), dict()
    for idx, group in dfn.groupby('idx'):
        try:
            dates = group.iloc[(n - 2):n, 1].tolist()
            coors = group.iloc[(n - 2):n, 2].tolist()

            # calculate use function
            dist_diff = distance(*coors)
            dates_diff = diff_between_dates(*dates)

            result = dist_diff / dates_diff
            res_dict[idx] = result
            coord_dict[idx] = middle_coors(*coors)
        except TypeError:
            print('nie ma danych')

    obj_res = pd.Series(res_dict)
    coord_dict = pd.Series(coord_dict)
    lista_series.append(obj_res)
    lista_coord.append(coord_dict)
    n = n + 1
df_speed = pd.concat(lista_series, axis=1)
df_coord = pd.concat(lista_coord, axis=1)
df_speed.to_csv(os.path.join(path_to_data, 'speed.csv'))
df_coord = df_coord.to_csv(os.path.join(path_to_data, 'coordinates_speed.csv'))
