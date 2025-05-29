

/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import DataArranger_forFDTD
import QtQuick.Studio.Components 1.0
import QtGraphs

Rectangle {
    id: canvas
    width: 848
    height: 800

    Label {
        id: title
        x: 24
        y: 24
        text: qsTr("Data Arranger for FDTD")
        font.pixelSize: 25
        font.styleName: "Bold"
        font.family: "Melete"
    }

    GroupItem {
        id: folderSelect
        x: 24
        y: 80

        Label {
            id: header_FolderSelect
            x: 0
            y: 0
            text: qsTr("Folder  Select")
            font.pointSize: 20
            font.bold: true
        }

        GroupItem {
            id: folderSelectComponent
            x: 0
            y: 28

            TextField {
                id: folderSelectField
                x: 0
                y: 7
                width: 500
                height: 35
                text: ""
                font.pixelSize: 15
                placeholderText: "Select Folder..."
                cursorVisible: true
                readOnly: false
            }

            Button {
                id: browseButton
                x: 525
                y: 2
                width: 108
                height: 45
                text: qsTr("Browse...")
                autoExclusive: true

                Connections {
                    target: browseButton
                    function onClicked() {
                        myUIHandler.open_folder_dialog()
                    }
                }
            }
        }
    }

    Button {
        id: startButton
        x: 674
        y: 106
        text: qsTr("Start")
        enabled: true
        highlighted: true
        icon.cache: true
        wheelEnabled: true
        checkable: false
        flat: false

        Connections {
            target: startButton
            function onClicked() {
                // ConnectionsエレメントのonClickedハンドラ内のコード
                myUIHandler.start_arranging(folderSelectField.text)
            }
        }
    }

    BusyIndicator {
        id: busyIndicator
        x: 764
        y: 9
        running: false
    }

    RoundButton {
        id: settingsButton
        x: 772
        y: 106
        text: ""
        flat: true
        highlighted: false
        icon.source: "images/icon_gear.svg"
    }

    GroupItem {
        id: graph
        x: 24
        y: 180

        Label {
            id: header_GraphArea
            x: 0
            y: 0
            text: qsTr("Graph Area")
            font.pointSize: 20
            font.bold: true
        }

        Rectangle {
            id: graphImage
            objectName: "graphImage"
            y: 28
            width: 800
            height: 500
            radius: 0
            bottomLeftRadius: 0
            topLeftRadius: 0

            GraphsView {
                id: graphArea
                x: 0
                y: 0
                width: 800
                height: 500
                marginLeft: 10
                marginBottom: 10
                axisX: ValueAxis {
                    visible: true
                    titleFont.capitalization: Font.MixedCase
                    tickAnchor: 0
                    subGridVisible: true
                    titleVisible: true
                    gridVisible: false
                    titleText: "Angle of QWP [deg.]"
                    titleFont.family: ".AppleSystemUIFont"
                    max: 360
                }
                axisY: ValueAxis {
                    visible: true
                    lineVisible: true
                    titleFont.hintingPreference: Font.PreferDefaultHinting
                    titleFont.family: ".AppleSystemUIFont"
                    subGridVisible: true
                    titleVisible: false
                    gridVisible: false
                    titleText: "Intensity [arb. units]"
                    max: 1.2
                }

                LineSeries {
                    id: lineSeries
                }
            }

            Text {
                id: yAxisText
                x: -40
                y: 28
                text: "Intensity [arb. units]"
                font.pixelSize: 13
                rotation: -90
                anchors.verticalCenter: parent.verticalCenter
                anchors.left: parent.left
                anchors.leftMargin: -40 // 必要に応じて調整
                color: "#000000"
            }
        }
    }

    Button {
        id: saveIntensityDataButton
        x: 196
        y: 724
        text: qsTr("Save Intensity Data")

        Connections {
            target: saveIntensityDataButton
            function onClicked() {
                myUIHandler.save_array_data()
            }
        }
    }

    Button {
        id: saveGraphButton
        x: 480
        y: 724
        text: qsTr("Save Graph")

        Connections {
            target: saveGraphButton
            function onClicked() {
                myUIHandler.save_graph()
            }
        }
    }

    Connections {
        target: myUIHandler
        function onIndicatorRun() {
            busyIndicator.running = true
        }
    }

    Connections {
        target: myUIHandler
        function onIndicatorStop() {
            busyIndicator.running = false
        }
    }

    Connections {
        target: myUIHandler
        function onFolderPathSelected(path) {
            folderSelectField.text = path
        }
    }

    Connections {
        target: myUIHandler
        function onSendPoints(pointsArray) {
            lineSeries.replace(pointsArray)
        }
    }
}
