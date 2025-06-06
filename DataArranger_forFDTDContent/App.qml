import QtQuick
import DataArranger_forFDTD

Window {
    width: mainScreen.width
    height: mainScreen.height

    visible: true
    title: "Data Arranger for FDTD"

    Screen01 {
        id: mainScreen
    }

    Window {
        id: settingsWindow
        width: 500
        height: 425
        minimumWidth: 500
        minimumHeight: 425
        visible: false
        title: "Settings"

        Loader {
            id: settingsLoader
            anchors.fill: parent
            source: "./SettingsWindow.ui.qml"  // .ui.qml を読み込む
            //onLoaded: {
            //    if (settingsLoader.item) {
                    // 必要ならさらに設定も可能
            //        settingsLoader.item.width = settingsWindow.width
            //        settingsLoader.item.height = settingsWindow.height
            //    }
            //}
        }
    }

    Connections {
        target: myUIHandler
        function onOpenSettingsWindow() {
            settingsWindow.visible = "true"
        }
    }
}
