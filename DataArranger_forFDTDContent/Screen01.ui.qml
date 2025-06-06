
/*
This is a UI file (.ui.qml) that is intended to be edited in Qt Design Studio only.
It is supposed to be strictly declarative and only uses a subset of QML. If you edit
this file manually, you might introduce QML code that is not supported by Qt Design Studio.
Check out https://doc.qt.io/qtcreator/creator-quick-ui-forms.html for details on .ui.qml files.
*/
import QtQuick
import QtQuick3D
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

        Connections {
            target: settingsButton
            function onClicked() {
                myUIHandler.open_settings_window()
            }
        }
    }

    GroupItem {
        id: graph
        x: 24
        y: 180
        height: 540

        Label {
            id: header_GraphArea
            x: 0
            y: 6
            text: qsTr("Graph Area")
            font.pointSize: 20
            font.bold: true
        }

        ComboBox {
            id: graphSelect
            x: 110
            y: 0
            width: 153
            height: 35
            visible: false
            font.pointSize: 13
            model: ["QWP", "Poincaré Sphere"]
            currentIndex: 0
        }

        Rectangle {
            id: graphImage
            objectName: "graphImage"
            y: 39
            width: 800
            height: 500
            radius: 0
            bottomLeftRadius: 0
            topLeftRadius: 0

            GroupItem {
                id: graphQWP
                x: 0
                y: 0
                anchors.fill: parent
                //visible: true
                visible: graphSelect.currentIndex === 0

                GraphsView {
                    id: graphAreaQWP
                    x: 0
                    y: 0
                    width: 800
                    height: 500
                    marginLeft: 10
                    marginBottom: 10
                    visible: true
                    axisX: ValueAxis {
                        visible: true
                        tickInterval: 45
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
                        max: 1.1
                    }

                    LineSeries {
                        id: lineSeries
                        color: "blue"
                    }
                }

                Text {
                    id: yAxisTextQWP
                    x: -40
                    y: 242
                    visible: true
                    text: "Intensity [arb. units]"
                    font.pixelSize: 13
                    rotation: -90
                    // 必要に応じて調整
                    color: "#000000"
                }
            }

            Item {
                id: graphPoincare
                width: 200
                height: 200
            }


            /*View3D {
                id: graphAreaPS
                anchors.fill: parent

                visible: false
                //visible: graphSelect.currentIndex === 1 // 表示切り替え
                environment: SceneEnvironment {
                    clearColor: "#303030"
                    //clearColor: "#FFFFEE"
                    backgroundMode: SceneEnvironment.Color
                    // lightProbe: ProceduralSkyLightProbe {} // 必要に応じて
                }

                PerspectiveCamera {
                    id: cameraPS
                    position: Qt.vector3d(0, 0, 3) // 例: 球から少し離れた位置
                    //lookAt: Qt.vector3d(0, 0, 0) // 例: 球の中心を見る
                    eulerRotation: Qt.vector3d(0, 0, 0)
                }

                DirectionalLight {
                    eulerRotation.x: -45
                }

                // ポアンカレ球の本体 (半透明の球メッシュ)
                Model {
                    id: poincareSphereBody
                    source: "meshes/sphere_001_mesh.mesh" // 球メッシュのパス (リソースに追加するか、ローカルパスを指定)
                    materials: [poincareSphereBodyMaterial]
                    //scale: Qt.vector3d(1, 1, 1) // 球の半径が1になるように調整
                }

                // 軸の描画 (例: 細いシリンダーモデルを使用)
                // Model { source: "qrc:/meshes/axis_cylinder.obj"; position: ...; rotation: ...; scale: ...; materials: ... }
                // (X, Y, Z軸それぞれに配置)

                // ストークスパラメータの点をプロット
                Node {
                    // Repeater3Dの親Node
                    Repeater3D {
                        id: stokesPointsRepeater
                        model: myUIHandler.stokesPointsModel // Python側から供給するデータモデル (QAbstractListModel推奨)

                        // 例: [{x:0, y:0, z:1, color:"red"}, ...]
                        delegate: Model {
                            source: "#Sphere" // 小さな球で点を表現
                            scale: Qt.vector3d(0.05, 0.05, 0.05) // 点のサイズ
                            position: Qt.vector3d(
                                          modelData.x, modelData.y,
                                          modelData.z) // modelDataから座標を取得
                        }
                    }
                }
            }*/
        }

        Button {
            id: saveIntensityDataButton
            x: 196
            y: 551
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
            y: 551
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
                lineSeries.clear()
                //lineSeries.replace(pointsArray)
                for (var i = 0; i < pointsArray.length; i++) {
                    //var pt = pointsArray[i]
                    lineSeries.append(pointsArray[i][0], pointsArray[i][1])
                }
                busyIndicator.running = false
            }
        }
    }

    Item {
        id: __materialLibrary__

        PrincipledMaterial {
            id: poincareSphereBodyMaterial
            objectName: "poincareSphereBodyMaterial"
            baseColor: Qt.rgba(0.7, 0.7, 0.8, 0.3) // 半透明
            metalness: 0.1
            roughness: 0.7
            alphaMode: PrincipledMaterial.Blend
        }

        PrincipledMaterial {
            objectName: ""
            //baseColor: modelData.color // modelDataから色を取得
        }
    }
}

/*##^##
Designer {
    D{i:0;matPrevEnvDoc:"SkyBox";matPrevEnvValueDoc:"preview_studio";matPrevModelDoc:"#Sphere"}
}
##^##*/

