"""
This module contains the information for a abstract DataViewTab.
"""
from operator import itemgetter
from datetime import date

from PyQt5.QtWidgets import (QWidget, QTableView, QVBoxLayout, QHBoxLayout, QApplication, QFileDialog)
from PyQt5.QtCore import QAbstractTableModel, QVariant, Qt, QSortFilterProxyModel
from PyQt5.QtGui import QColor, QBrush

from other.utils import convertValue

class StationToolTableModel(QAbstractTableModel):
    """
    Class inheriting QAbstractTableModel for handling table operations for the DataViewTab objects table_view object.
    """
    def __init__(self, parent, header, data, editable = False):
        QAbstractTableModel.__init__(self, parent)
        self.header_data = [h[0] for h in header]
        self.header_types = [h[1] for h in header]
        self.array_data = data
        self.editable = editable

    def removeSelectedFromTable(self, index):
        """
        Remove selected row from table
        """
        if index != -1 or index >= len(self.array_data):
            del self.array_data[index]
            self.layoutChanged.emit()

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

    def flags(self, index):
        """
        Overrided flags function for enabling data editing
        """
        if self.editable:
            return Qt.ItemIsEnabled | Qt.ItemIsEditable
        else:
            return Qt.ItemIsEnabled

    def setData(self, index, value, role):
        """
        Overridden function for setting data
        """
        if self.editable and index.isValid():
            data_value = convertValue(value, self.header_types[index.column()])
            if data_value is not None:
                try:
                    self.array_data[index.row()][index.column()] = data_value
                except:
                    return False
                self.parent().resizeAll()
                self.layoutChanged.emit()
                return True
        return False

    def data(self, index, role):
        """
        Overrided function for getting data from certain index
        """
        if index.isValid():
            if role == Qt.BackgroundRole:
                if self.array_data[index.row()][0] not in self.getSelectedIds() and len(self.getSelectedIds()) != 0:
                    return QVariant(QBrush(QColor('lightGray')))
                else:
                    return QVariant(QBrush(QColor('white')))
            if role == Qt.DisplayRole:
                if isinstance(self.array_data[index.row()][index.column()], date):
                    return QVariant(self.array_data[index.row()][index.column()].strftime("%d/%m/%Y"))
                return QVariant(self.array_data[index.row()][index.column()])
        return QVariant()

    def headerData(self, col, orientation, role):
        """
        Overrided function for getting headerData from certain column
        """
        if orientation == Qt.Horizontal and role == Qt.DisplayRole:
            return QVariant(self.header_data[col])
        return QAbstractTableModel.headerData(self, col, orientation, role)

    def getSelectedIds(self):
        """
        Function for getting the selected ids for sorting. Override this!
        """
        raise Exception("Do not use this function but override it in the child objects!")

    def updateTab(self):
        """
        Function for updating the this tab
        """
        self.layoutAboutToBeChanged.emit()
        self.layoutChanged.emit()

    def sort(self, col, order = Qt.AscendingOrder):
        """
        Function for sorting a column.
        """
        self.layoutAboutToBeChanged.emit()

        chosen = []
        not_chosen = []
        chosen_ids = self.getSelectedIds()

        for data in self.array_data:
            if data[0] in chosen_ids:
                chosen.append(data)
            else:
                not_chosen.append(data)

        if self.header_types[col] is str:
            chosen.sort(key=lambda x: x[col] or '')
            not_chosen.sort(key=lambda x: x[col] or '')
        elif self.header_types[col] is float:
            chosen.sort(key=lambda x: x[col] or -99999999999.999)
            not_chosen.sort(key=lambda x: x[col] or -99999999999.999)
        elif self.header_types[col] is int:
            chosen.sort(key=lambda x: x[col] or -99999999999)
            not_chosen.sort(key=lambda x: x[col] or -99999999999)
        elif self.header_types[col] is date:
            chosen.sort(key=lambda x: x[col] or date(1900,1,1))
            not_chosen.sort(key=lambda x: x[col] or date(1900,1,1))
        elif self.header_types[col] is datetime:
            chosen.sort(key=lambda x: x[col] or datetime(1900,1,1))
            not_chosen.sort(key=lambda x: x[col] or datetime(1900,1,1))

        if order != Qt.AscendingOrder:
            chosen.reverse()
            not_chosen.reverse()

        self.array_data = chosen + not_chosen

        self.layoutChanged.emit()

    def insertNewDataRow(self, data):
        """
        Function for inserting a new row to the table.
        """
        if len(data) != len(self.header_data):
            raise Exception("Data array not of right length: expected {0} received {1}".format(len(self.header_data), len(data)))

        for i in range (0, len(data)):
            if not isinstance(data[i], self.header_types[i]) and data[i] is not None:
                raise Exception("Data not of right type: expected {0} received {1}".format(self.header_types[i], type(data[i])))

        self.array_data.append(data)
        self.layoutChanged.emit()
        self.parent().resizeAll()
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
        StationToolTableModel.__init__(self, parent, header, data, False)
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
    def __init__(self, parent, header, data, database_model):
        StationToolTableModel.__init__(self, parent, header, data, True)
        self.database_model = database_model

    def getSelectedIds(self):
        """
        Overridden function for getSelectedIds
        """
        return []

    def pushDataToDatabase(self):
        """
        Function for pushing data from the storage table to the Actual database.
        """
        raise Exception("pushDataToDatabase has not been redefined! Inherit AbstractStorageTableModel to your own class and redefine pushDataToDatabase for this to work")

class DataViewTab(QWidget):
    """
    DataViewTab for handling the table data.
    """
    def __init__(self, parent, buttons = None):
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

        if buttons is not None:
            self.layout.addWidget(buttons)

        self.setLayout(self.layout)

        self.selected_id = -1
        self.selected_storage_id = -1
        self.database_view.clicked.connect(self.saveDataRowID)
        self.storage_view.clicked.connect(self.saveStorageRowID)

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
        self.storage_view.model().insertNewDataRow(data)

    def pushStorageModelToDatabase(self):
        """
        Function for pushing storage data to the database.
        """
        self.storage_view.model().pushDataToDatabase()
        self.storage_view.resizeColumnsToContents()
        self.updateDatabaseModel()

    def saveDataRowID(self, index):
        """
        Function for saving the database id of the clicked data row
        """
        if index.isValid():
            #modifiers = QApplication.keyboardModifiers()
            #if modifiers == Qt.ControlModifier:
            self.addIdToSelection(index.sibling(index.row(), 0).data())
            self.database_view.model().sort(0)

    def saveStorageRowID(self, index):
        """
        Save a storage id of a station
        """
        if index.isValid():
            self.selected_storage_id = index.row()

    def addIdToSelection(self, selected_id):
        """
        Function that needs to be overridden
        """
        raise Exception("Override this function")

    def updateView(self):
        """
        Function for updating views of this tab
        """
        self.database_view.model().updateTab()
        self.storage_view.model().updateTab()

    def removeSelectedFromStorage(self):
        """
        Remove selected id from storage
        """
        self.storage_view.model().removeSelectedFromTable(self.selected_storage_id)

class DataViewTabButtons(QWidget):
    """
    Class for handling all dataview tab button operations
    """
    def __init__(self, buttons):
        QWidget.__init__(self)
        self.layout = QHBoxLayout()
        self.buttons = buttons

        for button in buttons:
            button.setFixedWidth(100)
            self.layout.addWidget(button)

        self.setLayout(self.layout)
        self.layout.setAlignment(Qt.AlignRight)

