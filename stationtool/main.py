"""
Main script of the StationTool. Starts the program and does nothing else.
"""
import sys

from PyQt5.QtWidgets import QApplication

from stationTool import StationTool

if __name__ == '__main__':
    app = QApplication(sys.argv)
    screen_size = QApplication.desktop().screenGeometry()
    ex = StationTool(screen_size)
    sys.exit(app.exec_())
