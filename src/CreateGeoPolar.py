# commandPort -n "localhost:7001" -stp "mel"
import maya.cmds as mc
import math as m

########################################
#             Facilities               #
########################################

class Vector:
    def __init__(self, *args):
        self.x = args[0]
        self.y = args[1]
        self.z = args[2]
        
    def __add__(self, other):
        return Vector(self.x + other.x, self.y + other.y, self.z + other.z )
    
    #operator - overload
    def __sub__(self, other):
        return Vector(self.x - other.x, self.y - other.y, self.z - other.z )
    
    # operator * overload
    def __mul__(self, scalar):
        return Vector(self.x * scalar, self.y * scalar, self.z * scalar)
    
    def __truediv__(self, scalar):
        return Vector(self.x/scalar, self.y/scalar, self.z/scalar)
    
    def GetLength(self):
        return (self.x ** 2 + self.y ** 2 + self.z **2) ** 0.5
    
    def GetNormalized(self):
        return self/self.GetLength()
    
    def __str__(self):
        return f"<{self.x},{self.y},{self.z}>"

def GetObjPos(obj):
    pos = mc.xform(obj, t=True, q=True, ws=True)
    return Vector(pos[0], pos[1], pos[2])

def SetObjPos(obj, pos: Vector):
    mc.setAttr(obj + ".translate", pos.x, pos.y, pos.z, type = "float3")

class GeoCreator:
    def __init__(self):  
        self.geoSize = 10
        self.radialValue = 10
        self.thetaValue = 30
        self.color = []

    def CreateGeoCube(self):
        colorR = self.color[0] 
        colorG = self.color[1] 
        colorB = self.color[2] 







########################################
#             UI                       #
########################################
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QColorDialog, QCheckBox
from PySide2.QtGui import QDoubleValidator, QColor, QPainter, QPalette, QPixmap

class ColorPickerWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.color = QColor(0,0,0)
        self.masterLayout = QVBoxLayout()   
        self.setLayout(self.masterLayout)
        self.button = QPushButton()
        self.button.clicked.connect(self.ButtonPressed)
        self.setAutoFillBackground(True)
        self.masterLayout.addWidget(self.button)
        self.setFixedSize(200,50)
        self.colorD = QColorDialog()

    def ButtonPressed(self, event):
        self.colorD = QColorDialog(self.color)
        self.color = QColor(self.colorD.getColor())
        print(self.color.name())
        
        self.button.setStyleSheet(f"background-color : {self.color.name()}")

        print(f"Button {self.color.name()}")
        
    def paintEvent(self, event):
        self.colorD = QColorDialog().setCurrentColor(self.color) 
        self.button.setStyleSheet(f"background-color : {self.color.name()}")

        

class ThreeJntChainWiget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Create Three Joint Chain")
        self.setGeometry(0,0,300,300)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)

        ctrlSettingLayout = QVBoxLayout()
        radialCordinateLabel = QLabel("Radial Cordinate Value: ")
        ctrlSettingLayout.addWidget(radialCordinateLabel)

        self.radialValue = QLineEdit()
        self.radialValue.setValidator(QDoubleValidator())
        self.radialValue.textChanged.connect(self.RadialValueSet)
        self.radialValue.setText("10") # probably broken
        ctrlSettingLayout.addWidget(self.radialValue)

        thetaCordinateLabel = QLabel("Theta Cordinate Value: ")
        ctrlSettingLayout.addWidget(thetaCordinateLabel)

        self.thetaValue = QLineEdit()
        self.thetaValue.setValidator(QDoubleValidator())
        self.thetaValue.textChanged.connect(self.ThetaValueSet)
        self.thetaValue.setText("30") # probably broken
        ctrlSettingLayout.addWidget(self.thetaValue)

        ctrlSizeLabel = QLabel("Geo Size: ")
        ctrlSettingLayout.addWidget(ctrlSizeLabel)

        self.ctrlSize = QLineEdit()
        self.ctrlSize.setValidator(QDoubleValidator())
        self.ctrlSize.textChanged.connect(self.CtrlSizeValueSet)
        self.ctrlSize.setText("10") # probably broken
        ctrlSettingLayout.addWidget(self.ctrlSize)

        self.masterLayout.addLayout(ctrlSettingLayout)

        self.colorPicker = ColorPickerWidget()
        self.masterLayout.addWidget(self.colorPicker)

        rigThreeJntchainBtn = QPushButton("Create Geo From Polar Cord")
        self.masterLayout.addWidget(rigThreeJntchainBtn)
        rigThreeJntchainBtn.clicked.connect(self.CreateGeoBtnClicked)


        self.adjustSize()
        self.geoCreator = GeoCreator()
    
    def CreateGeoBtnClicked(self):
        print("Rig Button Pressed")
        self.geoCreator.colorR = self.colorPicker.color.redF()
        self.geoCreator.colorG = self.colorPicker.color.greenF()
        self.geoCreator.colorB = self.colorPicker.color.blueF()
        print(self.colorPicker.color)
        self.geoCreator.CreateGeoCube()
    
    def CtrlSizeValueSet(self, valStr:str):
        size = float(valStr)
        self.geoCreator.ctrlSize = size
    def RadialValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.radialValue = val

    def ThetaValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.thetaValue = val

threeJntChainWidget = ThreeJntChainWiget()
threeJntChainWidget.show()