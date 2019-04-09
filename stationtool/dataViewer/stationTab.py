"""
This module contains information for handling StationTab class.
"""
from pathlib import Path

from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtGui import QColor

from datetime import datetime, date
from dataViewer.dataViewTab import (DataViewTab, AbstractDatabaseTableModel,
                                    AbstractStorageTableModel, DataViewTabButtons)
from dataEdit.newStationWindow import NewStationWindow
from other.utils import datetime2DateOrNone

from nordb.nordic.station import Station, readStationStringToStation

class StationDatabaseModel(AbstractDatabaseTableModel):
    """
    Class for handling station database model.
    """
    def __init__(self, parent, header, database_api, selection_manager):
        AbstractDatabaseTableModel.__init__(self, parent, header, [], database_api)
        self.selection_manager = selection_manager
        self.stations = []
        self.sort(0)

    def getSelectedIds(self):
        """
        Function for overriding old getSelectedIds
        """
        return self.selection_manager.getSelectedStations()

    def getSitechans(self):
        """
        Function for receiving all sitechans in the stations on StationDatabaseModel
        """
        sitechans = []

        for stat in self.stations:
            for chan in stat.sitechans:
                sitechans.append(chan)

        return sitechans

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
            self.insertNewDataRow( [stat.s_id,
                                    stat.network,
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
    def __init__(self, parent, header, database_model, selection_manager):
        AbstractStorageTableModel.__init__(self, parent, header, [], database_model)
        self.selection_manager = selection_manager

    def pushDataToDatabase(self):
        """
        Function for pushing the station storage to the database
        """
        for stat in self.array_data:
            new_stat = Station()
            new_stat.network = stat[1]
            new_stat.station_code = stat[2]
            new_stat.on_date = stat[3]
            new_stat.off_date = stat[4]
            new_stat.latitude = stat[5]
            new_stat.longitude = stat[6]
            new_stat.elevation = stat[7]
            new_stat.station_name = stat[8]
            new_stat.station_type = stat[9]
            new_stat.reference_station = stat[10]
            new_stat.north_offset = stat[11]
            new_stat.east_offset = stat[12]
            new_stat.load_date = stat[13]
            self.database_model.database_api.insertStation(stat)

        self.clearModelData()
        self.parent().updateDatabaseModel()

class StationViewTab(DataViewTab):
    """
    Class for handling the table tab for station related information.
    """
    def __init__(self, parent, database_api, selection_manager):
        buttons = StationViewTabButtons()
        DataViewTab.__init__(self, parent, buttons)
        self.selection_manager = selection_manager
        buttons.setParent(self)
        header = [['Id', int],
                  ['Network', str],
                  ['Station code', str],
                  ['On Date', date],
                  ['Off Date', date],
                  ['Latitude', float],
                  ['Longitude', float],
                  ['Elevation',float],
                  ['Station Name', str],
                  ['Station Type', str],
                  ['Reference Station', str],
                  ['North Offset', float],
                  ['East Offset', float],
                  ['Load Date', date]]
        self.database_api = database_api
        self.selection_manager = selection_manager
        self.station_db_model = StationDatabaseModel(self, header, database_api, selection_manager)
        self.station_storage_model = StationStorageModel(self, header, self.station_db_model, selection_manager)
        self.addModels(self.station_db_model, self.station_storage_model)

    def addIdToSelection(self, selected_id):
        """
        Overridden selection function
        """
        self.selection_manager.addStationToSelection(selected_id)
        self.parent().parent().parent().parent().setSelectionText('Station')

    def addStationToStorage(self, station):
        """
        Function for adding a nordb Station object to the stationViewTabs model.
        """
        data = [station.s_id,
                station.network,
                station.station_code,
                station.on_date,
                station.off_date,
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

class StationViewTabButtons(DataViewTabButtons):
    """
    Class for StationViewTab buttons.
    """
    ADD_BUTTON = 0
    IMPORT_BUTTON = 1
    REMOVE_BUTTON = 2
    CLEAR_BUTTON = 3
    PUSH_BUTTON = 4

    def __init__(self):
        buttons = [
            QPushButton("Add"),
            QPushButton("Import"),
            QPushButton("Remove"),
            QPushButton("Clear"),
            QPushButton("Push")
        ]
        buttons[self.ADD_BUTTON].clicked.connect(self.openNewStationWindowButton)
        buttons[self.IMPORT_BUTTON].clicked.connect(self.importStationsButton)
        buttons[self.REMOVE_BUTTON].clicked.connect(self.removeFromStorageButton)
        buttons[self.CLEAR_BUTTON].clicked.connect(self.clearStorageButton)
        buttons[self.PUSH_BUTTON].clicked.connect(self.pushToDatabaseButton)

        DataViewTabButtons.__init__(self, buttons)

    def importStationsButton(self):
        """
        Open a site file and read them into storage
        """
        try:
            site_file = open(QFileDialog.getOpenFileName(self, "Open a CSS3.0 site file", str(Path.home()), '')[0], 'r')
        except:
            return

        stations = []

        for line in site_file:
            try:
                if line[0] == '#' or not len(line.strip()):
                    continue
                stations.append(readStationStringToStation(line, ''))
            except Exception as e:
                site_file.close()
                print(e)
                return

        for s in stations:
            self.parent().addStationToStorage(s)

        site_file.close()

    def openNewStationWindowButton(self):
        """
        Open a window for creating a new window
        """
        self.widget = NewStationWindow(self.parent().station_storage_model, self.parent().database_api)
        self.widget.show()

    def pushToDatabaseButton(self):
        """
        Push data to database
        """
        self.parent().station_storage_model.pushDataToDatabase()

    def clearStorageButton(self):
        """
        Clear this storage and all attached information
        """
        self.parent().station_storage_model.clearModelData()

    def removeFromStorageButton(self):
        """
        Remove a field from storage
        """
        self.parent().removeSelectedFromStorage()
