import os
import pandas as pd
import ast

path = os.getcwd()
path_to_data = os.path.join(path, 'data')

with open(os.path.join(path_to_data, 'bus_streams.txt')) as fp:
    lines = fp.readlines()

# if there are irregularities, use a try/except to pass these (note, you may wish to use a logger in practice)
lista = []
for line in lines:
    try:
        lista.append(ast.literal_eval(line))
    except ValueError:
        print("malformed string; skipping this line")
    except SyntaxError:
        print("looks like some encoding errors with this file...")

my_dick = []
for d in lista:
    my_dick.append([d["Lines"], d["VehicleNumber"], d["Time"], [(d["Lat"]), (d["Lon"])]])
array1 = [_ for _, __, col, val in my_dick]
array2 = [__ for _, __, col, val in my_dick]
arrays = [array1, array2]
tuples = list(zip(*arrays))

indeks = pd.MultiIndex.from_tuples(tuples, names=['Lines', 'VehicleNumber'])

df = pd.DataFrame([{col: val} for _ , __, col, val in my_dick], index=indeks)
df = df.groupby(level=[0, 1]).first()
df.columns = pd.to_datetime(df.columns)
df = df.reindex(sorted(df.columns), axis=1)
x1 = '2020-12-23 15:38:00'
x2 = '2020-12-23 16:42:00'
m1 = [i for i in df.columns if i > pd.to_datetime(x1)]
df = df[m1]
m2 = [i for i in df.columns if i < pd.to_datetime(x2)]
df = df[m2]

df.to_csv(os.path.join(path_to_data, 'bus_coordinates.csv'))
