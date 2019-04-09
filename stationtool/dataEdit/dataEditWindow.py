from PyQt5.QtWidgets import (QWidget, QHBoxLayout, QVBoxLayout, QPlainTextEdit,
                             QPushButton)
from PyQt5.QtCore import Qt

class DataEditWindow(QWidget):
    """
    Class for all data edit popup windows. Inherit this class when creating different data generation functionalities
    """
    def __init__(self, title, storage_model, fields = []):
        super().__init__()
        self.layout = QHBoxLayout()
        self.setWindowTitle(title)

        self.setGeometry(100, 100, 450, 350)

        self.help_box = HelpBox(self)
        self.help_box.setHelpField()
        self.data_edit_fields = DataEditFields(self, fields)

        self.layout.addWidget(self.data_edit_fields)
        self.layout.addWidget(self.help_box)

        self.setLayout(self.layout)

        self.storage_field = storage_model

    def setHelpText(self, text):
        """
        Function for setting the help_box text
        """
        self.help_box.setHelpField(text)

    def pushToStorage(self):
        """
        Method for pushing content to storage.
        """
        self.storage_field.insertNewDataRow(self.getDataFromFields())
        self.exitWindow()

    def clearAll(self):
        """
        Function for clearing all current fields.
        """
        self.data_edit_fields.clearAllFields()

    def exitWindow(self):
        """
        Function for exiting from window
        """
        self.close()

    def getDataFromFields(self):
        """
        Function for collecting data from all the fields
        """
        raise Exception("Get data from fields function for class {0} is not defined. ".format(self.__class__.__name__))

class DataEditButtons(QWidget):
    """
    Class for dataEditWindow buttons
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QHBoxLayout()

        self.add_button = QPushButton('Add', self)
        self.clear_button = QPushButton('Clear', self)
        self.exit_button = QPushButton('Exit', self)

        self.add_button.clicked.connect(self.addButtonFunc)
        self.clear_button.clicked.connect(self.clearButtonFunc)
        self.exit_button.clicked.connect(self.exitButtonFunc)

        self.layout.addWidget(self.add_button)
        self.layout.addWidget(self.clear_button)
        self.layout.addWidget(self.exit_button)
        self.layout.setAlignment(Qt.AlignRight)

        self.setLayout(self.layout)

    def addButtonFunc(self):
        """
        Functionality for add button
        """
        self.parent().parent().pushToStorage()

    def clearButtonFunc(self):
        """
        Functionality for clear button
        """
        self.parent().parent().clearAll()

    def exitButtonFunc(self):
        """
        Functionality for exit button
        """
        self.parent().parent().exitWindow()

class HelpBox(QWidget):
    """
    Class for handling all helpbox related functionality in the program.
    """
    def __init__(self, parent):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.text_field = QPlainTextEdit()
        self.text_field.setReadOnly(True)
        self.text_field.setMinimumWidth(200)

        self.buttons = DataEditButtons(self)

        self.layout.addWidget(self.text_field)
        self.layout.addWidget(self.buttons)

        self.setLayout(self.layout)

    def setHelpField(self, text = ""):
        """
        Function for setting the help field.
        """
        self.text_field.setPlainText(text)

class DataEditFields(QWidget):
    """
    Class for handling all edit fields what will be in DataEditWindow.
    """
    def __init__(self, parent, fields):
        super().__init__(parent)
        self.layout = QVBoxLayout()
        self.layout.setSpacing(0)

        self.fields = fields

        for field in self.fields:
            self.layout.addWidget(field)

        self.setLayout(self.layout)

    def clearAllFields(self):
        """
        Function for clearing all fields in dataEditFields class
        """
        for field in self.fields:
            field.clearField()
