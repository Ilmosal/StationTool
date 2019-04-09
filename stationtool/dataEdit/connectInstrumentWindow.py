"""
Module for handling connecting a Instrument to a Station by creating Sensor and Sitechan fields
"""
from dataEdit.dataEditWindow import DataEditWindow
from dataEdit.dataEditField import (FloatEditField, IntegerEditField, StringEditField,
                                    ChoiceEditField, DateEditField, DatetimeEditField,
                                    CheckBoxFields)
from datetime import datetime

class ConnectInstrumentWindow(DataEditWindow):
    """
    Class for handling the window of the ConnectInstrument operations
    """
    STATION_CODE = 0
    CHANNEL_CODES = 1
    ON_DATETIME = 2
    EMPLACEMENT_DEPTH = 3
    DESCRIPTION = 4
    TSHIFT = 5
    INSTANT = 6
    CALRATIO = 7
    CALPER = 8

    def __init__(self, sitechan_storage_model, sensor_storage_model, database_api, calratio, calper, instrument_id):
        self.database_api = database_api
        self.fields = [
            ChoiceEditField(self, "Station Code", "Station code to which this instrument will be attached to", self.database_api.getStationCodes()),
            CheckBoxFields(self, "Channels", "Channels that will be created", ["N", "E", "Z"]),
            DatetimeEditField(self, "On Datetime", "Datetime when this instrument was set up"),
            FloatEditField(self, "Emplacement Depth", "Depth of this instrument in the relation of the elevation of the station in meters", -100.0, 100.0),
            StringEditField(self, "Description", "Description of this sitechan installation", 50),
            IntegerEditField(self, "Tshift", "Correction to the data processing time", min_val=-1000, max_val=1000),
            ChoiceEditField(self, "Instant", "Discrete or continuing snapshot. 'y' - yes, 'n' - no  ", ['y', 'n']),
            FloatEditField(self, "Calibration Ratio", "Calibration rate of the instrument", min_val = 0.0, max_val = 1000.0, default_val = calratio),
            FloatEditField(self, "Calibration Period", "Calibration period of the instrument", min_val = 0.0, max_val = 5000.0, default_val = calper)
        ]
        self.instrument_id = instrument_id
        self.sitechan_storage_model = sitechan_storage_model
        self.sensor_storage_model = sensor_storage_model
        DataEditWindow.__init__(self, 'Connect Instrument', None, self.fields)

    def pushToStorage(self):
        """
        Overridden method for pushing content to storage
        """
        for c_code in self.fields[self.CHANNEL_CODES].getValue():
            self.sitechan_storage_model.insertNewDataRow(self.getSitechanDataFromFields(c_code))
            self.sensor_storage_model.insertNewDataRow(self.getSensorDataFromFields(c_code))
        self.exitWindow()

    def getSitechanDataFromFields(self, c_code):
        """
        Get relevant sitechan data
        """
        if c_code == 'Z':
            horizontal_angle = -1.0
            vertical_angle = 0.0
        elif c_code == 'E':
            horizontal_angle = 90.0
            vertical_angle = 90.0
        elif c_code == 'N':
            horizontal_angle = 0.0
            vertical_angle = 90.0
        else:
            horizontal_angle = None
            vertical_angle = None

        return [
            -1,
            self.fields[self.STATION_CODE].getValue(),
            c_code,
            self.fields[self.ON_DATETIME].getValue(),
            None,
            'n',
            self.fields[self.EMPLACEMENT_DEPTH].getValue(),
            horizontal_angle,
            vertical_angle,
            self.fields[self.DESCRIPTION].getValue(),
            datetime.now()
        ]

    def getSensorDataFromFields(self, c_code):
        """
        Get relevant sensor data
        """
        return [
            -1,
            self.fields[self.STATION_CODE].getValue(),
            c_code,
            self.fields[self.ON_DATETIME].getValue().timetuple(),
            9999999999.999,
            self.fields[self.CALRATIO].getValue(),
            self.fields[self.CALPER].getValue(),
            self.fields[self.TSHIFT].getValue(),
            self.fields[self.INSTANT].getValue(),
            datetime.now()
        ]
