"""Module that provides functions for coordinates operations"""
import pandas as pd


def transform_coors(szer_geo, dlug_geo):
    return str([szer_geo, dlug_geo])


def middle_coors(wsp1, wsp2):
    return [(a + b) / 2 for a, b in zip(list(get_coors(wsp1)), list(get_coors(wsp2)))]


def get_coors(wspx):
    wspx = wspx[1:-1]
    return float(wspx.split(',')[0]), float(wspx.split(',')[1])


def distance(wsp1, wsp2):
    """ takes as an input coordinates in a form str([52.2296756, 21.0122287])
    and returns distance between them in km."""
    from math import sin, cos, sqrt, atan2, radians
    wsp11, wsp12 = get_coors(wsp1)
    wsp21, wsp22 = get_coors(wsp2)
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
    """ takes as an input dates in a form '23/12/2020  15:38:01'
    and returns difference between them in hours"""
    difference = abs(pd.to_datetime(date2) - pd.to_datetime(date1))
    return difference.seconds / 3600
