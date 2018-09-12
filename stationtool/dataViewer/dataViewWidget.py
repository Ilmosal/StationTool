"""
This module contains DataViewWidget class, which contains all the data view widgets of the program. 
"""

from PyQt5.QtWidgets import (QWidget, QTabWidget, QVBoxLayout)
from dataViewer.stationTab import StationViewTab

class DataViewWidget(QWidget):
    """
    Class that contains all DataTab objects and allows shuffling through them easily with tabs.
    """
    def __init__(self, parent, database_api):
        super(QWidget, self).__init__(parent)
        self.tabs = QTabWidget()
        self.tabs.resize(300,200)

        self.station_tab = StationViewTab(self, database_api)
        self.tabs.addTab(self.station_tab, 'Station')

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.tabs)
        self.setLayout(self.layout)

    def updateAllTabsWith(self):
        """
        Function for updating all the tabs of the dataViewWidget.
        """
        pass
