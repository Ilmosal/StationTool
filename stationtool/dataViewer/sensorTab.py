"""
This module contains information for handling SensorTab class.
"""
from PyQt5.QtWidgets import QPushButton, QFileDialog
from PyQt5.QtCore import QVariant, Qt
from PyQt5.QtGui import QColor

from datetime import datetime, date
from dataViewer.dataViewTab import (DataViewTab, AbstractDatabaseTableModel,
                                    AbstractStorageTableModel, DataViewTabButtons)

class SensorDatabaseModel(AbstractDatabaseTableModel):
    """
    Class for handling sensor database model
    """
    def __init__(self, parent, header, database_api, selection_manager):
        AbstractDatabaseTableModel.__init__(self,parent, header, [], database_api)
        self.selection_manager = selection_manager
        self.sensors = []

    def getSelectedIds(self):
        """
        Function for overriding old getSelectedIds
        """
        return self.selection_manager.getSelectedSensors()

    def fetchDataFromDB(self):
        """
        SensorDatabaseModels overridden fetchDataFromDB function for filling the table with database related information
        """
        self.sensors = self.database_api.getSensors()
        self.updateSensorsArrayModel()

    def updateSensorsArrayModel(self):
        """
        Function for updating model data_array to match sensors own list of sensors
        """
        self.clearModelData()
        for sen in self.sensors:
            self.insertNewDataRow([ sen.s_id,
                                    sen.station_code,
                                    sen.channel_code,
                                    sen.time,
                                    sen.endtime,
                                    sen.calratio,
                                    sen.calper,
                                    sen.tshift,
                                    sen.instant,
                                    sen.lddate])


class SensorStorageModel(AbstractStorageTableModel):
    """
    Class for handling sensors storage model.
    """
    def __init__(self, parent, header, database_model, selection_manager):
        AbstractStorageTableModel.__init__(self, parent, header, [], database_model)
        self.selection_manager = selection_manager

    def pushDataToDatabase(self):
        for sen in self.array_data:
            #transform into sensor object
            continue

        self.clearDatabaseModel()

class SensorViewTab(DataViewTab):
    """
    Class for handling the table tab for sensor related information
    """
    def __init__(self, parent, database_api, selection_manager):
        buttons = SensorViewTabButtons()
        DataViewTab.__init__(self, parent, buttons)
        self.selection_manager = selection_manager
        buttons.setParent(self)
        header = [  ["Id", int],
                    ["Station code", str],
                    ["Channel Code", str],
                    ["Time", float],
                    ["End Time", float],
                    ["Calibration ratio", float],
                    ["Calibration period", float],
                    ["Tshift", float],
                    ["Instant", str],
                    ["Load date", date]]

        sensor_db_model = SensorDatabaseModel(self, header, database_api, selection_manager)
        sensor_storage_model = SensorStorageModel(self, header, sensor_db_model, selection_manager)
        self.addModels(sensor_db_model, sensor_storage_model)

    def addIdToSelection(self, selected_id):
        """
        Overridden selection function
        """
        print('adding id {0} to selection'.format(selected_id))
        self.selection_manager.addSensorToSelection(selected_id)
        self.parent().parent().parent().parent().setSelectionText('Sensor')

    def addSensorToStorage(self, sensor):
        """
        Function for adding a nordb Sensor object to the sensorViewTabs model.
        """
        data = [sensor.s_id,
                sensor.station_code,
                sensor.channel_code,
                sensor.time,
                sensor.endtime,
                sensor.calratio,
                sensor.calper,
                sensor.tshift,
                sensor.instant,
                sensor.lddate]

        return self.addRowToStorage(data)

class SensorViewTabButtons(DataViewTabButtons):
    """
    Class for SensorViewTab buttons.
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
        buttons[self.IMPORT_BUTTON].clicked.connect(self.importSensorButton)
        buttons[self.CLEAR_BUTTON].clicked.connect(self.clearStorageButton)
        buttons[self.PUSH_BUTTON].clicked.connect(self.pushToDatabaseButton)

        DataViewTabButtons.__init__(self, buttons)

    def importSensorButton(self):
        """
        Open a sensor file and read them into storage
        """
        try:
            sensor_file = open(QFileDialog.getOpenFileName(self, "Open a CSS3.0 sensor file", str(Path.home()), '')[0], 'r')
        except:
            return

        sensors = []

        for line in sensor_file:
            try:
                if line[0] == '#' or not len(line.strip()):
                    continue
                sensors.append(readSensorStringToSensor(line, ''))
            except Exception as e:
                sensor_file.close()
                print(e)
                return

        for s in sensors:
            self.parent().addSensorToStorage(s)

        sensor_file.close()

    def pushToDatabaseButton(self):
        """
        Push data to database
        """
        self.parent().sensor_storage_model.pushDataToDatabase()

    def clearStorageButton(self):
        """
        Clear this storage and all attached information
        """
        self.parent().sensor_storage_model.clearModelData()
