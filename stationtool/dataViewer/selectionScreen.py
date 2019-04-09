"""
This module contains the class definition for selectionScreen object.
"""

from PyQt5.QtWidgets import QWidget, QGridLayout, QLabel, QDateTimeEdit, QPushButton, QSizePolicy
from PyQt5.QtCore import Qt

class SelectionScreen(QWidget):
    """
    Screen for showing and modifying current selections
    """
    def __init__(self, parent, selection_manager):
        super().__init__(parent)
        self.selection_manager = selection_manager

        layout = QGridLayout(self)
        layout.setColumnMinimumWidth(0, 0)
        layout.setColumnMinimumWidth(1, 0)
        layout.setColumnMinimumWidth(2, 0)
        layout.setColumnMinimumWidth(3, 400)
        layout.setSpacing(5)
        label_size = 200

        self.date_label = QLabel('Date ', self)
        self.date_label.setAlignment(Qt.AlignRight)

        self.date_widget = QDateTimeEdit(self)
        self.date_widget.setDisplayFormat("dd-MM-yyyy")
        self.date_widget.setCalendarPopup(True)
        self.date_widget.setAlignment(Qt.AlignLeft)
        self.date_widget.setFixedWidth(label_size)
        self.date_widget.dateChanged.connect(self.handleSelectDate)
        self.date_widget.setEnabled(False)

        self.enable_date_button = QPushButton('Enable', self)
        self.enable_date_button.clicked.connect(self.enableSelectDate)
        self.enabled = False

        self.clear_all_button = QPushButton('Clear', self)
        self.clear_all_button.clicked.connect(self.clearAllSelections)

        self.selected_label = QLabel('Selected: ', self)
        self.selected_label.setAlignment(Qt.AlignRight)

        self.selected_field = QLabel('None', self)
        self.selected_field.setAlignment(Qt.AlignLeft)

        empty_widget = QWidget()
        empty_widget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Preferred)

        layout.addWidget(self.date_label, 0, 0,)
        layout.addWidget(self.date_widget, 0, 1)
        layout.addWidget(self.enable_date_button, 0, 2)
        layout.addWidget(self.selected_label, 1, 0)
        layout.addWidget(self.selected_field, 1, 1)
        layout.addWidget(self.clear_all_button, 1, 2)
        layout.addWidget(empty_widget, 2, 0)
        self.setLayout(layout)

    def clearAllSelections(self):
        """
        Function for clearing all selections
        """
        self.parent().parent().clearSelections()

    def updateViews(self):
        """
        Function for updating all views
        """
        self.parent().parent().updateDataViewWidget()

    def enableSelectDate(self):
        """
        Function for clearing date selection
        """
        if self.enabled:
            self.date_widget.setEnabled(False)
            self.selection_manager.clearDate()
            self.enabled = False
            self.enable_date_button.setText('Enable')
        else:
            self.date_widget.setEnabled(True)
            self.selection_manager.selectDate(self.date_widget.date().toPyDate())
            self.enabled = True
            self.enable_date_button.setText('Disable')

        self.updateViews()

    def handleSelectDate(self, new_date):
        """
        Function that handles select date changes
        """
        self.selection_manager.selectDate(new_date.toPyDate())

    def changeSelectedFieldLabel(self, new_text):
        """
        Function for changing the label text
        """
        self.selected_field.setText(new_text)
