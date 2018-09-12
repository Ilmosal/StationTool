from PyQt5.QtWidgets import (   QMainWindow, QAction, QWidget, QHBoxLayout,
                                qApp)
from PyQt5.QtGui import QIcon

from dataViewer.dataViewWidget import DataViewWidget
from mapViewer.mapViewerWidget import SidePanelWidget
from other.databaseAPI import DatabaseApi
"""
This module contains the MainWindow class of the StationTool program.
The StationTool class will have all the functionality of the program inside of
it and it will pass all the messages between different parts of the program.
"""

class StationTool(QMainWindow):
    """
    The StationTool class. Defines the basic parameters of the whole program.
    """
    def __init__(self, screen_size):
        super().__init__()
        self.title = 'StationTool'
        self.left = 0
        self.top = 0
        self.width = screen_size.width()
        self.height = screen_size.height()

        self.setWindowTitle(self.title)
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.initMenuBarItems()

        self.station_tool_widget = StationToolWidget(self)
        self.setCentralWidget(self.station_tool_widget)

        self.show()

    def initMenuBarItems(self):
        """
        Function for initialising basic menu bar items.
        """
        exit_act = QAction(QIcon('exit.png'), '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.triggered.connect(qApp.quit)

        self.file_menu = self.menuBar().addMenu('&File')
        self.file_menu.addAction(exit_act)

class StationToolWidget(QWidget):
    """
    StationToolWidget contains the core functionality of the StationTool program.
    """
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.database_api = DatabaseApi()
        self.data_view_widget = DataViewWidget(self, self.database_api)
        self.side_panel_widget = SidePanelWidget(self)

        self.layout = QHBoxLayout(self)
        self.layout.addWidget(self.data_view_widget)
        self.layout.addWidget(self.side_panel_widget)

        self.setLayout(self.layout)

