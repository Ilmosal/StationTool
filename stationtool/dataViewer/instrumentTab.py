"""
This module contains information for handling InstrumentTab class.
"""
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QPushButton

from datetime import datetime, date
from dataViewer.dataViewTab import (DataViewTab, AbstractDatabaseTableModel,
                                    AbstractStorageTableModel, DataViewTabButtons)
from dataEdit.newInstrumentWindow import NewInstrumentWindow
from dataEdit.connectInstrumentWindow import ConnectInstrumentWindow

from nordb.nordic.instrument import Instrument

class InstrumentDatabaseModel(AbstractDatabaseTableModel):
    """
    Class for handling instrument database model
    """
    def __init__(self, parent, header, database_api, selection_manager):
        AbstractDatabaseTableModel.__init__(self, parent, header, [], database_api)
        self.selection_manager = selection_manager
        self.instruments = []

    def getSelectedIds(self):
        """
        Function for overriding old getSelectedIds
        """
        return self.selection_manager.getSelectedInstruments()

    def fetchDataFromDB(self):
        """
        InstrumentDatabaseModels overridden fetchDataFromDB function for filling the table with database related information
        """
        self.instruments = self.database_api.getInstruments()
        self.updateInstrumentsArrayModel()

    def updateInstrumentsArrayModel(self):
        """
        Function for updating model data_array to match instruments own list of instruments
        """
        self.clearModelData()
        for ins in self.instruments:
            self.insertNewDataRow([ ins.i_id,
                                    ins.instrument_name,
                                    ins.instrument_type,
                                    ins.band,
                                    ins.digital,
                                    ins.samprate,
                                    ins.ncalib,
                                    ins.ncalper,
                                    ins.resp_dir,
                                    ins.dfile,
                                    ins.rsptype,
                                    ins.lddate])


class InstrumentStorageModel(AbstractStorageTableModel):
    """
    Class for handling instruments storage model.
    """
    def __init__(self, parent, header, database_model, selection_manager):
        AbstractStorageTableModel.__init__(self, parent, header, [], database_model)
        self.selection_manager = selection_manager
        self.stored_responses = []

    def pushDataToDatabase(self):
        for resp in self.stored_responses:
            self.database_model.database_api.insertResponse(resp)

        for ins in self.array_data:
            new_ins = Instrument()
            new_ins.instrument_name = ins[1]
            new_ins.instrument_type = ins[2]
            new_ins.band = ins[3]
            new_ins.digital = ins[4]
            new_ins.samprate = ins[5]
            new_ins.ncalib = ins[6]
            new_ins.ncalper = ins[7]
            new_ins.resp_dir = ins[8]
            new_ins.dfile = ins[9]
            new_ins.rsptype = ins[10]
            new_ins.lddate = ins[11]

            for resp in self.stored_responses:
                if resp.file_name == new_ins.dfile:
                    new_ins.response_id = resp.response_id
                    break

            self.database_model.database_api.insertInstrument(new_ins)

        self.stored_responses.clear()
        self.clearModelData()
        self.parent().updateDatabaseModel()

    def addResponseToStorage(self, response):
        """
        Function for adding a response in the storage
        """
        self.stored_responses.append(response)

class InstrumentViewTab(DataViewTab):
    """
    Class for handling the table tab for instrument related information
    """
    def __init__(self, parent, database_api, selection_manager):
        buttons = InstrumentViewTabButtons()
        DataViewTab.__init__(self, parent, buttons)
        selection_manager = selection_manager
        buttons.setParent(self)

        header = [  ["Id", int],
                    ["Instrument_name", str],
                    ["Instrument type", str],
                    ["Band", str],
                    ["Digital", str],
                    ["Sample rate", float],
                    ["Nominal calibration rate", float],
                    ["Nominal calibration period", float],
                    ["Response directory", str],
                    ["Response filename", str],
                    ["Response type", str],
                    ["Load date", date]
                 ]

        self.database_api = database_api
        self.instrument_db_model = InstrumentDatabaseModel(self, header, database_api, selection_manager)
        self.instrument_storage_model = InstrumentStorageModel(self, header, self.instrument_db_model, selection_manager)
        self.addModels(self.instrument_db_model, self.instrument_storage_model)

    def addIdToSelection(self, selected_id):
        """
        Overridden selection function
        """
        self.selection_manager.addInstrumentToSelection(selected_id)
        self.parent().parent().parent().parent().setSelectionText('Instrument')

    def getSelectedInstrument(self):
        """
        Function for getting the recently selected instrument
        """
        pass

    def addInstrumentToStorage(self, instrument):
        """
        Function for adding a nordb Instrument object to the instrumentViewTabs model.
        """
        data = [instrument.i_id,
                instrument.instrument_name,
                instrument.instrument_type,
                instrument.band,
                instrument.digital,
                instrument.samprate,
                instrument.ncalib,
                instrument.ncalper,
                instrument.resp_dir,
                instrument.dfile,
                instrument.rsptype,
                instrument.lddate]

        return self.addRowToStorage(data)

    def saveDataRowID(self):
        """
        Overridden function for saving the id of the clicked instrument row and passing it to response
        """
        select = self.database_view.selectionModel().currentIndex()
        self.selected_id = select.sibling(select.row(), 0).data()
        self.parent().parent().parent().response_tab.updateResponseTab(self.selected_id)

class InstrumentViewTabButtons(DataViewTabButtons):
    """
    Class for InstrumentViewTa buttons.
    """
    ADD_BUTTON = 0
    CONNECT_BUTTON = 1
    REMOVE_BUTTON = 2
    CLEAR_BUTTON = 3
    PUSH_BUTTON = 4

    def __init__(self):
        buttons = [
            QPushButton("Add"),
            QPushButton("Connect"),
            QPushButton("Remove"),
            QPushButton("Clear"),
            QPushButton("Push")
        ]
        buttons[self.ADD_BUTTON].clicked.connect(self.openNewStationWindowButton)
        buttons[self.CONNECT_BUTTON].clicked.connect(self.openConnectInstrumentWindowButton)
        buttons[self.REMOVE_BUTTON].clicked.connect(self.removeFromStorageButton)
        buttons[self.CLEAR_BUTTON].clicked.connect(self.clearStorageButton)
        buttons[self.PUSH_BUTTON].clicked.connect(self.pushToDatabaseButton)

        DataViewTabButtons.__init__(self, buttons)

    def openNewStationWindowButton(self):
        """
        Open a window for creating a new window
        """
        self.widget = NewInstrumentWindow(self.parent().instrument_storage_model, self.parent().database_api)
        self.widget.show()

    def openConnectInstrumentWindowButton(self):
        """
        Open connect instrument window
        """
        instrument = self.parent().getSelectedInstrument()

        if instrument is None:
            return

        self.widget = ConnectInstrumentWindow(self.parent().sitechan_storage_model,
                                              self.parent().sensor_storage_model,
                                              self.parent().database_api,
                                              instrument.ncalib,
                                              instrument.ncalper,
                                              instrument.i_id)
        self.widget.show()

    def pushToDatabaseButton(self):
        """
        Push data to database
        """
        self.parent().instrument_storage_model.pushDataToDatabase()

    def clearStorageButton(self):
        """
        Clear this storage and all attached information
        """
        self.parent().instrument_storage_model.clearModelData()

    def removeFromStorageButton(self):
        """
        Remove a field from storage
        """
        self.parent().removeSelectedFromStorage()
