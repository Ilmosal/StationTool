"""
This module contains information for handling StationTab class.
"""
from datetime import datetime, date
from dataViewer.dataViewTab import (DataViewTab, AbstractDatabaseTableModel,
                                    AbstractStorageTableModel)

class StationDatabaseModel(AbstractDatabaseTableModel):
    """
    Class for handling station database model.
    """
    def __init__(self, parent, header, database_api):
        AbstractDatabaseTableModel.__init__(self, parent, header, [], database_api)
        self.stations = []

    def fetchDataFromDB(self):
        """
        StationDatabaseModels overridden fetchDataFromDB function for filling the table with database related information
        """
        self.stations = self.database_api.getStations()
        self.updateStationArrayModel()

    def updateStationArrayModel(self):
        """
        Function for updating model data_array to match stations own list of stations
        """
        self.clearModelData()

        for stat in self.stations:
            self.insertNewDataRow(  [stat.network,
                                    stat.station_code,
                                    stat.on_date,
                                    stat.off_date,
                                    stat.latitude,
                                    stat.longitude,
                                    stat.elevation,
                                    stat.station_name,
                                    stat.station_type,
                                    stat.reference_station,
                                    stat.north_offset,
                                    stat.east_offset,
                                    stat.load_date])

class StationStorageModel(AbstractStorageTableModel):
    """
    Class for handling station storage model.
    """
    def __init__(self, parent, header, database_model):
        AbstractStorageTableModel.__init__(self, parent, header, [], database_model)

    def pushDataToDatabase(self):
        for stat in self.array_data:
            #Here transform stat to NorDB station object and push it to database
            continue

        self.clearDatabaseModel()

class StationViewTab(DataViewTab):
    """
    Class for handling the table tab for station related information.
    """
    def __init__(self, parent, database_api):
        DataViewTab.__init__(self, parent)
        header = [['Network', str], ['Station code', str],
                  ['On Date', date], ['Off Date', date], ['Latitude', float],
                  ['Longitude', float], ['Elevation',float],
                  ['Station Name', str], ['Station Type', str],
                  ['Reference Station', str], ['North Offset', float],
                  ['East Offset', float], ['Load Date', date]]
        station_db_model = StationDatabaseModel(self, header, database_api)
        station_storage_model = StationStorageModel(self, header, station_db_model)
        self.addModels(station_db_model, station_storage_model)

    def addStationToStorage(self, station):
        """
        Function for adding a nordb Station object to the stationViewTabs model.
        """
        data = [station.network,
                station.station_code,
                station.on_date.date(),
                station.off_date.date(),
                station.latitude,
                station.longitude,
                station.elevation,
                station.station_name,
                station.station_type,
                station.reference_station,
                station.north_offset,
                station.east_offset,
                station.load_date]

        return self.addRowToStorage(data)
