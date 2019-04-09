"""
This module contains an object for managing data row selection policies and passing them across the application
"""

class SelectionManager(object):
    """
    Object for managing selections across the application
    """
    NONE = 0
    STATION = 1
    SITECHAN = 2
    SENSOR = 3
    INSTRUMENT = 4

    def __init__(self, databaseApi):
        self._selected_date = None
        self._selected_stations = []
        self._selected_sitechans = []
        self._selected_sensors = []
        self._selected_instruments = []
        self._active_selection = self.NONE
        self._databaseApi = databaseApi

    def selectField(self, field):
        """
        Function for selecting a field
        """
        if self._active_selection == self.NONE:
            self._active_selection = field
        elif self._active_selection != field:
            self.clearAll()
            self._active_selection = field

    def getSelectedDate(self):
        """
        Get selected date
        """
        return self._selected_date

    def selectDate(self, new_date):
        """
        Select a new date
        """
        self._selected_date = new_date
        if self._active_selection is self.NONE:
            self._selected_stations = self._databaseApi.getStationIds(self._selected_date)
            self._selected_sitechans = self._databaseApi.getSitechanIds(self._selected_date)
            self._selected_sensors = self._databaseApi.getSensorIds(self._selected_date)
            self._selected_instruments = self._databaseApi.getInstrumentIds(self._selected_date)

    def clearDate(self):
        """
        Set the current date to None
        """
        self._selected_date = None
        if self._active_selection is self.NONE:
            self._selected_stations = []
            self._selected_sitechans = []
            self._selected_sensors = []
            self._selected_instruments = []

    def getSelectedStations(self):
        """
        Get selected station
        """
        return self._selected_stations

    def selectStation(self, station_id):
        """
        Select a new station
        """
        self._selected_stations = [station_id]

        self._selected_sitechans = self._databaseApi.getSitechanIdsFromStations(self._selected_stations, self._selected_date)
        self._selected_sensors = self._databaseApi.getSensorIdsFromStations(self._selected_stations, self._selected_date)
        self._selected_instruments = self._databaseApi.getInstrumentIdsFromStations(self._selected_stations, self._selected_date)

    def addStationToSelection(self, station_id):
        """
        Add a station id to current selection
        """
        self.selectField(self.STATION)

        if station_id not in self._selected_stations:
            self._selected_stations.append(station_id)

            self._selected_sitechans = self._databaseApi.getSitechanIdsFromStations(self._selected_stations, self._selected_date)
            self._selected_sensors = self._databaseApi.getSensorIdsFromStations(self._selected_stations, self._selected_date)
            self._selected_instruments = self._databaseApi.getInstrumentIdsFromStations(self._selected_stations, self._selected_date)

    def getSelectedSitechans(self):
        """
        Get selected sitechans
        """
        return self._selected_sitechans

    def selectSitechan(self, sitechan_id):
        """
        Select a new sitechan
        """
        self._selected_sitechans = [sitechan_id]

        self._selected_stations = self._databaseApi.getStationIdsFromSitechans(self._selected_sitechans, self._selected_date)
        self._selected_sensors = self._databaseApi.getSensorIdsFromSitechans(self._selected_sitechans, self._selected_date)
        self._selected_instruments = self._databaseApi.getInstrumentIdsFromSitechans(self._selected_sitechans, self._selected_date)

    def addSitechanToSelection(self, sitechan_id):
        """
        Add sitechan id to current selection
        """
        self.selectField(self.SITECHAN)

        if sitechan_id not in self._selected_sitechans:
            self._selected_sitechans.append(sitechan_id)

            self._selected_stations = self._databaseApi.getStationIdsFromSitechans(self._selected_sitechans, self._selected_date)
            self._selected_sensors = self._databaseApi.getSensorIdsFromSitechans(self._selected_sitechans, self._selected_date)
            self._selected_instruments = self._databaseApi.getInstrumentIdsFromSitechans(self._selected_sitechans, self._selected_date)

    def getSelectedInstruments(self):
        """
        Get selected instrument
        """
        return self._selected_instruments

    def selectInstrument(self, instrument_id):
        """
        Select a new instrument
        """
        self._selected_instruments = [instrument_id]

        self._selected_stations = self._databaseApi.getStationIdsFromInstruments(self._selected_instruments, self._selected_date)
        self._selected_sitechans = self._databaseApi.getSitechanIdsFromInstruments(self._selected_instruments, self._selected_date)
        self._selected_sensors = self._databaseApi.getSensorIdsFromInstruments(self._selected_instruments, self._selected_date)

    def addInstrumentToSelection(self, instrument_id):
        """
        Add instrument id to current selection
        """
        self.selectField(self.INSTRUMENT)

        if instrument_id not in self._selected_instruments:
            self._selected_instruments.append(instrument_id)

            self._selected_stations = self._databaseApi.getStationIdsFromInstruments(self._selected_instruments, self._selected_date)
            self._selected_sitechans = self._databaseApi.getSitechanIdsFromInstruments(self._selected_instruments, self._selected_date)
            self._selected_sensors = self._databaseApi.getSensorIdsFromInstruments(self._selected_instruments, self._selected_date)

    def getSelectedSensors(self):
        """
        Get all selected sensors
        """
        return self._selected_sensors

    def selectSensor(self, sensor_id):
        """
        Select a new sensor
        """
        self._selected_sensors = [sensor_id]
        self._selected_stations = self._databaseApi.getStationIdsFromSensors(self._selected_sensors, self._selected_date)
        self._selected_sitechans = self._databaseApi.getSitechanIdsFromSensors(self._selected_sensors, self._selected_date)
        self._selected_instruments = self._databaseApi.getInstrumentIdsFromSensors(self._selected_sensors, self._selected_date)

    def addSensorToSelection(self, sensor_id):
        """
        Add sensor to current selection
        """
        self.selectField(self.SENSOR)

        print("add sensor if not in list")
        if sensor_id not in self._selected_sensors:
            self._selected_sensors.append(sensor_id)

            print("fetching stations from database")
            self._selected_stations = self._databaseApi.getStationIdsFromSensors(self._selected_sensors, self._selected_date)
            print("fetching sitechans")
            self._selected_sitechans = self._databaseApi.getSitechanIdsFromSensors(self._selected_sensors, self._selected_date)
            print("fetching instruments")
            self._selected_instruments = self._databaseApi.getInstrumentIdsFromSensors(self._selected_sensors, self._selected_date)
            print("done!")

    def clearAll(self):
        """
        Clear all fields, except for selected_date
        """
        self._active_selection = self.NONE
        if self._selected_date is not None:
            self._selected_stations = self._databaseApi.getStationIds(self._selected_date)
            self._selected_sitechans = self._databaseApi.getSitechanIds(self._selected_date)
            self._selected_sensors = self._databaseApi.getSensorIds(self._selected_date)
            self._selected_instruments = self._databaseApi.getInstrumentIds(self._selected_date)
        else:
            self._selected_stations = []
            self._selected_sitechans = []
            self._selected_sensors = []
            self._selected_instruments = []

