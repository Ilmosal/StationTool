"""
Module for handling creation of a new Instrument
"""

from PyQt5.QtWidgets import QWidget

from dataEdit.dataEditWindow import DataEditWindow
from dataEdit.dataEditField import (FloatEditField, IntegerEditField, StringEditField,
                                    ChoiceEditField, DateEditField, DatetimeEditField,
                                    ResponseEditField)
from datetime import datetime

class NewInstrumentWindow(DataEditWindow):
    """
    Class for handling the window of the New Instrument functionality
    """
    INSTRUMENT_NAME = 0
    INSTRUMENT_TYPE = 1
    BAND = 2
    DIGITAL = 3
    SAMPLERATE = 4
    NCALIB = 5
    NCALPER = 6
    RESPONSE_FILE = 7

    def __init__(self, storage_model, database_api):
        self.database_api = database_api
        self.fields = [
            StringEditField(self, "Instrument name", "Name of the instrument", 50),
            StringEditField(self, "Instrument type", "Type of the instrument", 6),
            StringEditField(self, "Instrument Bandwidth", "Bandwidth code of the instrument", 1),
            ChoiceEditField(self, "Digital", "Info whether the instrument is digital or analog. d - digital, a - analog", ['d', 'a']),
            FloatEditField(self, "Samplerate", "Default samplerate of the instrument", min_val = 10.0, max_val = 2000.0, decimals = 3, default_val = 200.0),
            FloatEditField(self, "Instrument nominal calibration", "Nominal calibration (nn/count) of the instrument", min_val = 0.0, max_val = 10000.0, decimals = 7),
            FloatEditField(self, 'Instrument calibration period', "Nominal calibration period (sec)", min_val = 0.0, max_val = 100.0, decimals = 6, default_val = 0.5),
            ResponseEditField(self, "Response file", "Response file of the instrument. You can either load a new response to the database or use an existing one as your response file.", database_api)
        ]
        DataEditWindow.__init__(self, 'New Instrument', storage_model, self.fields)

    def getDataFromFields(self):
        """
        Get instrument data from fields.
        """
        return  [
            -1,
            self.fields[self.INSTRUMENT_NAME].getValue(),
            self.fields[self.INSTRUMENT_TYPE].getValue(),
            self.fields[self.BAND].getValue(),
            self.fields[self.DIGITAL].getValue(),
            self.fields[self.SAMPLERATE].getValue(),
            self.fields[self.NCALIB].getValue(),
            self.fields[self.NCALPER].getValue(),
            "../response",
            self.fields[self.RESPONSE_FILE].getValue().file_name,
            self.fields[self.RESPONSE_FILE].getValue().response_format,
            datetime.now()
        ]

    def getResponse(self):
        """
        Get response object from the NewInstrumentWindow
        """
        return self.fields[self.RESPONSE_FILE].getValue()

    def pushToStorage(self):
        """
        Overwritten function for pushing instrument AND the response to the storage model
        """
        self.storage_field.insertNewDataRow(self.getDataFromFields())
        self.storage_field.addResponseToStorage(self.getResponse())
        self.exitWindow()

