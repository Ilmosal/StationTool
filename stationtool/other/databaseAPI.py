"""
This module contains a class for handling all database calls of the StationTool Program
"""
from nordb.database.sql2station import getAllStations
class DatabaseApi(object):
    """
    Class that handles all database calls for the StationTool Program.
    """
    def __init__(self):
        pass

    def getStations(self):
        """
        """
        stations = getAllStations()

        return stations
