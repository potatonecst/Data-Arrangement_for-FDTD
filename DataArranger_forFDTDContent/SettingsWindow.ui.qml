
/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick.Controls
import QtGraphs

Rectangle {
    id: root
    width: 500
    height: 425
    anchors.fill: parent

    Label {
        id: label
        x: 24
        y: 24
        text: qsTr("Settings")
        font.bold: true
        font.pointSize: 25
    }

    Item {
        id: divisionNoItem
        x: 24
        y: 60
        width: 338
        height: 48

        Label {
            id: divisionNoLabel
            x: 0
            y: 16
            text: qsTr("Division No.")
        }

        TextField {
            id: divisionNoField
            x: 140
            y: 7
            width: 155
            height: 35
            placeholderText: qsTr("Division No.")
        }
    }

    Item {
        id: fileNameItem
        x: 24
        y: 114
        width: 460
        height: 200

        Label {
            id: label1
            x: 0
            y: 8
            text: qsTr("Filename")
            font.bold: true
            font.pointSize: 18
        }

        Item {
            id: esRealFileNameItem
            x: 0
            y: 33
            width: 468
            height: 50
            Label {
                id: esRealFileNameLabel
                x: 0
                y: 16
                height: 18
                text: qsTr("Filename of Es_real")
            }

            TextField {
                id: esRealFileNameField
                x: 140
                y: 7
                width: 220
                height: 36
                placeholderText: qsTr("Real Part of Es")
            }

            Button {
                id: esRealBrowseButton
                x: 370
                y: 7
                width: 90
                height: 36
                text: qsTr("Browse")
                font.pointSize: 10

                Connections {
                    target: esRealBrowseButton
                    function onClicked() {
                        myUIHandler.setFileName("esRealFileNameField")
                    }
                }
            }
        }

        Item {
            id: esImagFileNameItem
            x: 0
            y: 87
            width: 468
            height: 50
            Label {
                id: esImagFileNameLabel
                x: 0
                y: 16
                height: 18
                text: qsTr("Filename of Es_imag")
            }

            TextField {
                id: esImagFileNameField
                x: 140
                y: 7
                width: 220
                height: 36
                placeholderText: qsTr("Imaginary Part of Es")
            }

            Button {
                id: esImagBrowseButton
                x: 370
                y: 7
                width: 90
                height: 36
                text: qsTr("Browse")
                font.pointSize: 10

                Connections {
                    target: esImagBrowseButton
                    function onClicked() {
                        myUIHandler.setFileName("esImagFileNameField")
                    }
                }
            }
        }

        Item {
            id: epRealFileNameItem
            x: 0
            y: 141
            width: 468
            height: 50
            Label {
                id: epRealFileNameLabel
                x: 0
                y: 16
                height: 18
                text: qsTr("Filename of Ep_real")
            }

            TextField {
                id: epRealFileNameField
                x: 140
                y: 7
                width: 220
                height: 36
                placeholderText: qsTr("Real Part of Ep")
            }

            Button {
                id: epRealBrowseButton
                x: 370
                y: 7
                width: 90
                height: 36
                text: qsTr("Browse")
                font.pointSize: 10

                Connections {
                    target: epRealBrowseButton
                    function onClicked() {
                        myUIHandler.setFileName("epRealFileNameField")
                    }
                }
            }
        }

        Item {
            id: epImagFileNameItem
            x: 0
            y: 197
            width: 468
            height: 50
            Label {
                id: epImagFileNameLabel
                x: 0
                y: 16
                height: 18
                text: qsTr("Filename of Ep_imag")
            }

            TextField {
                id: epImagFileNameField
                x: 140
                y: 7
                width: 220
                height: 36
                placeholderText: qsTr("Imaginary Part of Ep")
            }

            Button {
                id: epImagBrowseButton
                x: 370
                y: 7
                width: 90
                height: 36
                text: qsTr("Browse")
                font.pointSize: 10

                Connections {
                    target: epImagBrowseButton
                    function onClicked() {
                        myUIHandler.setFileName("epImagFileNameField")
                    }
                }
            }
        }
    }

    Button {
        id: settingsApplyButton
        x: 386
        y: 370
        width: 100
        height: 50
        text: qsTr("Apply")
        highlighted: true

        Connections {
            target: settingsApplyButton
            function onClicked() {
                myUIHandler.apply_settings(divisionNoField.text,
                                           esRealFileNameField.text,
                                           esImagFileNameField.text,
                                           epRealFileNameField.text,
                                           epImagFileNameField.text)
            }
        }
    }

    Connections {
        target: myUIHandler
        function onReflectValues(divNo, esRealName, esImagName, epRealName, epImagName) {
            divisionNoField.text = divNo
            esRealFileNameField.text = esRealName
            esImagFileNameField.text = esImagName
            epRealFileNameField.text = epRealName
            epImagFileNameField.text = epImagName
        }
    }

    Connections {
        target: myUIHandler
        function onSendFileName(fileName, fileNameField) {
            if (fileNameField === "esRealFileNameField")
                esRealFileNameField.text = fileName
            else if (fileNameField === "esImagFileNameField")
                esImagFileNameField.text = fileName
            else if (fileNameField === "epRealFileNameField")
                epRealFileNameField.text = fileName
            else if (fileNameField === "epImagFileNameField")
                epImagFileNameField.text = fileName
        }
    }
}
