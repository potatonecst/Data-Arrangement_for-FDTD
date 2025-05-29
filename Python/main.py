import os
import sys
from pathlib import Path
import numpy as np

from PySide6.QtQuickControls2 import QQuickStyle
from PySide6.QtGui import QGuiApplication
from PySide6.QtQml import QQmlApplicationEngine
from PySide6.QtCore import QObject, Slot, Signal, QSize
from PySide6.QtWidgets import QApplication, QMainWindow, QPushButton, QFileDialog

from autogen.settings import url, import_paths

from DataArranger_func import *

class MyUIHandler(QObject):
    folderPathSelected = Signal(str) #フォルダパスが取得されたときにそのパス（文字列）をqmlに送る
    sendPoints = Signal(list) #データ点のlistをqmlに送る
    saveImage = Signal(str)

    def __init__(self, parent=None):
        super().__init__(parent)
    
    def getObjectName(self, name):
        self.graphItem = name

    @Slot()
    def open_folder_dialog(self):
        """
        フォルダー選択ダイアログを開き、選択されたフォルダーのパスをシグナルで送信します。
        """
        print("フォルダー選択ボタンがクリックされました！")
        # getExistingDirectory() を使用してフォルダーを選択
        folder_path = QFileDialog.getExistingDirectory(
            parent = None,  # 親ウィジェット
            caption = "Select Folder", # ダイアログのタイトル
            dir = ""     # 初期ディレクトリ (空文字列でカレントディレクトリ)
        )
        if folder_path:
            print(f"選択されたフォルダー: {folder_path}")
            # 取得したフォルダーパスをQMLに送信するためにシグナルを発行
            self.folderPathSelected.emit(folder_path)
        else:
            print("フォルダー選択がキャンセルされました。")
    
    @Slot(str)
    def start_arranging(self, folderPath):
        if folderPath:
            print("Start Arranging...")
            self.arranger = ArrangerM1(folderPath)
            self.arranger.fileInput()
            self.arranger.extractData()
            self.theta, self.I= self.arranger.calcPolarization()
            self.points1 = [[float(np.rad2deg(t)), float(i1)] for t, i1 in zip(self.theta, self.I)]
            if self.sendPoints.emit(self.points1):
                print("Send successfully")
            else:
                print("Failed to send")
            #print(self.points1)

        else:
            print("Select Folder!")
            return
    
    @Slot()
    def save_graph(self):
        self.grab_result = self.graphItem.grabToImage()
        if self.grab_result:
            self.grab_result_ref = self.grab_result # 参照を保持
            self.grab_result_ref.ready.connect(self.open_file_dialog)
        else:
            print("Error: grabToImage (before \"open_file_dialog\" slot)")
        
    @Slot()
    def open_file_dialog(self):
        if self.grab_result_ref:
            self.imgFileName, _ = QFileDialog.getSaveFileName(
                parent = None,
                caption = "Save Graph",
                dir = "./Figure1.png",
                filter = "PNG Files (*.png);;JPEG Files (*.jpg *.jpeg);;All Files (*)"
            )
            if self.grab_result_ref.saveToFile(self.imgFileName):
                print("Save successfully")
            else:
                print("Failed to save")
        else:
            print("Error: (after \"open_file_dialog\" slot)")
            return

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

    # ウィンドウサイズを取得
    initial_width = root_obj.width()
    initial_height = root_obj.height()

    root_obj.setMinimumSize(QSize(initial_width, initial_height)) #最小サイズを設定

    graph_item = root_obj.findChild(QObject, "graphImage") # "graphImage" を探す
    my_ui_handler.getObjectName(graph_item)

    sys.exit(app.exec())