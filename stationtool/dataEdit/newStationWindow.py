"""
Module for handling creation of a new station
"""

from dataEdit.dataEditWindow import DataEditWindow
from dataEdit.dataEditField import (FloatEditField, IntegerEditField, StringEditField,
                                    ChoiceEditField, DateEditField, DatetimeEditField)

class NewStationWindow(DataEditWindow):
    """
    Class for handling the window of the New Station functionality
    """
    NETWORK = 0
    STATION_CODE = 1
    STATION_NAME = 2
    ON_DATE = 3
    LATITUDE = 4
    LONGITUDE = 5
    ELEVATION = 6
    STATION_TYPE = 7
    REFERENCE_STATION = 8
    NORTH_OFFSET = 9
    EAST_OFFSET = 10

    def __init__(self, storage_model, database_api):
        self.database_api = database_api
        self.fields = [  ChoiceEditField(self,
                                    'Network',
                                    'Network of the station. Choose one of the listed.',
                                    database_api.getNetworks()),
                    StringEditField(self,
                                    'Station Code',
                                    'Station Code of the station. Maximum of six characters. This needs to be unique.',
                                    6),
                    StringEditField(self,
                                   'Station Name',
                                   'Full name of the station. Maximum of 50 characters',
                                   50),
                    DateEditField(  self,
                                    'On Date',
                                    'The date when the station was opened'),
                    FloatEditField( self,
                                    'Latitude',
                                    'Latitude coordinate of the station in degrees.',
                                    0.0, 360.0, 6, 25.0),
                    FloatEditField( self,
                                    'Longitude',
                                    'Longitude coordinate of the station in degrees.',
                                    -180.0, 180.0, 6, 60.0),
                    FloatEditField( self,
                                    'Elevation',
                                    'Elevation of the station in kilometers',
                                    -20.0, 10.0, 4, 0.0),
                    ChoiceEditField(self,
                                    'Station Type',
                                    'Type of the station. Possible choices are ss(substation), bb(broadband) and ar(array)',
                                    ['ss', 'bb', 'ar']),
                    StringEditField(self,
                                    'Reference Station',
                                    'Reference station to which the offset position is calculated to if this station is part of an array. Use the station code of the reference point, but leave this field blanc if this station is not part of an array',
                                    6),
                    FloatEditField( self,
                                    'North Offset',
                                    'Offset in kilometers to the reference station',
                                    -50.0, 50.0, 4, 0.0),
                    FloatEditField( self,
                                    'East Offset',
                                    'Offset in kilometers to the reference station',
                                    -50.0, 50.0, 4, 0.0)
                 ]
        DataEditWindow.__init__(self, 'New Station', storage_model, self.fields)

    def getDataFromFields(self):
        """
        Get station data from fields.
        """
        return  [
            -1,
            self.fields[self.NETWORK].getValue(),
            self.fields[self.STATION_CODE].getValue(),
            self.fields[self.ON_DATE].getValue(),
            None,
            self.fields[self.LATITUDE].getValue(),
            self.fields[self.LONGITUDE].getValue(),
            self.fields[self.ELEVATION].getValue(),
            self.fields[self.STATION_NAME].getValue(),
            self.fields[self.STATION_TYPE].getValue(),
            self.fields[self.REFERENCE_STATION].getValue(),
            self.fields[self.NORTH_OFFSET].getValue(),
            self.fields[self.EAST_OFFSET].getValue(),
            None
        ]
