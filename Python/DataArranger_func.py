import numpy as np
import matplotlib.pyplot as plt
from PolarizationCalculation import CalcPolarizationFDTD

class fileReading:
    def __init__(self, filePath): #初期化
        self.fPath = filePath
        self.readAll()
        
    def readAll(self): #1行ずつ読み込んでlistに格納(\nは削除)
        with open(self.fPath, "r", encoding="utf-8") as f:
            self.lines = [line.strip() for line in f.readlines()]
        return self.lines
    
    def readBetween(self, startLine, endLine): #1行目は1として指定、endLineは含まない
        return self.lines[startLine - 1:endLine-1]

def divideStr(arr): #スペースで文字列を分割
    arr = [line.split() for line in arr]
    return arr

def str2Float(arr): #文字列のlistをfloat型に
    arr = [float(s) for s in arr]
    return arr

def str2FloatArr(arr): #文字列の2重listをfloat型に
    arr = [[float(s) for s in row] for row in arr] #2重リスト(arr)の0軸の要素(1重リスト)でrowをループさせ、その中でrowの要素数でループ
    return arr

class ArrangerM1:
    def __init__(self, folderPath):
        self.folderPath = folderPath
        self.theta = np.linspace(0, 2 * np.pi, 1000)
        self.faxis = 0

    def fileInput(self):
        self.EsFile_real = fileReading(self.folderPath + "/ff_m1_opposite_Es_real.txt")
        self.EsFile_imag = fileReading(self.folderPath + "/ff_m1_opposite_Es_imag.txt")
        self.EpFile_real = fileReading(self.folderPath + "/ff_m1_opposite_Ep_real.txt")
        self.EpFile_imag = fileReading(self.folderPath + "/ff_m1_opposite_Ep_imag.txt")
    
    def extractData(self):
        self.uy = str2Float(self.EpFile_real.readBetween(4, 204))
        self.uz = str2Float(self.EpFile_real.readBetween(206, 406))

        self.Es_real = np.array(str2FloatArr(divideStr(self.EsFile_real.readBetween(408, 608))))
        self.Es_imag = np.array(str2FloatArr(divideStr(self.EsFile_imag.readBetween(408, 608))))
        self.Es = self.Es_real + 1j * self.Es_imag

        self.Ep_real = np.array(str2FloatArr(divideStr(self.EpFile_real.readBetween(408, 608))))
        self.Ep_imag = np.array(str2FloatArr(divideStr(self.EpFile_imag.readBetween(408, 608))))
        self.Ep = self.Ep_real + 1j * self.Ep_imag
    
    def calcPolarization(self):
        self.EsPP = self.Es[100, 100]
        self.EpPP = self.Ep[100, 100]
        self.EyPP = self.EsPP
        self.EzPP = -self.EpPP
        self.I = CalcPolarizationFDTD(self.EyPP, self.EzPP, self.theta, self.faxis).squeeze()

        return self.theta, self.I

if __name__ == "__main__":
    folderPath = "/Users/neirotakada/Library/CloudStorage/Box-Box/Sadgrove研究室/研究/FDTD/20250520/90deg_revised"
    arranger = ArrangerM1(folderPath)
    arranger.fileInput()
    arranger.extractData()
    theta, I = arranger.calcPolarization()

    fig, ax = plt.subplots()
    ax.plot(np.rad2deg(theta), I, label="I")
    ax.set_xlabel("Angle of QWP [deg]")
    ax.set_ylabel("Intensity [arb. units]")
    ax.legend()
    plt.show()