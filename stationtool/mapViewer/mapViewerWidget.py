"""
"""
from PyQt5.QtCore import QAbstractListModel, Qt, QModelIndex, QVariant, QCoreApplication, QPointF, QUrl, QByteArray, \
    QTimer
from PyQt5.QtWidgets import QWidget, QVBoxLayout
from PyQt5.QtQuickWidgets import QQuickWidget
from PyQt5.QtQuick import QQuickView
from PyQt5.QtGui import QColor
from PyQt5.QtQml import QQmlApplicationEngine

from dataViewer.selectionScreen import SelectionScreen

class SidePanelWidget(QWidget):
    """
    Temporary QWidget representing the map widget
    """
    def __init__(self, parent, selection_manager):
        super(QWidget, self).__init__(parent)
        self.setFixedWidth(600)
        self.map_view = MapViewWidget(self)
        self.selection_screen = SelectionScreen(self, selection_manager)
        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.selection_screen)
        self.layout.addWidget(self.map_view)
        self.setLayout(self.layout)

    def addStations(self, stations):
        """
        Add stations to MapViewWidget
        """
        self.map_view.addStations(stations)

class MapViewWidget(QQuickWidget):
    """
    Class for containing the map widget
    """
    def __init__(self, parent):
        super(QQuickWidget, self).__init__(parent)
        self.setFixedHeight(800)

        self.model = MarkerModel()
        self.active_stations = []
        self.all_stations = []
        #self.model.addMarker(MapMarker(QPointF(60.171944,24.941389), 'Steissi', QColor('red')))

        self.context = self.rootContext()
        self.context.setContextProperty('markerModel', self.model)

        self.setSource(QUrl.fromLocalFile('./mapViewer/map.qml'))
        self.setResizeMode(QQuickWidget.SizeRootObjectToView)
        self.show()

    def addStations(self, stations):
        """
        Function for adding all stations to mapViewWidget
        """
        self.model.clear()
        for stat in stations:
            self.model.addMarker(MapMarker(
                                        QPointF(stat.latitude, stat.longitude),
                                        stat.station_code,
                                        QColor('red')
                                        ))

class MapMarker(object):
    def __init__(self, position, name, color=QColor("red")):
        self._position = position
        self._name = name
        self._color = color

    def name(self):
        return self._name

    def setName(self, value):
        self._name = value

    def position(self):
        return self._position

    def setPosition(self, value):
        self._position = value

    def color(self):
        return self._color

    def setColor(self, value):
        self._color = value

class MarkerModel(QAbstractListModel):
    PositionRole = Qt.UserRole + 1
    NameRole = Qt.UserRole + 2
    ColorRole = Qt.UserRole + 3

    _roles = {PositionRole: QByteArray(b'markerPosition'),
              NameRole: QByteArray(b'markerName'),
              ColorRole: QByteArray(b'markerColor')}

    def __init__(self, parent = None):
        QAbstractListModel.__init__(self, parent)
        self._markers = []

    def rowCount(self, index=QModelIndex()):
        return len(self._markers)

    def roleNames(self):
        return self._roles

    def data(self, index, role=Qt.DisplayRole):
        if index.row() >= self.rowCount():
            return QVariant()
        marker = self._markers[index.row()]

        if role == MarkerModel.PositionRole:
            return marker.position()
        elif role == MarkerModel.NameRole:
            return marker.name()
        elif role == MarkerModel.ColorRole:
            return marker.color()

        return QVariant()

    def setData(self, index, value, role=Qt.EditRole):
        if index.isValid():
            marker = self._markers[index.row()]

            if role == MarkerModel.PositionRole:
                return marker.setPosition(value)
            elif role == MarkerModel.NameRole:
                return marker.setName(value)
            elif role == MarkerModel.ColorRole:
                return marker.setColor(value)

            self.dataChanged.emit(index, index)
            return True

        return QAbstractListModel.setData(self, index, value, role)

    def addMarker(self, marker):
        self.beginInsertRows(QModelIndex(), self.rowCount(), self.rowCount())
        self._markers.append(marker)
        self.endInsertRows()

    def flags(self, index):
        if not index.isValid():
            return Qt.ItemIsEnabled
        return QAbstractListModel.flags(index) | Qt.ItemIsEditable

    def clear(self):
        """
        Function for clearing MarkerModel
        """
        self.markers = []

