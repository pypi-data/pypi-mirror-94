import pandas as pd
import sys
import os
from webscraping_bus_stops import download_bus_schedule
from coordinate_functions import transform_coordinates, distance
from bus_stop_functions import check_direction, get_time_for_bus_stop

path = os.getcwd()
path_to_data = os.path.join(path, 'data')

df1 = pd.read_csv(os.path.join(path_to_data, 'bus_coordinates.csv'), low_memory=False)
df1[['Lines', 'VehicleNumber']] = df1[['Lines', 'VehicleNumber']].astype(str)
df2 = pd.read_csv(os.path.join(path_to_data, 'bus_stops.csv'), low_memory=False, encoding='utf-8')
df2["nazwa_zespolu"] = df2["nazwa_zespolu"].str.lower()

if __name__ == '__main__':
    bus_number='212'
    #bus_number = input("Wpisz numer autobusu którego punktualność chcesz sprawdzić")
    vehicles = list(df1.loc[df1['Lines'] == bus_number, 'VehicleNumber'])
    #vehicle_number = input(f"Wybierz vehicle number z listy {vehicles}")
    vehicle_number = '9680'

    if bus_number not in df1['Lines'].values or vehicle_number not in vehicles:
        print('this bus is not in the data')
        sys.exit()

    row = df1.loc[df1['Lines'] == bus_number]
    row = row.loc[row['VehicleNumber'] == vehicle_number].dropna(axis=1)
    row = row.drop(['Lines', 'VehicleNumber'], axis=1)
    row = row.iloc[0]
    if row.empty:
        print('no coordinates for this line')
        sys.exit()

    bus_stops_two_directions, bus_stops = download_bus_schedule(bus_number)
    ###Leave only those bus stops which are in bus_stop data.
    for lists in bus_stops_two_directions:
        for bus_stop in lists:
            if bus_stop not in df2["nazwa_zespolu"].values:
                lists.remove(bus_stop)
    for bus_stop in bus_stops:
        if bus_stop not in df2["nazwa_zespolu"].values:
            bus_stops.remove(bus_stop)

    df3 = df2.loc[df2['nazwa_zespolu'].isin(bus_stops)][['szer_geo', 'dlug_geo', 'nazwa_zespolu']]

    df3['coordinates'] = df3.apply(lambda x: transform_coordinates(x['szer_geo'], x['dlug_geo']), axis=1)

    df3['distance_from_bus_initial'] = df3.apply(lambda x: distance(x['coordinates'], row[0]), axis=1)
    minimum_initial = df3['distance_from_bus_initial'].min()
    bus_stop_initial = df3[df3['distance_from_bus_initial'] == minimum_initial]['nazwa_zespolu'].iloc[0]

    direction, opposite_direction = check_direction(bus_stop_initial, bus_stops_two_directions, row, 3, df3)


    df3['distance_from_bus_final'] = df3.apply(lambda x: distance(x['coordinates'], row[-1]), axis=1)
    minimum_final = df3['distance_from_bus_final'].min()
    bus_stop_final = df3[df3['distance_from_bus_final'] == minimum_final]['nazwa_zespolu'].iloc[0]

    times = []
    previous_bus_stop_time = row[row == row[0]].index[0]

    if bus_stop_final in direction[direction.index(bus_stop_initial):]:
        for bus_stop in direction[direction.index(bus_stop_initial):direction.index(bus_stop_final)]:
            times.append(get_time_for_bus_stop(bus_stop, previous_bus_stop_time, row, df3))
            previous_bus_stop_time = times[-1]
    else:
        for bus_stop in direction[direction.index(bus_stop_initial):]:
            times.append(get_time_for_bus_stop(bus_stop, previous_bus_stop_time, row, df3))
            previous_bus_stop_time = times[-1]
        for bus_stop in opposite_direction[:direction.index(bus_stop_final)]:
            times.append(get_time_for_bus_stop(bus_stop, previous_bus_stop_time, row, df3))
            previous_bus_stop_time = times[-1]
    print(direction)
    print(row)
    print(times)
