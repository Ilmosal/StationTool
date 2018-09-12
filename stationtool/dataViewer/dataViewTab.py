"""
This module contains the information for a abstract DataViewTab.
"""
from operator import itemgetter
from datetime import date

from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout)
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QSortFilterProxyModel

class StationToolTableModel(QAbstractTableModel):
    """
    Class inheriting QAbstractTableModel for handling table operations for the DataViewTab objects table_view object.
    """
    def __init__(self, parent, header, data):
        QAbstractTableModel.__init__(self, parent)
        self.header_data = [h[0] for h in header]
        self.header_types = [h[1] for h in header]
        self.array_data = data

    def rowCount(self, parent):
        """
        Overrided function for calculating the number of rows
        """
        return len(self.array_data)

    def columnCount(self, parent):
        """
        Overrided function for calculating the number of columns
        """
        return len(self.header_data)

    def data(self, index, role):
        """
        Overrided function for getting data from certain index
        """
        if index.isValid() and role == Qt.DisplayRole:
            if isinstance(self.array_data[index.row()][index.column()], date):
                return QVariant("prii")
            return QVariant(self.array_data[index.row()][index.column()])
        return QVariant()

    def headerData(self, col, orientation, role):
        """
        Overrided function for getting headerData from certain column
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[col])
        return QAbstractTableModel.headerData(self, col, orientation, role)

    def sort(self, col, order = Qt.AscendingOrder):
        """
        Function for sorting a column.
        """
        self.layoutAboutToBeChanged.emit()
        self.array_data.sort(key=lambda x: (x[col] or ''))

        if order != Qt.AscendingOrder:
            self.array_data.reverse()

        self.layoutChanged.emit()
        self.parent().resizeAll()

    def insertNewDataRow(self, data):
        """
        Function for inserting a new row to the table.
        """
        if len(data) != len(self.header_data):
            return False

        for i in range (0, len(data)):
            if not isinstance(data[i], self.header_types[i]) and data[i] is not None:
                return False

        self.array_data.append(data)
        self.layoutChanged.emit()
        return True

    def clearModelData(self):
        """
        Function for clearing all Data from model
        """
        self.array_data = []
        self.layoutChanged.emit()

class AbstractDatabaseTableModel(StationToolTableModel):
    """
    Class for handling database table models. All data in this model will be fetched from the database. This data can be modified in some ways. This class needs to be extended on because of how the different database models function in the database.
    """
    def __init__(self, parent, header, data, database_api):
        StationToolTableModel.__init__(self, parent, header, data)
        self.database_api = database_api
        self.fetchDataFromDB()

    def fetchDataFromDB(self):
        """
        Function for fetching all relevant data from the database and giving them to the DatabaseTableModel. Redefine this to first clear the existing table and then fetch all data from the database_api.
        """
        raise Exception("Do not use AbstractDatabaseTableModel but inherit it to your own class")

class AbstractStorageTableModel(StationToolTableModel):
    """
    Class for handling temporary table models. All data is first imported to temporary storage table model. It will then be either abandoned or pushed to the database and then destroyed.
    """
    def __init__(self, parent, header, data, databaseModel):
        StationToolTableModel.__init__(self, parent, header, data)

    def pushDataToDatabase(self):
        """
        Function for pushing data from the storage table to the Actual database.
        """
        raise Exception("pushDataToDatabase has not been redefined! Inherit AbstractStorageTableModel to your own class and redefine pushDataToDatabase for this to work")

class DataViewTab(QWidget):
    """
    DataViewTab for handling the table data.
    """
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.database_view = QTableView()
        self.storage_view = QTableView()

        self.database_view.setSortingEnabled(True)
        self.database_view.resizeColumnsToContents()

        self.storage_view.setSortingEnabled(True)
        self.storage_view.resizeColumnsToContents()
        self.storage_view.setFixedHeight(200)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(self.database_view)
        self.layout.addWidget(self.storage_view)
        self.setLayout(self.layout)

    def resizeAll(self):
        """
        Function for resizing all necessary windows
        """
        self.database_view.resizeColumnsToContents()
        self.storage_view.resizeColumnsToContents()

    def addModels(self, database_model, storage_model):
        """
        Add models to DatabViewTab after initialisation
        """
        self.database_view.setModel(database_model)
        self.storage_view.setModel(storage_model)
        self.resizeAll()

    def updateDatabaseModel(self):
        """
        Function for updating a the databaseModel to correspond to the database.
        """
        self.database_view.model().fetchDataFromDB()
        self.database_view.resizeColumnsToContents()

    def addRowToStorage(self, data):
        """
        Function for adding a new row to the Storage Model.
        """
        self.storage_view.model().insertNewDataRow(self, data)

    def pushStorageModelToDatabase(self):
        """
        Function for pushing storage data to the database.
        """
        self.storage_view.model().pushDataToDatabase()
        self.storage_view.resizeColumnsToContents()
        self.updateDatabaseModel()
