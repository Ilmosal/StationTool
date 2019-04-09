import QtQuick 2.0
import QtQuick.Window 2.0
import QtLocation 5.6
import QtPositioning 5.6

Canvas {
    Plugin {
        id: mapPlugin
        name: "esri"
        // specify plugin parameters if necessary
    }

    Map {
        anchors.fill: parent
        plugin: mapPlugin
        center: QtPositioning.coordinate(60.19, 25.94) // Approx Helsinki
        zoomLevel: 6
    }
}
