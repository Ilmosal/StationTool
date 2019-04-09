"""
This module contains DataViewWidget class, which contains all the data view widgets of the program.
"""

from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout, QAction)
from PyQt5.QtGui import QIcon
from dataViewer.stationTab import StationViewTab
from dataViewer.sitechanTab import SitechanViewTab
from dataViewer.sensorTab import SensorViewTab
from dataViewer.instrumentTab import InstrumentViewTab
from dataViewer.responseTab import ResponseTab

class DataViewWidget(QWidget):
    """
    Class that contains all DataTab objects and allows shuffling through them easily with tabs.
    """
    def __init__(self, parent, database_api, selection_manager):
        super(QWidget, self).__init__(parent)
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)

        self.selection_manager = selection_manager
        self.station_tab = StationViewTab(self, database_api, selection_manager)
        self.sitechan_tab = SitechanViewTab(self, database_api, selection_manager)
        self.sensor_tab = SensorViewTab(self, database_api, selection_manager)
        self.instrument_tab = InstrumentViewTab(self, database_api, selection_manager)
        self.response_tab = ResponseTab(self, database_api, selection_manager)

        self.tabs.addTab(self.station_tab, 'Station')
        self.tabs.addTab(self.sitechan_tab, 'Sitechan')
        self.tabs.addTab(self.sensor_tab, 'Sensor')
        self.tabs.addTab(self.instrument_tab, 'Instrument')
        self.tabs.addTab(self.response_tab, 'Response')
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

        clear_act = QAction(QIcon('exit.png'), '&Clear', self)
        clear_act.setShortcut('Ctrl+C')
        clear_act.triggered.connect(self.clearSelectionFields)

        self.addAction(clear_act)

    def clearSelectionFields(self):
        """
        Function for clearing all selections
        """
        self.selection_manager.clearAll()
        self.station_tab.updateView()
        self.sitechan_tab.updateView()
        self.sensor_tab.updateView()
        self.instrument_tab.updateView()
        self.parent().side_panel_widget.selection_screen.changeSelectedFieldLabel('None')

    def updateAllTabViews(self):
        """
        Function for updating all the tabs views
        """
        self.station_tab.updateView()
        self.sitechan_tab.updateView()
        self.sensor_tab.updateView()
        self.instrument_tab.updateView()

