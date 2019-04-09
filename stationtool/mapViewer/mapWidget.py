import sys

from PyQt5.QtCore import pyqtProperty, QCoreApplication, QObject, QUrl
from PyQt5.QtWidgets import QMainWindow, QWidget, QApplication
from PyQt5.QtQml import qmlRegisterType, QQmlComponent, QQmlEngine
from PyQt5.QtQuick import QQuickView

# This is the type that will be registered with QML.  It must be a
# sub-class of QObject.
class Person(QObject):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Initialise the value of the properties.
        self._name = ''
        self._shoeSize = 0

    # Define the getter of the 'name' property.  The C++ type of the
    # property is QString which Python will convert to and from a string.
    @pyqtProperty('QString')
    def name(self):
        return self._name

    # Define the setter of the 'name' property.
    @name.setter
    def name(self, name):
        self._name = name

    # Define the getter of the 'shoeSize' property.  The C++ type and
    # Python type of the property is int.
    @pyqtProperty(int)
    def shoeSize(self):
        return self._shoeSize

    # Define the setter of the 'shoeSize' property.
    @shoeSize.setter
    def shoeSize(self, shoeSize):
        self._shoeSize = shoeSize


# Create the application instance.

app = QApplication(sys.argv)
view = QQuickView()
view.setSource(QUrl.fromLocalFile('example.qml'))
view.show()
view.setResizeMode(QQuickView.SizeRootObjectToView)

# Register the Python type.  Its URI is 'People', it's v1.0 and the type
# will be called 'Person' in QML.
#qmlRegisterType(Person, 'People', 1, 0, 'Person')

# Create a QML engine.
#engine = QQmlEngine()

# Create a component factory and load the QML script.
#component = QQmlComponent(engine)
#component.loadUrl()
#
# Create an instance of the component.
#testmap = component.create()

sys.exit(app.exec_())
