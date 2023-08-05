import pandas as pd


def transform_coordinates(szer_geo, dlug_geo):
    return str([szer_geo, dlug_geo])


def middle_coors(wsp1, wsp2):
    return [(a + b) / 2 for a, b in zip(list(wsp(wsp1)), list(wsp(wsp2)))]


def wsp(wspx):
    wspx = wspx[1:-1]
    return float(wspx.split(',')[0]), float(wspx.split(',')[1])


def distance(wsp1, wsp2):
    from math import sin, cos, sqrt, atan2, radians
    wsp11, wsp12 = wsp(wsp1)
    wsp21, wsp22 = wsp(wsp2)
    # approximate radius of earth in km
    R = 6373.0

    lat1 = radians(float(wsp11))
    lon1 = radians(float(wsp12))
    lat2 = radians(float(wsp21))
    lon2 = radians(float(wsp22))

    dlon = lon2 - lon1
    dlat = lat2 - lat1

    a = sin(dlat / 2) ** 2 + cos(lat1) * cos(lat2) * sin(dlon / 2) ** 2
    c = 2 * atan2(sqrt(a), sqrt(1 - a))

    return R * c


def diff_between_dates(date1, date2):
    difference = abs(pd.to_datetime(date2) - pd.to_datetime(date1))
    return difference.seconds / 3600

