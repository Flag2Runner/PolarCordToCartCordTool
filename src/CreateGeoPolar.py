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
        self.polarValue = 30
        self.alphaValue = 30
        self.color = [128,128,128]

    def UpdateColors(self, r,g,b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b

    def CreateGeoCube(self):
        x = self.radialValue * m.sin(self.polarValue) * m.cos(self.alphaValue)
        y = self.radialValue * m.sin(self.polarValue) * m.sin(self.alphaValue)
        z = self.radialValue * m.cos(self.polarValue)

        if mc.objExists(self.PolyName()):
            mc.delete(self.PolyName())

        mc.polyCube(n = self.PolyName(), ax =[0,0,90], h = self.geoSize, w = self.geoSize)

        mc.move(x, y, z, f"{self.PolyName()}", absolute=True, ws = True)
       
        self.CreateMaterialForCube()

    def CreateMaterialForCube(self):
        r = self.color[0] 
        g = self.color[1] 
        b = self.color[2] 
        matName = self.GetShaderNameForCube(self.PolyName())
        if not mc.objExists(matName):
            mc.shadingNode("lambert", asShader = True, name = matName) 

        setName = self.GetShaderEngineForCube(self.PolyName())
        if not mc.objExists(setName):
            mc.sets(name = setName, renderable = True, empty = True)

        mc.connectAttr(matName + ".outColor", setName + ".surfaceShader", force = True)
        mc.sets(self.PolyName(), edit=True, forceElement = setName)

        self.SetGhostColor(r,g,b)

    def SetGhostColor(self, r, g, b):
        ghostMat = self.GetShaderNameForCube(self.PolyName())
        mc.setAttr(ghostMat + ".color", r, g, b, type = "double3")

    def PolyName(self):
        return "Cube"
    
    def GetShaderEngineForCube(self, cube):
        return cube + "_sg"
    
    def GetShaderNameForCube(self, cube):
        return cube + "_mat"





########################################
#             UI                       #
########################################
from PySide2.QtWidgets import QWidget, QLabel, QVBoxLayout, QPushButton, QLineEdit, QHBoxLayout, QColorDialog, QCheckBox
from PySide2.QtGui import QDoubleValidator, QColor, QPainter, QPalette, QPixmap, QBrush
from PySide2.QtCore import Signal

class ColorPickerWidget(QWidget):
    colorChanged = Signal(QColor)
    def __init__(self, width = 190, height = 20):
        super().__init__()
        self.setFixedSize(width, height)
        self.color = QColor(128, 128, 128)

    def mousePressEvent(self, event):
        color = QColorDialog().getColor(self.color)
        if color.isValid:
            self.color = color
            self.colorChanged.emit(self.color)
            self.update()

    def paintEvent(self, event):
        painter = QPainter(self)
        painter.setBrush(QBrush(self.color))
        painter.drawRect(0,0, self.width(), self.height())    

        

class CreatePolarGeo(QWidget):
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

        polarLable = QLabel("Polar Value: ")
        ctrlSettingLayout.addWidget(polarLable)

        self.polarValue = QLineEdit()
        self.polarValue.setValidator(QDoubleValidator())
        self.polarValue.textChanged.connect(self.PolarValueSet)
        self.polarValue.setText("30") # probably broken
        ctrlSettingLayout.addWidget(self.polarValue)

        alphaLable = QLabel("Alpha Value: ")
        ctrlSettingLayout.addWidget(alphaLable)

        self.alphaValue = QLineEdit()
        self.alphaValue.setValidator(QDoubleValidator())
        self.alphaValue.textChanged.connect(self.AlphaValueSet)
        self.alphaValue.setText("30") # probably broken
        ctrlSettingLayout.addWidget(self.alphaValue)

        ctrlSizeLabel = QLabel("Geo Size: ")
        ctrlSettingLayout.addWidget(ctrlSizeLabel)

        self.ctrlSize = QLineEdit()
        self.ctrlSize.setValidator(QDoubleValidator())
        self.ctrlSize.textChanged.connect(self.CtrlSizeValueSet)
        self.ctrlSize.setText("10") # probably broken
        ctrlSettingLayout.addWidget(self.ctrlSize)

        self.masterLayout.addLayout(ctrlSettingLayout)

        self.colorPicker = ColorPickerWidget()
        self.colorPicker.colorChanged.connect(self.ColorPickerChanged)
        self.masterLayout.addWidget(self.colorPicker)

        createPolarGeo = QPushButton("Create Geo From PolarValue Cord")
        self.masterLayout.addWidget(createPolarGeo)
        createPolarGeo.clicked.connect(self.CreateGeoBtnClicked)


        self.adjustSize()
        self.geoCreator = GeoCreator()
    
    def CreateGeoBtnClicked(self):
        print("Rig Button Pressed")
        self.geoCreator.CreateGeoCube()
    
    def CtrlSizeValueSet(self, valStr:str):
        size = float(valStr)
        self.geoCreator.geoSize = size

    def RadialValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.radialValue = val

    def PolarValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.polarValue = val

    def AlphaValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.alphaValue = val
        
    def ColorPickerChanged(self, newColor):
        self.geoCreator.UpdateColors(newColor.redF(), newColor.greenF(), newColor.blueF())


threeJntChainWidget = CreatePolarGeo()
threeJntChainWidget.show()