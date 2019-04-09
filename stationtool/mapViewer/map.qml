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

        MapItemView {
            model: markerModel
            delegate:MapQuickItem{
                anchorPoint: Qt.point(2.5, 2.5)
                coordinate: QtPositioning.coordinate(markerPosition.x, markerPosition.y)
                zoomLevel: 0
                sourceItem: Rectangle{
                    width: 16
                    height: 16
                    radius: 8
                    border.color: "black"
                    color: markerColor
                    border.width: 1

                    Text{
                        y: 12
                        text: markerName
                        font.family: "Helvetica"
                        font.pointSize: 13
                        font.bold: true
                        anchors.horizontalCenter: parent.horizontalCenter
                        color: 'black'
                    }
                }
            }
        }
    }
}
