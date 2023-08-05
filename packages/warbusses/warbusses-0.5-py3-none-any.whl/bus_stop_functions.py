from coordinate_functions import distance

def check_direction(bus_stop_initial, bus_stops_two_directions, row, n, df3):
    distances_list = [0, 0]
    checking_row = row[1:n]
    for k, direction in enumerate(bus_stops_two_directions):
        distances = 0
        if bus_stop_initial not in direction:
            distances_list[k] = 1000
            continue
        else:
            index_bus_stop_initial = direction.index(bus_stop_initial)
            next_stop = direction[index_bus_stop_initial + 1]
            next_stop_coordinates = df3[df3['nazwa_zespolu'] == next_stop]['coordinates'].iloc[0]
            for coordinate in checking_row:
                distances += distance(next_stop_coordinates, coordinate)
            distances_list[k] = distances

    if distances_list[0] < distances_list[1]:
        return bus_stops_two_directions[0], bus_stops_two_directions[1]
    else:
        return bus_stops_two_directions[1], bus_stops_two_directions[0]


def get_time_for_bus_stop(bus_stop, previous_bus_stop_time, row, df3):
    bus_stop_coordinate = df3[df3['nazwa_zespolu'] == bus_stop]['coordinates'].iloc[0]
    coor = row[previous_bus_stop_time]
    minimum = distance(bus_stop_coordinate, row[0])
    row = row[previous_bus_stop_time:]
    for coordinate in row[0:4]:
        if distance(bus_stop_coordinate, coordinate) < minimum:
            minimum = distance(bus_stop_coordinate, coordinate)
            coor = coordinate
    return row[row == coor].index[0]