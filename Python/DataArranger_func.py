import sys
import numpy as np
import matplotlib.pyplot as plt
from HybridModeSolverRevised import CalcHEMode
from PolarizationCalculationRevised import CalcPolarizationFDTD

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
    def __init__(self):
        #self.folderPath = folderPath
        self.theta = np.linspace(0, 2 * np.pi, 1000)
        self.faxis = 0
        self.sigmaX = np.array([[0, 1], #Pauli行列
                                [1, 0]])
        self.sigmaY = np.array([[0, -1j],
                                [1j, 0]])
        self.sigmaZ = np.array([[1, 0],
                                [0, -1]])
        self.divNo = 201
        self.Es_real_name = "ff_m1_opposite_Es_real.txt"
        self.Es_imag_name = "ff_m1_opposite_Es_imag.txt"
        self.Ep_real_name = "ff_m1_opposite_Ep_real.txt"
        self.Ep_imag_name = "ff_m1_opposite_Ep_imag.txt"
    
    def setFolderPath(self, folderPath):
        self.folderPath = folderPath

    def setDivisionNo(self, divNo):
        self.divNo = divNo

    def setFileName(self, fileName, EComponentVar):
        if EComponentVar == "EsReal":
            self.Es_real_name = fileName
        elif EComponentVar == "EsImag":
            self.Es_imag_name = fileName
        elif EComponentVar == "EpReal":
            self.Ep_real_name = fileName
        else:
            self.Ep_imag_name = fileName

    def fileInput(self):
        self.EsFile_real = fileReading(self.folderPath + "/" + self.Es_real_name)
        self.EsFile_imag = fileReading(self.folderPath + "/" + self.Es_imag_name)
        self.EpFile_real = fileReading(self.folderPath + "/" + self.Ep_real_name)
        self.EpFile_imag = fileReading(self.folderPath + "/" + self.Ep_imag_name)
    
    def extractData(self):
        self.ux = 1
        self.uy = np.array(str2Float(self.EpFile_real.readBetween(4, 4 + self.divNo)))
        self.uz = np.array(str2Float(self.EpFile_real.readBetween(6 + self.divNo, 6 + 2 * self.divNo)))

        self.Theta = np.arctan(np.sqrt(self.ux ** 2 + self.uy ** 2) / (self.uz + sys.float_info.epsilon))
        self.Phi = np.arctan(self.uy / self.ux)

        self.Es_real = np.array(str2FloatArr(divideStr(self.EsFile_real.readBetween(8 + 2 * self.divNo, 8 + 3 * self.divNo))))
        self.Es_imag = np.array(str2FloatArr(divideStr(self.EsFile_imag.readBetween(8 + 2 * self.divNo, 8 + 3 * self.divNo))))
        self.Es = self.Es_real + 1j * self.Es_imag

        self.Ep_real = np.array(str2FloatArr(divideStr(self.EpFile_real.readBetween(8 + 2 * self.divNo, 8 + 3 * self.divNo))))
        self.Ep_imag = np.array(str2FloatArr(divideStr(self.EpFile_imag.readBetween(8 + 2 * self.divNo, 8 + 3 * self.divNo))))
        self.Ep = self.Ep_real + 1j * self.Ep_imag
    
    def calcPolarization(self):
        self.ind = int(np.ceil(self.divNo / 2)) if self.divNo % 2 == 0 else int(np.ceil(self.divNo / 2)) - 1 #原点あるいは原点に最も近い正の点を示すindex
        print(self.ind, self.uz[self.ind])
        self.EsPP = self.Es[self.ind, self.ind]
        self.EpPP = self.Ep[self.ind, self.ind]
        #self.EyPP = self.EpPP * np.cos(self.Theta[self.ind]) * np.sin(self.Phi[self.ind]) + self.EsPP * np.cos(self.Phi[self.ind])
        #self.EzPP = -self.EpPP * np.sin(self.Theta[self.ind])
        self.EyPP = self.EsPP * np.cos(self.Theta[self.ind]) * np.sin(self.Phi[self.ind]) + self.EpPP * np.cos(self.Phi[self.ind])
        self.EzPP = -self.EsPP * np.sin(self.Theta[self.ind])
        self.pureState = np.array([[self.EzPP], #純粋状態
                                   [self.EyPP]])
        self.rho = self.pureState @ self.pureState.conj().T #純粋状態の密度行列
        self.S0 = np.trace(self.rho @ np.identity(2)).real #Stokesパラメータ
        self.s1 = (np.trace(self.rho @ self.sigmaZ) / self.S0).real
        self.s2 = (np.trace(self.rho @ self.sigmaX) / self.S0).real
        self.s3 = (np.trace(self.rho @ self.sigmaY) / self.S0).real
        self.I = CalcPolarizationFDTD(self.EyPP, self.EzPP, self.theta, self.faxis).squeeze() #QWPを通過した光の強度

        return self.s1, self.s2, self.s3, self.theta, self.I

if __name__ == "__main__":
    #folderPath = "/Users/neirotakada/Library/CloudStorage/Box-Box/Sadgrove研究室/研究/FDTD/20250520/90deg_revised_div201"
    folderPath = "/Users/neirotakada/Library/CloudStorage/Box-Box/Sadgrove研究室/研究/FDTD/20250523/minus90deg_div201"
    alpha = -np.pi/2 #HEモードの理論計算用
    arranger = ArrangerM1()
    arranger.setFolderPath(folderPath)
    arranger.setDivisionNo(201)
    arranger.fileInput()
    arranger.extractData()
    s1, s2, s3, Theta, I = arranger.calcPolarization()
    print(s1, s2, s3)
    print(s1 ** 2 + s2 ** 2 + s3 **2)

    fig, ax = plt.subplots()
    ax.plot(np.rad2deg(Theta), I)
    ax.set_xlabel("Angle of QWP [deg]")
    ax.set_ylabel("Intensity [arb. units]")
    ax.set_ylim([0, 1.1])

    a = 200e-9
    nco = 1.45
    ncl = 1.0
    n = 1
    l = 1
    lam = 785e-9
    psi = np.pi / 2
    R = a
    propDir = 0
    ExTheo, EyTheo, EzTheo = CalcHEMode(a, nco, ncl, n, l, lam, psi, R, alpha, propDir)
    #print(ExTheo, EyTheo, EzTheo)
    stateTheo = np.array([[EzTheo],
                          [EyTheo]])
    rhoTheo = stateTheo @ stateTheo.conj().T
    S0Theo = np.trace(rhoTheo @ np.identity(2)).real
    s1Theo = (np.trace(rhoTheo @ np.array([[1, 0], [0, -1]])) / S0Theo).real
    s2Theo = (np.trace(rhoTheo @ np.array([[0, 1], [1, 0]])) / S0Theo).real
    s3Theo = (np.trace(rhoTheo @ np.array([[0, -1j], [1j, 0]])) / S0Theo).real
    print("Theoretical")
    print(s1Theo, s2Theo, s3Theo)
    print(s1Theo ** 2 + s2Theo ** 2 + s3Theo ** 2)
    theta = np.linspace(0., np.pi, 19)
    phi = np.linspace(0., 2.*np.pi, 19)
    thetaMesh, phiMesh = np.meshgrid(theta, phi)
    x = np.sin(thetaMesh) * np.cos(phiMesh)
    y = np.sin(thetaMesh) * np.sin(phiMesh)
    z = np.cos(thetaMesh)
    xl = np.linspace(0, s1, 100)
    yl = np.linspace(0, s2, 100)
    zl = np.linspace(0, s3, 100)
    fig2, ax2 = plt.subplots(subplot_kw={"projection": "3d"})
    ax2.plot_wireframe(x, y, z, alpha=0.5, color="lightsteelblue")
    ax2.plot(xl, yl, zl, color="black") #線
    ax2.plot(s1, s2, s3, color="tab:red", marker="o", markersize=7, label="FDTD")
    ax2.plot(s1Theo, s2Theo, s3Theo, color="tab:green", marker="o", markersize=3, label="Simple Theoretical Calc.")
    ax2.plot(0, 0, 0, color="black", marker="o", markersize=2) #原点
    ax2.set_xlabel("S_1")
    ax2.set_ylabel("S_2")
    ax2.set_zlabel("S_3")
    ax2.legend()
    plt.show()