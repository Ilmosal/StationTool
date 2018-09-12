from PyQt5.QtWidgets import QWidget

class SidePanelWidget(QWidget):
    """
    Temporary QWidget representing the map widget
    """
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.setFixedWidth(400)
