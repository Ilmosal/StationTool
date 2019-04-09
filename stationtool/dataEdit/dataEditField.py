"""
Module that contains all dataEditFields.
"""
from datetime import datetime
from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QLabel, QDateTimeEdit,
                             QDoubleSpinBox, QSpinBox, QLineEdit, QComboBox,
                             QFileDialog, QPushButton, QCheckBox,
                             QGridLayout)
from nordb.nordic.response import readResponseArrayToResponse
from pathlib import Path
from PyQt5.QtCore import Qt
from other.utils import qDate2Date, qDateTime2Datetime

class DataEditField(QWidget):
    """
    Abstract class for all edit fields
    """
    def __init__(self, parent, title, help_text, field):
        super(QWidget, self).__init__()
        self.label = QLabel(title)
        self.help_text = help_text
        self.layout = QHBoxLayout()

        self.setFixedHeight(50)
        self.field.setFixedWidth(220)
        self.label.setAlignment(Qt.AlignRight)

        self.layout.addWidget(self.label)
        self.layout.addWidget(self.field)

        self.setLayout(self.layout)

    def enterEvent(self, event):
        """
        Send the help text to the parent
        """
        self.parent().parent().setHelpText(self.help_text)

    def clearField(self):
        """
        Clear the current field
        """
        raise Exception("Default clearing method called! Please implement clearing for {0}".format(self.__class__.__name__))

    def getValue(self):
        """
        Get the value of the field
        """
        raise Exception("getValue function not defined with class {0}".format(self.__class__.__name__))

class DateEditField(DataEditField):
    """
    Class for editing date fields.
    """
    def __init__(self, parent, title, help_text):
        self.field = QDateTimeEdit(datetime.now().date())
        self.field.setCalendarPopup(True)
        self.field.setDisplayFormat("dd-MM-yyyy")

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Set field to current date
        """
        self.field.setDate(datetime.now().date())

    def getValue(self):
        """
        Get value of DateEditField
        """
        return qDate2Date(self.field.date())

class DatetimeEditField(DataEditField):
    """
    Class for editing datetime fields.
    """
    def __init__(self, parent, title, help_text):
        self.field = QDateTimeEdit(datetime.now())
        self.field.setCalendarPopup(True)
        self.field.setDisplayFormat("dd-MM-yyyy hh:mm:ss")

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Set field to current datetime
        """
        self.field.setDateTime(datetime.now())

    def getValue(self):
        """
        Get value of DateTimeEditField
        """
        return qDateTime2Datetime(self.field.dateTime())

class FloatEditField(DataEditField):
    """
    Class for editing float field.
    """
    def __init__(self, parent, title, help_text, min_val = None, max_val = None, decimals = 4, default_val = None):
        if default_val is None:
            self.default_val = (min_val + max_val)/2
        else:
            self.default_val = default_val
        self.field = QDoubleSpinBox()
        self.field.setStyleSheet("background: white")
        self.field.setDecimals(decimals)
        if min_val is not None:
            self.field.setMinimum(min_val)
        else:
            min_val = 0.0
        if max_val is not None:
            self.field.setMaximum(max_val)
        else:
            max_val = 0.0

        self.field.setValue(self.default_val)

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Set float to default value
        """
        self.field.setValue(self.default_val)

    def getValue(self):
        """
        Get the value of FloatEditField
        """
        return self.field.value()

class IntegerEditField(DataEditField):
    """
    Class for editing integer field.
    """
    def __init__(self, parent, title, help_text, min_val = None, max_val = None, default_val = None):
        self.field = QSpinBox()
        self.field.setStyleSheet("background: white")
        if min_val is not None:
            self.field.setMinimum(min_val)
        else:
            min_val = 0
        if max_val is not None:
            self.field.setMaximum(max_val)
        else:
            max_val = 0

        if default_val is None:
            self.default_val = (min_val + max_val) / 2
        else:
            self.default_val = default_val

        self.field.setValue(self.default_val)

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Set integer to default value
        """
        self.field.setValue(self.default_val)

    def getValue(self):
        """
        Get the value of IntegerEditField
        """
        return self.field.value()

class ResponseEditField(DataEditField):
    """
    Field for picking up a response file
    """
    def __init__(self, parent, title, help_text, database_api):
        self.field = QLineEdit()
        self.field.setReadOnly(True)

        DataEditField.__init__(self, parent, title, help_text, self.field)
        self.file_button = QPushButton('From file', self)
        self.file_button.clicked.connect(self.readResponseFile)
        self.db_button = QPushButton('From database', self)
        self.db_button.clicked.connect(self.readResponseDB)

        self.response = None
        self.database_api = database_api

        self.layout.addWidget(self.file_button)
        self.layout.addWidget(self.db_button)

    def readResponseFile(self):
        """
        Function for reading a response file
        """
        resp_filename = QFileDialog.getOpenFileName(self, "Open Response File", str(Path.home()), '') 
        try:
            resp_file = open(resp_filename[0], 'r')
        except:
            print("Couldn't get any files from QFileDialog")
            return

        try:
            response = readResponseArrayToResponse(resp_file.read().split('\n'), resp_filename[0].split('/')[-1])
        except Exception as e:
            response = None
            print("Not a valid response file: {0}".format(e))

        resp_file.close()

        if response is not None:
            self.setResponse(response)

    def setResponse(self, response):
        """
        Set the current response
        """
        self.response = response
        self.field.setText(response.file_name)

    def readResponseDB(self):
        """
        Function for reading the response from the database
        """
        self.widget = ResponseFilePicker(self, self.database_api)
        self.widget.show()

    def clearField(self):
        """
        Clear the response
        """
        self.response = None
        self.field.setText('')

    def getValue(self):
        return self.response

class StringEditField(DataEditField):
    """
    Class for editing string fields
    """
    def __init__(self, parent, title, help_text, max_len = None):
        self.field = QLineEdit()
        self.field.setStyleSheet("background: white")

        if max_len is not None:
            self.field.setMaxLength(max_len)

        self.field.setText("")

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Clear string field value
        """
        self.field.setText("")

    def getValue(self):
        """
        Get the value of StringEditField
        """
        return self.field.text()

class CheckBoxEditField(DataEditField):
    """
    Class for handling checkboxes
    """
    def __init__(self, parent, title, help_text, choices):
        self.field = CheckBoxFields(self, choices)

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Clear all the checkboxes in the CheckBoxFields class
        """
        self.field.clearFields()

    def getValue(self):
        """
        get all the string values from the CheckBoxFields
        """
        return self.field.getValues()

class CheckBoxFields(QWidget):
    """
    Container for multiple checkboxes
    """
    def __init__(self, parent, choices):
        QWidget.__init__(self, parent)
        self.layout = QHBoxLayout(self)
        self.checkboxes = []

        for choice in choices:
            self.checkboxes.append(QCheckBox(choice, self))

        for cbox in self.checkboxes:
            self.layout.addWidget(cbox)

        self.layout.setAlignment(Qt.AlignLeft)

    def getValues(self):
        """
        Get all values from the checkboxes
        """
        result = []
        for cbox in self.checkboxes:
            if cbox.isChecked():
                result.append(cbox.text())

        return result

    def clearFields(self):
        """
        Clear all fields
        """
        for cbox in self.checkboxes:
            cbox.setChecked(False)

class ChoiceEditField(DataEditField):
    """
    Class for editing choice fields
    """
    def __init__(self, parent, title, help_text, choices):
        self.field = QComboBox()
        for c in choices:
            self.field.addItem(c)

        DataEditField.__init__(self, parent, title, help_text, self.field)

    def clearField(self):
        """
        Set choice edit field to its first value
        """
        self.field.setCurrentIndex(0)

    def getValue(self):
        """
        Get the value of ChoiceEditField
        """
        return self.field.currentText()

class ResponseFilePicker(QWidget):
    """
    Window to picking a response from database
    """
    def __init__(self, response_edit, database_api):
        super().__init__()
        self.response_edit = response_edit
        self.database_api = database_api
        self.setWindowTitle("Pick a response from database")

        self.response_label = QLabel('Response', self)
        self.response_names = set([ins.dfile for ins in self.database_api.getInstruments()])
        self.response_box = QComboBox(self)
        self.response_box.addItems(self.response_names)

        self.cancel_btn = QPushButton('Cancel', self)
        self.cancel_btn.clicked.connect(self.pressCancel)
        self.add_btn = QPushButton('Add', self)
        self.add_btn.clicked.connect(self.pressAdd)

        self.layout = QGridLayout(self)
        self.layout.addWidget(self.response_label, 0, 0)
        self.layout.addWidget(self.response_box, 0, 1, 1, 2)
        self.layout.addWidget(self.cancel_btn, 1, 1)
        self.layout.addWidget(self.add_btn, 1, 2)

        self.setLayout(self.layout)

    def pressCancel(self):
        """
        Cancel button is pressed
        """
        self.close()

    def pressAdd(self):
        """
        Add button is pressed
        """
        for ins in self.database_api.getInstruments():
            if ins.dfile == self.response_box.currentText():
                self.response_edit.setResponse(ins.response)
                self.close()
