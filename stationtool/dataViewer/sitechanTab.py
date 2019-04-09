"""
This module contains information for handling SitechanTab class.
"""
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtGui import QColor

from datetime import datetime, date
from dataViewer.dataViewTab import (DataViewTab, AbstractDatabaseTableModel,
                                    AbstractStorageTableModel, DataViewTabButtons)

class SitechanDatabaseModel(AbstractDatabaseTableModel):
    """
    Class for handling sitechan database model.
    """
    def __init__(self, parent, header, database_api, selection_manager):
        AbstractDatabaseTableModel.__init__(self, parent, header, [], database_api)
        self.selection_manager = selection_manager
        self.sitechans = []

    def getSelectedIds(self):
        """
        Function for overriding old getSelectedIds
        """
        return self.selection_manager.getSelectedSitechans()

    def fetchDataFromDB(self):
        """
        SitechanDatabaseModels overridden fetchDataFromDB function for filling the table with database related information
        """
        self.sitechans = self.database_api.getSitechans()
        self.updateSitechanArrayModel()

    def updateSitechanArrayModel(self):
        """
        Function for updating model data_array to match sitechans own list of sitechans
        """
        self.clearModelData()

        for chan in self.sitechans:
            self.insertNewDataRow( [chan.s_id,
                                    chan.station_code,
                                    chan.channel_code,
                                    chan.on_date,
                                    chan.off_date,
                                    chan.channel_type,
                                    chan.emplacement_depth,
                                    chan.horizontal_angle,
                                    chan.vertical_angle,
                                    chan.description,
                                    chan.load_date])

class SitechanStorageModel(AbstractStorageTableModel):
    """
    Class for handling sitechans storage model.
    """
    def __init__(self, parent, header, database_model, selection_manager):
        AbstractStorageTableModel.__init__(self, parent, header, [], database_model)
        self.selection_manager = selection_manager

    def pushDataToDatabase(self):
        for chan in self.array_data:
            #Here transform chan to NorDB sitechan object and push it to database
            continue

        self.clearDatabaseModel()

class SitechanViewTab(DataViewTab):
    """
    Class for handling the table tab for sitechan related information.
    """
    def __init__(self, parent, database_api, selection_manager):
        buttons = SitechanViewTabButtons()
        DataViewTab.__init__(self, parent, buttons)
        self.selection_manager = selection_manager
        buttons.setParent(self)
        header = [['Id', int],
                  ['Station code', str],
                  ['Channel Code', str],
                  ['On Date', date],
                  ['Off Date', date],
                  ['Channel Type', str],
                  ['Emplacement Depth', float],
                  ['Horizontal Angle',float],
                  ['Vertical Angle', float],
                  ['Description', str],
                  ['Load Date', date]]
        sitechan_db_model = SitechanDatabaseModel(self, header, database_api, selection_manager)
        sitechan_storage_model = SitechanStorageModel(self, header, sitechan_db_model, selection_manager)
        self.addModels(sitechan_db_model, sitechan_storage_model)

    def addIdToSelection(self, selected_id):
        """
        Overridden selection function
        """
        self.selection_manager.addSitechanToSelection(selected_id)
        self.parent().parent().parent().parent().setSelectionText('Sitechan')

    def addSitechanToStorage(self, sitechan):
        """
        Function for adding a nordb Sitechan object to the sitechanViewTabs model.
        """
        data = [sitechan.s_id,
                sitechan.station_code,
                sitechan.channel_code,
                sitechan.on_date,
                sitechan.off_date,
                sitechan.channel_type,
                sitechan.emplacement_depth,
                sitechan.horizontal_angle,
                sitechan.vertical_angle,
                sitechan.description,
                sitechan.load_date]

        return self.addRowToStorage(data)

class SitechanViewTabButtons(DataViewTabButtons):
    """
    Class for StationViewTab buttons.
    """
    IMPORT_BUTTON = 0
    CLEAR_BUTTON = 1
    PUSH_BUTTON = 2

    def __init__(self):
        buttons = [
            QPushButton("Import"),
            QPushButton("Clear"),
            QPushButton("Push")
        ]
        buttons[self.IMPORT_BUTTON].clicked.connect(self.importSitechanButton)
        buttons[self.CLEAR_BUTTON].clicked.connect(self.clearStorageButton)
        buttons[self.PUSH_BUTTON].clicked.connect(self.pushToDatabaseButton)

        DataViewTabButtons.__init__(self, buttons)

    def importSitechanButton(self):
        """
        Open a sitechan file and read them into storage
        """
        try:
            sitechan_file = open(QFileDialog.getOpenFileName(self, "Open a CSS3.0 sitechan file", str(Path.home()), '')[0], 'r')
        except:
            return

        sitechans = []

        for line in sitechan_file:
            try:
                if line[0] == '#' or not len(line.strip()):
                    continue
                sitechans.append(readSitechanStringToSitechan(line, ''))
            except Exception as e:
                sitechan_file.close()
                print(e)
                return

        for s in sitechan:
            self.parent().addSitechanToStorage(s)

        sitechan_file.close()

    def pushToDatabaseButton(self):
        """
        Push data to database
        """
        self.parent().sitechan_storage_model.pushDataToDatabase()

    def clearStorageButton(self):
        """
        Clear this storage and all attached information
        """
        self.parent().sitechan_storage_model.clearModelData()
