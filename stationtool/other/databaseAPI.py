"""
This module contains a class for handling all database calls of the StationTool Program
"""
import time

from nordb.database.sql2station import getAllStations
from nordb.database.sql2instrument import getAllInstruments
from nordb.database.networks import getNetworks
from nordb.database.station2sql import insertStation2Database
from nordb.database.sitechan2sql import insertSiteChan2Database
from nordb.database.sensor2sql import insertSensor2Database
from nordb.database.instrument2sql import insertInstrument2Database
from nordb.database.response2sql import insertResponse2Database
from nordb.database.norDBManagement import databaseIsRunning
from nordb.core.usernameUtilities import log2nordb

class DatabaseApi(object):
    """
    Class that handles all database calls for the StationTool Program.
    """
    def __init__(self):
        if not databaseIsRunning():
            raise Exception("ERROR: Database is not running! Please see if database is actually running or if your database has been configured correctly with nordb")
        self.stations = []
        self.sitechans = []
        self.sensors = []
        self.instruments = []
        self.responses = []

    def insertStation(self, station):
        """
        Insert station to the database
        """
        insertStation2Database(station)

    def insertSitechan(self, sitechan):
        """
        Insert sitechans to the database
        """
        insertSitechan2Database(sitechan)

    def insertSensor(self, sensor):
        """
        Insert sensor to the database
        """
        insertSensor2Database(sensor)

    def insertInstrument(self, instrument):
        """
        Insert instrument to the database
        """
        insertInstrument2Database(instrument)

    def insertResponse(self, response):
        """
        Insert response to the database.
        """
        if response.response_id == -1:
            insertResponse2Database(response)

    def getNetworks(self):
        """
        Returns all networks to user
        """
        return getNetworks()

    def getStations(self):
        """
        Return all stations from the database
        """
        self.stations = getAllStations()
        return self.stations

    def getSitechans(self):
        """
        Returns all sitechans from the database
        """
        self.sitechans = []

        if len(self.stations) == 0:
            self.getStations()

        for stat in self.stations:
            for chan in stat.sitechans:
                self.sitechans.append(chan)

        return self.sitechans

    def getSensors(self):
        """
        Return all sensors from the database
        """
        self.sensors = []

        if len(self.sitechans) == 0:
            self.getSitechans()

        for chan in self.sitechans:
            for sen in chan.sensors:
                self.sensors.append(sen)

        return self.sensors

    def getInstruments(self):
        """
        Return all instruments from the database.
        """
        self.instruments = getAllInstruments()

        return self.instruments

    def getResponse(self, instrument_id):
        """
        Function for getting a single response from the database
        """
        if len(self.instruments) == 0:
            self.getInstruments()

        for ins in self.instruments:
            if ins.i_id == instrument_id:
                return ins.response

        return None

    def getStationIdsFromSitechans(self, sitechan_ids, selected_datetime):
        """
        Function for getting a list of station_ids from sitechan_ids
        """
        if not sitechan_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(station_id)
                    FROM
                        sitechan
                    WHERE
                        sitechan.id IN %s
                    """)
            cur.execute(query, (tuple(sitechan_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(station_id)
                    FROM
                        sitechan
                    WHERE
                        sitechan.id IN %(sitechan_ids)s
                    AND
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                    """)
            cur.execute(query, {'sitechan_ids':tuple(sitechan_ids), 's_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getStationIdsFromSensors(self, sensor_ids, selected_datetime):
        """
        Function for getting a list of station_ids from sensor_ids
        """
        if not sensor_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(station_id)
                    FROM
                        sitechan, sensor
                    WHERE
                        sensor.id IN %s
                    AND
                        sensor.sitechan_id = sitechan.id
                    """)
            cur.execute(query, (tuple(sensor_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(station_id)
                    FROM
                        sitechan, sensor
                    WHERE
                        sensor.id IN %(sensor_ids)s
                    AND
                        sensor.sitechan_id = sitechan.id
                    AND
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                    """)
            cur.execute(query, {'sensor_ids':tuple(sensor_ids), 's_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getStationIdsFromInstruments(self, instrument_ids, selected_datetime):
        """
        Function for getting a list of station_ids from instrument_ids
        """
        if not instrument_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(station_id)
                    FROM
                        sitechan, sensor
                    WHERE
                        sensor.sitechan_id = sitechan.id
                    AND
                        sensor.instrument_id IN %s
                    """)
            cur.execute(query, (tuple(instrument_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(station_id)
                    FROM
                        sitechan, sensor
                    WHERE
                        sensor.sitechan_id = sitechan.id
                    AND
                        sensor.instrument_id IN %(instrument_ids)s
                    AND
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                    """)
            cur.execute(query, {'instrument_ids':tuple(instrument_ids), 's_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSitechanIdsFromStations(self, station_ids, selected_datetime):
        """
        Function for getting a list of sitechan_ids from station_ids
        """
        if not station_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(id)
                    FROM
                        sitechan
                    WHERE
                        station_id IN %s
                    """)
            cur.execute(query, (tuple(station_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(id)
                    FROM
                        sitechan
                    WHERE
                        station_id IN %(station_ids)s
                    AND
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                    """)
            cur.execute(query, {'station_ids':tuple(station_ids), 's_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSitechanIdsFromSensors(self, sensor_ids, selected_datetime):
        """
        Function for getting a list of sitechan_ids from sensor_ids
        """
        if not sensor_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(sitechan_id)
                    FROM
                        sensor
                    WHERE
                        id IN %s
                    """)
            cur.execute(query, (tuple(sensor_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(sitechan_id)
                    FROM
                        sensor
                    WHERE
                        id IN %(sensor_ids)s
                    AND
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                    """)
            cur.execute(query, {'sensor_ids':tuple(sensor_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})
        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSitechanIdsFromInstruments(self, instrument_ids, selected_datetime):
        """
        Function for getting a list of sitechan_ids from instrument_ids
        """
        if not instrument_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(sitechan_id)
                    FROM
                        sensor
                    WHERE
                        instrument_id IN %s
                    """)
            cur.execute(query, (tuple(instrument_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(sitechan_id)
                    FROM
                        sensor
                    WHERE
                        instrument_id IN %(instrument_ids)s
                    AND
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                    """)

            cur.execute(query, {'instrument_ids':tuple(instrument_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSensorIdsFromStations(self, station_ids, selected_datetime):
        """
        Function for getting a list of sensor_ids from station_ids
        """
        if not station_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(sensor.id)
                    FROM
                        sensor, sitechan
                    WHERE
                        station_id IN %s
                    AND
                        sensor.sitechan_id = sitechan.id
                    """)
            cur.execute(query, (tuple(station_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(sensor.id)
                    FROM
                        sensor, sitechan
                    WHERE
                        station_id IN %(station_ids)s
                    AND
                        sensor.sitechan_id = sitechan.id
                    AND
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                    """)

            cur.execute(query, {'station_ids':tuple(station_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSensorIdsFromSitechans(self, sitechan_ids, selected_datetime):
        """
        Function for getting a list of sensor_ids from sitechan_ids
        """
        if not sitechan_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(sensor.id)
                    FROM
                        sensor
                    WHERE
                        sitechan_id IN %s
                    """)
            cur.execute(query, (tuple(sitechan_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(sensor.id)
                    FROM
                        sensor
                    WHERE
                        sitechan_id IN %(sitechan_ids)s
                    AND
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                    """)

            cur.execute(query, {'sitechan_ids':tuple(sitechan_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})
        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSensorIdsFromInstruments(self, instrument_ids, selected_datetime):
        """
        Function for getting a list of sensor_ids from instrument_ids
        """
        if not instrument_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(sensor.id)
                    FROM
                        sensor
                    WHERE
                        instrument_id IN %s
                    """)
            cur.execute(query, (tuple(instrument_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(sensor.id)
                    FROM
                        sensor
                    WHERE
                        instrument_id IN %(instrument_ids)s
                    AND
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                    """)
            cur.execute(query, {'instrument_ids':tuple(instrument_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getInstrumentIdsFromStations(self, station_ids, selected_datetime):
        """
        Function for getting a list of instrument_ids from station_ids
        """
        if not station_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(sensor.instrument_id)
                    FROM
                        sitechan, sensor
                    WHERE
                        station_id IN %s
                    AND
                        sitechan.id = sitechan_id
                    """)
            cur.execute(query, (tuple(station_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(sensor.instrument_id)
                    FROM
                        sitechan, sensor
                    WHERE
                        station_id IN %(station_ids)s
                    AND
                        sitechan.id = sensor.sitechan_id
                    AND
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                    """)
            cur.execute(query, {'station_ids':tuple(station_ids), 's_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getInstrumentIdsFromSitechans(self, sitechan_ids, selected_datetime):
        """
        Function for getting a list of instrument_ids from sitechan_ids
        """
        if not sitechan_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(instrument_id)
                    FROM
                        sensor
                    WHERE
                        sitechan_id IN %s
                    """)
            cur.execute(query, (tuple(sitechan_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(instrument_id)
                    FROM
                        sensor
                    WHERE
                        sitechan_id IN %(sitechan_ids)s
                    AND
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                    """)
            cur.execute(query, {'sitechan_ids':tuple(sitechan_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getInstrumentIdsFromSensors(self, sensor_ids, selected_datetime):
        """
        Function for getting a list of instrument_ids from sensor_ids
        """
        if not sensor_ids:
            return []

        db_conn = log2nordb()
        cur = db_conn.cursor()

        if selected_datetime is None:
            query = (   """
                    SELECT
                        DISTINCT(instrument_id)
                    FROM
                        sensor
                    WHERE
                        id IN %s
                    """)
            cur.execute(query, (tuple(sensor_ids), ))
        else:
            query = (   """
                    SELECT
                        DISTINCT(instrument_id)
                    FROM
                        sensor
                    WHERE
                        id IN %(sensor_ids)s
                    AND
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                    """)
            cur.execute(query, {'sensor_ids':tuple(sensor_ids), 's_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getStationIds(self, selected_datetime):
        """
        Function for getting a list of station ids with selected_datetime
        """
        if selected_datetime is None:
            return [s.s_id for s in self.stations]

        db_conn = log2nordb()
        cur = db_conn.cursor()

        query = (   """
                SELECT
                    DISTINCT(id)
                FROM
                    station
                WHERE
                        (
                            (station.on_date <= %(s_datetime)s AND
                            station.off_date >= %(s_datetime)s)
                        OR
                            (station.on_date <= %(s_datetime)s AND
                            station.off_date IS NULL)
                        )
                """)

        cur.execute(query, {'s_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSitechanIds(self, selected_datetime):
        """
        Function for getting a list of sitechan ids with selected_datetime
        """
        if selected_datetime is None:
            return [s.s_id for s in self.sitechans]

        db_conn = log2nordb()
        cur = db_conn.cursor()

        query = (   """
                SELECT
                    DISTINCT(id)
                FROM
                    sitechan
                WHERE
                        (
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date >= %(s_datetime)s)
                        OR
                            (sitechan.on_date <= %(s_datetime)s AND
                            sitechan.off_date IS NULL)
                        )
                """)

        cur.execute(query, {'s_datetime':selected_datetime})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getSensorIds(self, selected_datetime):
        """
        Function for getting a list of sensor ids with selected_datetime
        """
        if selected_datetime is None:
            return [s.s_id for s in self.sensors]

        db_conn = log2nordb()
        cur = db_conn.cursor()

        query = (   """
                SELECT
                    DISTINCT(id)
                FROM
                    sensor
                WHERE
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                """)

        cur.execute(query, {'s_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids

    def getInstrumentIds(self, selected_datetime):
        """
        Function for getting a list of sensor ids with selected_datetime
        """
        if selected_datetime is None:
            return [s.instruments[0].i_id for s in self.sensors]

        db_conn = log2nordb()
        cur = db_conn.cursor()

        query = (   """
                SELECT
                    DISTINCT(instrument_id)
                FROM
                    sensor
                WHERE
                        (
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime >= %(s_datetime)s)
                        OR
                            (sensor.time <= %(s_datetime)s AND
                            sensor.endtime = 9999999999.999)
                       )
                """)

        cur.execute(query, {'s_datetime':time.mktime(selected_datetime.timetuple())})

        return_ids = [a[0] for a in cur.fetchall()]

        db_conn.close()

        return return_ids


