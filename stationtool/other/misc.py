"""
This module contains all other small but important functions.
"""

import datetime
import pyproj
from PyQt5.QtCore import QDate, QDateTime, QTime

def qDate2Date(qdate_val):
    """
    Function for transforming from qdate into date
    """
    return datetime.date(qdate_val.year(), qdate_val.month(), qdate_val.day())

def date2QDate(date_val):
    """
    Function for transforming from date into qdate
    """
    return QDate(date_val.year, date_val.month, date_val.day)


def qDateTime2Datetime(qdatetime_val):
    """
    Function for transforming from qdatetime into datetime
    """
    return datetime.datetime(qdatetime_val.date().year(), qdatetime_val.date().month(), qdatetime_val.date().day(),
                            qdatetime_val.time().hour(), qdatetime_val.time().minute(), qdatetime_val.time().second(),
                            qdatetime_val.time().msec()*1000)

def datetime2QDateTime(date_val):
    """
    Function for transforming from datetime into qdatetime
    """
    return QDateTime(QDate(date_val.year, date_val.month, date_val.day),
                     QTime(date_val.hour, date_val.minute, date_val.second, date_val.microsecond/1000))

def fromTM35FINToMap(x, y):
    """
    Function for moving from TM35FIN coordinates into the coordinates of the
    picture
    """
    pic_h = 2480
    pic_w = 1748

    x_min = -40442
    y_min = 6555699
    x_max = 837057
    y_max = 7800801

    y_max -= y_min
    x_max -= x_min

    x_return = pic_w * (x - x_min) / x_max
    y_return = pic_h * (y_max - (y - y_min)) / y_max

    return x_return, y_return


def fromDegToTM35FIN(lat, lon):
    """
    Function for moving from latitude and longitude to TM35FIN coordinates.
    """
    p1 = pyproj.Proj(init="epsg:4326")
    p2 = pyproj.Proj(init="epsg:3067")

    coords = pyproj.transform(p1, p2, lon, lat)
    return coords[0], coords[1]

