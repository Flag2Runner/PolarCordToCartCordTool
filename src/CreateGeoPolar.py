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
        self.geoSize = 1
        self.radialValue = 10
        self.polarValue = 30
        self.alphaValue = 30
        self.radialRotationValue = 10
        self.polarRotationValue = 30
        self.alphaRotationValue = 30
        self.color = [128,128,128]
        self.model = ""
        self.isColorActive = True

    def UpdateColors(self, r,g,b):
        self.color[0] = r
        self.color[1] = g
        self.color[2] = b

    def CreateGeoCube(self):
        x = self.radialValue * m.cos(self.polarValue) * m.cos(self.alphaValue)
        y = self.radialValue * m.cos(self.polarValue) * m.sin(self.alphaValue)
        z = self.radialValue * m.sin(self.polarValue)

        xr = self.radialRotationValue * m.cos(self.polarRotationValue) * m.cos(self.alphaRotationValue)
        yr = self.radialRotationValue * m.cos(self.polarRotationValue) * m.sin(self.alphaRotationValue)
        zr = self.radialRotationValue * m.sin(self.polarRotationValue)
        
        selection = mc.ls(sl=True)
        if not selection:
            print("No Mesh Selected")
            self.model = "Cube"
            if mc.objExists(self.PolyName()):
                mc.move(x, y, z, f"{self.PolyName()}", absolute=True, ws = True)
                mc.xform(self.PolyName(), cp = True)
                mc.scale(self.geoSize, self.geoSize, self.geoSize, self.PolyName())
                mc.rotate(xr,yr,zr, self.PolyName())
                if self.isColorActive == True:
                    self.CreateMaterialForCube()
                return 0

            mc.polyCube(n = self.PolyName(), ax =[0,0,90],)
            mc.xform(self.PolyName(), cp = True)
            mc.scale(self.geoSize, self.geoSize, self.geoSize, self.PolyName())
            mc.rotate(xr,yr,zr, self.PolyName())
            mc.move(x, y, z, f"{self.PolyName()}", absolute=True, ws = True)
        
            if self.isColorActive == True:
                    self.CreateMaterialForCube()
            return 0
        
        selection = selection[0]
        shapes = mc.listRelatives(selection, s=True)
        for s in shapes:
            if mc.objectType(s) == "mesh":
                self.model = selection

        if mc.objExists(self.model):
            mc.move(x, y, z, f"{self.PolyName()}", absolute=True, ws = True)
            mc.xform(self.PolyName(), cp = True)
            mc.scale(self.geoSize, self.geoSize, self.geoSize, self.PolyName())
            mc.rotate(xr,yr,zr, self.PolyName())
            if self.isColorActive == True:
                    self.CreateMaterialForCube()
        return 0

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
        return self.model
    
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
    def __init__(self, width = 300, height = 20):
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

        self.setWindowTitle("PolarCord to CartCord Tool")
        self.setGeometry(0,0,100,200)
        self.masterLayout = QVBoxLayout()
        self.setLayout(self.masterLayout)


        ctrlSettingLayout = QHBoxLayout()
        rotationSettingLayout = QVBoxLayout()
        MoveSettingLayout = QVBoxLayout()
        radialCordinateLabel = QLabel("Radial Cordinate Value: ")
        MoveSettingLayout.addWidget(radialCordinateLabel)

        self.radialValue = QLineEdit()
        self.radialValue.setValidator(QDoubleValidator())
        self.radialValue.textChanged.connect(self.RadialValueSet)
        self.radialValue.setText("10") # probably broken
        MoveSettingLayout.addWidget(self.radialValue)

        polarLable = QLabel("Polar Value: ")
        MoveSettingLayout.addWidget(polarLable)

        self.polarValue = QLineEdit()
        self.polarValue.setValidator(QDoubleValidator())
        self.polarValue.textChanged.connect(self.PolarValueSet)
        self.polarValue.setText("30") # probably broken
        MoveSettingLayout.addWidget(self.polarValue)

        alphaLable = QLabel("Alpha Value: ")
        MoveSettingLayout.addWidget(alphaLable)

        self.alphaValue = QLineEdit()
        self.alphaValue.setValidator(QDoubleValidator())
        self.alphaValue.textChanged.connect(self.AlphaValueSet)
        self.alphaValue.setText("30") # probably broken
        MoveSettingLayout.addWidget(self.alphaValue)

        radialRotationCordinateLabel = QLabel("Rotation Radial Cordinate Value: ")
        rotationSettingLayout.addWidget(radialRotationCordinateLabel)

        self.radialRotationValue = QLineEdit()
        self.radialRotationValue.setValidator(QDoubleValidator())
        self.radialRotationValue.textChanged.connect(self.RadialRotationValueSet)
        self.radialRotationValue.setText("10") # probably broken
        rotationSettingLayout.addWidget(self.radialRotationValue)

        polarRotationLable = QLabel("Rotation Polar Value: ")
        rotationSettingLayout.addWidget(polarRotationLable)

        self.polarRoationValue = QLineEdit()
        self.polarRoationValue.setValidator(QDoubleValidator())
        self.polarRoationValue.textChanged.connect(self.PolarRotationValueSet)
        self.polarRoationValue.setText("30") # probably broken
        rotationSettingLayout.addWidget(self.polarRoationValue)

        alphaRotationLable = QLabel("Rotation Alpha Value: ")
        rotationSettingLayout.addWidget(alphaRotationLable)

        self.alphaRotationValue = QLineEdit()
        self.alphaRotationValue.setValidator(QDoubleValidator())
        self.alphaRotationValue.textChanged.connect(self.AlphaRotationValueSet)
        self.alphaRotationValue.setText("30") # probably broken
        rotationSettingLayout.addWidget(self.alphaRotationValue)

        ctrlSettingLayout.addLayout(MoveSettingLayout)
        ctrlSettingLayout.addLayout(rotationSettingLayout)
        self.masterLayout.addLayout(ctrlSettingLayout)

        ctrlSizeLabel = QLabel("Geo Size: ")
        self.masterLayout.addWidget(ctrlSizeLabel)

        self.ctrlSize = QLineEdit()
        self.ctrlSize.setValidator(QDoubleValidator())
        self.ctrlSize.textChanged.connect(self.CtrlSizeValueSet)
        self.ctrlSize.setText("1") # probably broken
        self.masterLayout.addWidget(self.ctrlSize)

        self.ColorLabel = QLabel("Color Options: \n")
        self.masterLayout.addWidget(self.ColorLabel)

        self.checkbox = QCheckBox("Enable Color Change", self)
        self.checkbox.setChecked(True)
        self.checkbox.stateChanged.connect(self.OnCheckBoxChanged)
        self.masterLayout.addWidget(self.checkbox)

        self.colorPicker = ColorPickerWidget()
        self.colorPicker.colorChanged.connect(self.ColorPickerChanged)
        self.masterLayout.addWidget(self.colorPicker)

        createPolarGeo = QPushButton("Update Polar Cords")
        self.masterLayout.addWidget(createPolarGeo)
        createPolarGeo.clicked.connect(self.CreateGeoBtnClicked)


        #self.adjustSize()
        self.geoCreator = GeoCreator()
    
    def CreateGeoBtnClicked(self):
        print("Create Button Pressed")
        self.geoCreator.CreateGeoCube()
    
    def CtrlSizeValueSet(self, valStr:str):
        size = float(valStr)
        self.geoCreator.geoSize = size

    def RadialValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.radialValue = val

    def RadialRotationValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.radialRotationValue = val

    def PolarValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.polarValue = val

    def PolarRotationValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.polarRotationValue = val

    def AlphaValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.alphaValue = val

    def AlphaRotationValueSet(self, valStr:str):
        val = float(valStr)
        self.geoCreator.alphaRotationValue = val
        
    def ColorPickerChanged(self, newColor):
        self.geoCreator.UpdateColors(newColor.redF(), newColor.greenF(), newColor.blueF())

    def OnCheckBoxChanged(self, state):
        if state == 2:  # Checked
            self.geoCreator.isColorActive = True
            
        else: # Unchecked
            self.geoCreator.isColorActive = False


threeJntChainWidget = CreatePolarGeo()
threeJntChainWidget.show()