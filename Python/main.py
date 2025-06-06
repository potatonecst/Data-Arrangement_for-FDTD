import os
import sys
from pathlib import Path
import numpy as np

from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, QSize, QFileInfo, QPointF
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

from autogen.settings import url, import_paths

from DataArranger_func import *

class MyUIHandler(QObject):
    openSettingsWindow = Signal() #Settingsウィンドウを開く
    reflectValues = Signal(int, str, str, str, str) #Settingsで設定可能な項目の現在の値をSettingsウィンドウに反映
    sendFileName = Signal(str, str) #利用するファイル名をqmlに送る
    folderPathSelected = Signal(str) #フォルダパスが取得されたときにそのパス（文字列）をqmlに送る
    sendPoints = Signal(list) #データ点のlistをqmlに送る
    saveImage = Signal(str)
    indicatorRun = Signal() #busyIndicatorを回す
    indicatorStop = Signal() #busyIndicator止める

    def __init__(self, parent=None):
        super().__init__(parent)
        self.arranger = ArrangerM1() #DataArranger
    
    def getObjectName(self, name):
        self.graphItem = name

    @Slot()
    def open_settings_window(self):
        self.reflectValues.emit(self.arranger.divNo, self.arranger.Es_real_name, self.arranger.Es_imag_name, self.arranger.Ep_real_name, self.arranger.Ep_imag_name)
        self.openSettingsWindow.emit()

    @Slot(str)
    def setFileName(self, fileNameField):
        filePath, _ = QFileDialog.getOpenFileName(
            parent = None,
            caption = "Filename Select",
            dir = "../../"
        )
        if filePath:
            fileInfo = QFileInfo(filePath)
            fileName = fileInfo.fileName()
            self.sendFileName.emit(fileName, fileNameField)
    
    @Slot(int, str, str, str, str)
    def apply_settings(self, divNo, EsRealName, EsImagName, EpRealName, EpImagName):
        self.arranger.setDivisionNo(divNo)
        self.arranger.setFileName(EsRealName, "EsReal")
        self.arranger.setFileName(EsImagName, "EsImag")
        self.arranger.setFileName(EpRealName, "EpReal")
        self.arranger.setFileName(EpImagName, "EpImag")

    @Slot()
    def open_folder_dialog(self):
        self.indicatorRun.emit()
        #フォルダ選択
        self.folder_path = QFileDialog.getExistingDirectory(
            parent = None,  #親ウィジェット
            caption = "Select Folder", #ダイアログのタイトル
            dir = "../../" #初期ディレクトリ(空文字列でカレントディレクトリ)
        )
        if self.folder_path:
            print(f"Selected folder: {self.folder_path}")
            self.folderPathSelected.emit(self.folder_path) #取得したフォルダパスをQMLに送信する
            self.indicatorStop.emit()
        else:
            print("Cancel")
            self.indicatorStop.emit()
    
    @Slot(str)
    def start_arranging(self, folderPath):
        self.indicatorRun.emit()
        if folderPath:
            print("Start Arranging...")
            self.arranger.setFolderPath(folderPath)
            self.arranger.fileInput()
            self.arranger.extractData()
            self.s1, self.s2, self.s3, self.theta, self.I = self.arranger.calcPolarization()
            self.points1 = [[float(np.rad2deg(t)), float(i1)] for t, i1 in zip(self.theta, self.I)]
            if self.sendPoints.emit(self.points1):
                print("Send successfully")
            else:
                print("Failed to send")
                self.indicatorStop.emit()
        else:
            print("ERROR: Select Folder!")
            self.indicatorStop.emit()
    
    @Slot()
    def save_graph(self):
        self.indicatorRun.emit()
        self.grab_result = self.graphItem.grabToImage()
        if self.grab_result:
            self.grab_result_ref = self.grab_result # 参照を保持
            self.grab_result_ref.ready.connect(self.open_file_dialog)
        else:
            print("ERROR: grabToImage (before \"open_file_dialog\" slot)")
            self.indicatorStop.emit()
        
    @Slot()
    def open_file_dialog(self):
        if self.grab_result_ref:
            self.imgFileName, _ = QFileDialog.getSaveFileName(
                parent = None,
                caption = "Save Graph",
                dir = "../../FDTD_Analysis_Result/Figure1.png",
                filter = "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
            )
            if self.grab_result_ref.saveToFile(self.imgFileName):
                print("Save successfully. (Graph Image)")
                self.indicatorStop.emit()
            else:
                print("Failed to save. (Graph Image)")
                self.indicatorStop.emit()
        else:
            print("ERROR: (after \"open_file_dialog\" slot)")
            self.indicatorStop.emit()
    
    @Slot()
    def save_array_data(self):
        self.indicatorRun.emit()
        if hasattr(self, "I"):
            self.arrayFileName, _ = QFileDialog.getSaveFileName(
                parent = None,
                caption = "Save Array Data",
                dir ="../../FDTD_Analysis_Result/IArray.npy",
                filter = "NPY Files (*npy)"
            )
            if self.arrayFileName:
                np.save(self.arrayFileName, self.I)
                print("Save successfully. (Intensity Array Data)")
                self.indicatorStop.emit()
            else:
                print("Failed to save. (Intensity Array Data)")
                self.indicatorStop.emit()
        else:
            print("ERROR: Start Arranging First!")
            self.indicatorStop.emit()

if __name__ == '__main__':
    os.environ["QT_QUICK_CONTROLS_STYLE"] = "Material"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_THEME"] = "Light"
    os.environ["QT_QUICK_CONTROLS_MATERIAL_ACCENT"] = "Indigo"
    QQuickStyle.setStyle("Material")

    app = QApplication(sys.argv)
    engine = QQmlApplicationEngine()

    app_dir = Path(__file__).parent.parent

    engine.addImportPath(os.fspath(app_dir))
    for path in import_paths:
        engine.addImportPath(os.fspath(app_dir / path))

    # UIのハンドラーをQMLコンテキストに公開
    # QMLからmyUIHandlerという名前でopen_file_dialogメソッドを呼び出せるようにする
    my_ui_handler = MyUIHandler()
    engine.rootContext().setContextProperty("myUIHandler", my_ui_handler) 

    engine.load(os.fspath(app_dir/url))
    if not engine.rootObjects():
        sys.exit(-1)
    
    root_obj = engine.rootObjects()[0] #エンジンからルートオブジェクト取得（ApplicationWindow または QQuickWindow 相当）
    initial_width = root_obj.width() #ウィンドウサイズを取得
    initial_height = root_obj.height()
    root_obj.setMinimumSize(QSize(initial_width, initial_height)) #最小サイズを設定

    graph_item = root_obj.findChild(QObject, "graphImage") #"graphImage" を探す
    my_ui_handler.getObjectName(graph_item)

    sys.exit(app.exec())