#MEL: commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;
#https://www.youtube.com/watch?v=lBz8lEqHXYM&ab_channel=TDSuperheroes
import math
import copy
import PySide2 as p2
import re
import maya.OpenMayaUI as omui
import shiboken2
import maya.cmds as cmds
from PySide2 import QtGui, QtCore
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

sVersion = "0.02"
"""
Log:
2023.10.13 
Naming tool now accepts %N for all func. and smart increment

2023.12.08
Solved renaming prob, which caused u can't exe on obj sharing same name
"""

def mayaMainWindow():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer),p2.QtWidgets.QWidget)
    
class cls_Window(MayaQWidgetDockableMixin, p2.QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(cls_Window, self).__init__(parent)
        self.setWindowTitle("CA2023 Toolbox"+" "+sVersion); self.resize(300,500)
        TabGrp_TabGrp = p2.QtWidgets.QTabWidget()
        TabGrp_TabGrp.addTab(Tab_General(), "General" )
        TabGrp_TabGrp.addTab(Tab_Naming(), "Naming")
        TabGrp_TabGrp.addTab(Tab_Rigging(), "Rigging")

        BtTestFunction = p2.QtWidgets.QPushButton('Press to print selected nodes')
        
        QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        QVBL_mainLayout.addWidget(TabGrp_TabGrp)
        QVBL_mainLayout.addWidget(BtTestFunction)

        BtTestFunction.clicked.connect(self.FuncTest)
    def FuncTest(self):
        selected_nodes = cmds.ls(selection=True, long=False)
        print(selected_nodes)
        
class Tab_General(p2.QtWidgets.QWidget):
    def __init__(self, parent = None):
        p2.QtWidgets.QWidget.__init__(self, parent)
        #Public
        self.attrArray = [
        ".translateX",
        ".translateY",
        ".translateZ",
        ".rotateX",
        ".rotateY",
        ".rotateZ"
        ]

        #UI
        self.QWContainer = p2.QtWidgets.QWidget()
        self.QGLTab_General = p2.QtWidgets.QGridLayout(self.QWContainer)
        self.QWContainer.setFixedHeight(200)

        self.QPBGetChildNodes = p2.QtWidgets.QPushButton("GetChildNodes")
        self.QPBGetRelativeT = p2.QtWidgets.QPushButton("GetRelativeTransform")
        self.QPBSetRelativeT = p2.QtWidgets.QPushButton("SetRealtiveTransform")
        self.QPBSetToZero = p2.QtWidgets.QPushButton("BackToOrigin")
        self.QPBGetMatrix = p2.QtWidgets.QPushButton("GetMatrix")
        self.QPBSetMatrix = p2.QtWidgets.QPushButton("SetMatrix")
        self.QPBCreateGarbage = p2.QtWidgets.QPushButton("CreateGarbage")

        
        self.QLShow =p2.QtWidgets.QLabel("Display return value")
        self.QLShow.setAlignment(p2.QtCore.Qt.AlignTop)
        self.QLShow.setFrameShape(p2.QtWidgets.QFrame.Box)

        self.QGLTab_General.addWidget(self.QPBGetChildNodes,0,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBGetRelativeT,0,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBSetRelativeT,1,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBSetToZero,1,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBGetMatrix,2,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBSetMatrix,2,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBCreateGarbage,3,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QLShow,4,0,p2.QtCore.Qt.AlignTop)
     
        #FakeCode
        """CheckAllnodesName
        get type
        if type =
            rule 1
        if type .....

        get all Construction history.
        if construction history not belong to safeConstructionHistory[]
            write in file.
            """

        #show
        self.QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        self.QVBL_mainLayout.addWidget(self.QWContainer)
        
        self.QPBGetChildNodes.clicked.connect(self.FuncGetChildNodes)
        self.QPBGetRelativeT.clicked.connect(self.FuncGetRelativeT)
        self.QPBSetRelativeT.clicked.connect(self.FuncSetRelativeT)
        self.QPBSetToZero.clicked.connect(self.FuncSetToZero)
        self.QPBGetMatrix.clicked.connect(self.FuncGetMatrix)
        self.QPBSetMatrix.clicked.connect(self.FuncSetMatrix)
        self.QPBCreateGarbage.clicked.connect(self.FuncCreateGarbage)
        
        #Func
    def FuncGetChildNodes(self):
        selected_nodes = cmds.ls(selection = True)
        selected_nodes_children = cmds.listRelatives(selected_nodes, 
                                                        allDescendents=True, 
                                                        children=True, 
                                                        type="transform"
                                                        )
        for i in range(len(selected_nodes)):
            selected_nodes_children.insert(0,selected_nodes[len(selected_nodes)-1-i])
        slNodes_rmDup = selected_nodes_children
        slNodes_rmDup = list(dict.fromkeys(slNodes_rmDup))
        cmds.select(slNodes_rmDup)
        print(slNodes_rmDup)

    def FuncGetRelativeT(self):
        self.depot = []
        sl_obj = cmds.ls(selection = True)[0]
        if not sl_obj:
            print("Nothing selected or Not having a transform attr.")
            return
        
        for i in range(len(self.attrArray)):
            self.depot.append(cmds.getAttr(sl_obj + self.attrArray[i]))

        self.QLShow.setText(f"""
            P: {round(self.depot[0], 3)}  {round(self.depot[1], 3)}  {round(self.depot[2], 3)} \r\n
            R: {round(self.depot[3], 3)}  {round(self.depot[4], 3)}  {round(self.depot[5], 3)} \r\n
            """)
    
    def FuncSetRelativeT(self):
        sl_objs = cmds.ls(selection =True)

        if not sl_objs:
            print("Nothing selected or Not having a transform attr.")
            return
        for j in range(len(sl_objs)):
            for i in range(len(self.attrArray)):
                BLattrLocked = cmds.getAttr(sl_objs[j] + self.attrArray[i], lock=True)
                if BLattrLocked:
                    continue
                else:
                    cmds.setAttr(sl_objs[j] + self.attrArray[i], self.depot[i])

    def FuncSetToZero(self):
        sl_objs = cmds.ls(selection =True)
        if not sl_objs:
            print("Nothing selected or Not having a transform attr.")
            return
        #for j in range(len(sl_objs)):
        #    for i in range(len(self.attrArray)):
        cmds.move(0,0,0, rotatePivotRelative=True)

    def FuncGetMatrix(self):
        sl_obj = cmds.ls(selection=True)[0]
        M = cmds.xform(sl_obj, query=True, matrix=True, worldSpace=True)
        print(M)

    def FuncSetMatrix(self):
        sl_obj = cmds.ls(selection=True)[0]
        B = cmds.getAttr(sl_obj+"."+"worldMatrix")
        B = cmds.xform(sl_obj, q=True, m=True, ws=True)
        print(B)

    def FuncCreateGarbage(self):
        sl_objs = cmds.ls(selection=True)   
        # Get the world transform of the object
        world_transform_pool=[]
        for i in range(len(sl_objs)):
            world_transform_pool.append(cmds.xform(sl_objs[i], query=True, worldSpace=True, matrix=True))
        # Get the original parent of the object
        original_parent_pool=[]
        for i in range(len(sl_objs)):
            original_parent_pool.append(cmds.listRelatives(sl_objs[i], parent=True))
        # Create a null object with the same world transform
        for i in range(len(sl_objs)):
            null_object = cmds.group(empty=True, name=sl_objs[i]+"Garbage")
            cmds.xform(null_object, worldSpace=True, matrix = world_transform_pool[i])
            # Parent the original object under the null object
            cmds.parent(sl_objs[i], null_object)
        # Reparent the original object to its original parent
            if original_parent_pool[i]:
                cmds.parent(null_object, original_parent_pool[i])

class Tab_Naming(p2.QtWidgets.QWidget):
    def __init__(self, parent=None):
        p2.QtWidgets.QWidget.__init__(self,parent)
        #UI
        self.QWContainer = p2.QtWidgets.QWidget()
        self.QGLTab_Naming = p2.QtWidgets.QGridLayout(self.QWContainer)
        self.QWContainer.setFixedHeight(200)

        self.QLPrefix = p2.QtWidgets.QLabel("Prefix");self.QLSuffix = p2.QtWidgets.QLabel("Suffix")
        self.QLReplace = p2.QtWidgets.QLabel("Replace");self.QLWith = p2.QtWidgets.QLabel("With")
        self.QLWhole = p2.QtWidgets.QLabel("Whole")

        self.QLEPrefix = p2.QtWidgets.QLineEdit("")
        self.QLESuffix = p2.QtWidgets.QLineEdit("")
        self.QLEReplace = p2.QtWidgets.QLineEdit("")
        self.QLEWith = p2.QtWidgets.QLineEdit("")
        self.QLEWhole = p2.QtWidgets.QLineEdit("")
        #self.QLEWhole.setMaximumWidth(150)
        
        self.QPBPrefixExe = p2.QtWidgets.QPushButton("Execute", self)
        self.QPBSuffixExe = p2.QtWidgets.QPushButton("Execute", self)
        self.QPBReplaceExe = p2.QtWidgets.QPushButton("Execute", self)
        self.QPBWholeExe = p2.QtWidgets.QPushButton("Execute", self)
        
        self.QGLTab_Naming.addWidget(self.QLPrefix,0,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLEPrefix,0,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBPrefixExe,0,2,p2.QtCore.Qt.AlignTop)
        
        self.QGLTab_Naming.addWidget(self.QLSuffix,1,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLESuffix,1,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBSuffixExe,1,2,p2.QtCore.Qt.AlignTop)

        self.QGLTab_Naming.addWidget(self.QLReplace,2,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLEReplace,2,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLWith,3,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLEWith,3,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBReplaceExe,3,2,p2.QtCore.Qt.AlignTop)

        self.QGLTab_Naming.addWidget(self.QLWhole,4,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLEWhole,4,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBWholeExe,4,2,p2.QtCore.Qt.AlignTop)
        
        self.QLInstruction = p2.QtWidgets.QLabel("""
        How to use: \r\n
        1. Select all nodes you want. \r\n
        2. Input the string. \r\n
        3. Hit Execute button. 
                        """)
        self.QLInstruction.setAlignment(p2.QtCore.Qt.AlignTop)
        self.QLInstruction.setFrameShape(p2.QtWidgets.QFrame.Box)
        self.QLPreview = p2.QtWidgets.QLabel("Here display what will be")
        
        #button
        self.QPBPrefixExe.clicked.connect(self.FuncExePrefix)
        self.QPBSuffixExe.clicked.connect(self.FuncExeSuffix)
        self.QPBReplaceExe.clicked.connect(self.FuncExeReplace)
        self.QPBWholeExe.clicked.connect(self.FuncExeWhole)
        
        #Show
        self.QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        self.QVBL_mainLayout.addWidget(self.QWContainer)
        self.QVBL_mainLayout.addWidget(self.QLInstruction)

    def AuxFuncMakeRelativeName(self, selected_objs): #input: origin selected objs list
        RelativeNameList = []
        for i in range(len(selected_objs)):
            RelativeName = re.sub(r"^.*\|", "", selected_objs[i])
            RelativeNameList.append(RelativeName)
        return RelativeNameList

    def FuncExePrefix(self):
        sl_objs = cmds.ls(selection=True) #origin namepath list
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        print(Re_sl_objs)

        IncrementKey = "$N"
        Zero = "0"
        MaxZero = math.floor(math.log10(len(sl_objs)))+1
        if IncrementKey in self.QLEPrefix.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero -math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                    Zero_Apply = Zero_Apply + Zero
                    
                recIncrement = Zero_Apply + str(Increment)
                recQLEPrefix = self.QLEPrefix.text().replace(IncrementKey, recIncrement)
                print(recQLEPrefix)
                NewName = recQLEPrefix + Re_sl_objs[i]
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
        else:
            for i in range(len(sl_objs)):
                Increment = i+1
                NewName = self.QLEPrefix.text() + Re_sl_objs[i]
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)

    def FuncExeSuffix(self):
        sl_objs = cmds.ls(selection=True)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        print(Re_sl_objs)
        IncrementKey = "$N"
        Zero = "0"
        MaxZero = math.floor(math.log10(len(sl_objs)))+1
        if IncrementKey in self.QLESuffix.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero -math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                    Zero_Apply = Zero_Apply + Zero
                    
                recIncrement = Zero_Apply + str(Increment)
                recQLESuffix = self.QLESuffix.text().replace(IncrementKey, recIncrement)
                NewName = Re_sl_objs[i] + recQLESuffix
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
            else:
                print("No nodes selected")
        else:
            for i in range(len(sl_objs)):
                Increment = i+1
                NewName = Re_sl_objs[i] + self.QLESuffix.text()
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)

            
    def FuncExeReplace(self):
        sl_objs = cmds.ls(selection=True)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        print(Re_sl_objs)
        IncrementKey = "$N"
        Zero = "0"
        MaxZero = math.floor(math.log10(len(sl_objs)))+1
        if IncrementKey in self.QLEWith.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero -math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                    Zero_Apply = Zero_Apply + Zero
                    
                recIncrement = Zero_Apply + str(Increment)
                recQLEWith = self.QLEWith.text().replace(IncrementKey, recIncrement)
                NewName = Re_sl_objs[i].replace(self.QLEReplace.text(), recQLEWith, 1)
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
            else:
                print("No nodes selected")
        else:
            for i in range(len(sl_objs)):
                Increment =i+1
                NewName = Re_sl_objs[i].replace(self.QLEReplace.text(), self.QLEWith.text(), 1)
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)

    def FuncExeWhole(self):
        #Must add Increment
        sl_objs = cmds.ls(selection=True)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        IncrementKey = "$N"
        Zero = "0"
        # if  sl_objs<=99, maxZero = 2 = math.ceiling.math.log10(len(sl_objs))
        #     add 00 for i+1 C 1~9: maxZero - 00.digits = log10(i+1)
        #     add 0 for i+1 C 10~99:
        MaxZero =  math.floor(math.log10(len(sl_objs)))+1 #if 1, add one 0. if 2, add two.
        
        print("vasdadf"+Zero)
        print(Re_sl_objs)
        if IncrementKey in self.QLEWhole.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero - math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                        Zero_Apply = Zero_Apply + Zero
                recIncrement = Zero_Apply + str(Increment)
                recQLEWhole = self.QLEWhole.text().replace(IncrementKey, recIncrement)
                print(recQLEWhole)
                NewName = recQLEWhole
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
            else:
                print("No nodes selected")
        else:
            for i in range(len(sl_objs)):
                Increment = i+1
                NewName = self.QLEWhole.text()
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
    
    def SupFuncIncrement(self, str): #Pending
        pass

class ClickableLabel(p2.QtWidgets.QLabel):
    clicked = QtCore.Signal()
    def mousePressEvent(self, event):
        self.clicked.emit()
class Tab_Rigging(p2.QtWidgets.QWidget):
    def __init__(self, parent=None):
        p2.QtWidgets.QWidget.__init__(self,parent)
        self.QWContainer = p2.QtWidgets.QWidget()
        #self.QWContainer.setFixedHeight(200)
        self.QGLTab_Rigging = p2.QtWidgets.QGridLayout(self.QWContainer)
        #module dev
        ExtraLine1, ExtraLine2 = 0,0
        TargColumnNum = 4

        Dic_CtrlerBtnInit = {#use number to indicate they belong to different groups .
            "CtrlerCube" :      ["GroupCtrler",0,0],
            "CtrlerSphere" :    ["GroupCtrler",0,0],
            "CtrlPrism" :       ["GroupCtrler",0,0],
            "CtrlRing" :        ["GroupCtrler",0,0],
            "CtrlRotPike" :     ["GroupCtrler",0,0],
            "CtrlerRot1Dir" :   ["GroupCtrler",0,0],
            "CtrlerTran1Dir" :  ["CtrlerTran1Dir",0,0],
            "CtrlerGear" :  ["CtrlerGear",0,0],
            "CtrlerTransCube" :  ["CtrlerTransCube",0,0]

            }
        Dic_ChangeColorBtnInit = {
            "QPBColorReturn" :  ["GroupChangeColor",0,0],
            "QPBColorYellow" :  ["GroupChangeColor",0,0],
            "QPBColorRed" :     ["GroupChangeColor",0,0],
            "QPBColorBlue" :    ["GroupChangeColor",0,0]}
        Dic_JointSizeBtnInit = {
            "QLJointSize" :     ["Joint Size",0,0],
            "QLEJointSize" :    ["Joint Size",0,0],
            "QPBJointSizeExe" : ["Joint Size",0,0]}
        
        Ls_BtnPos=[]
        Ls_CtrlerBtnPos = []
        Ls_ChangeColorBtnPos = []
        Ls_JointSizeBtnPos = []
        for i in range(len(Dic_CtrlerBtnInit)):
            V2_BtnPos = [i//TargColumnNum+ExtraLine1, i%TargColumnNum]
            Ls_CtrlerBtnPos.append(V2_BtnPos) 
        for i in range(len(Dic_ChangeColorBtnInit)):
            V2_BtnPos = [i//TargColumnNum+ExtraLine1+3, i%TargColumnNum]
            Ls_ChangeColorBtnPos.append(V2_BtnPos) 
        for i in range(len(Dic_JointSizeBtnInit)):
            V2_BtnPos = [i//TargColumnNum+ExtraLine2+4, i%TargColumnNum]
            Ls_JointSizeBtnPos.append(V2_BtnPos) 

        #print(Ls_BtnPosRun)
        #func 1 - 
        #self.tempIcon_path = os.path.join(os.path.dirname("C:/Users/JoleneLinxy/OneDrive/OrganizeFilesStructure/08_Environment/Config/Maya/script/CAToolbox/images"), "tempIcon.jpg")
        self.easyToSee = "C:/Users/JoleneLinxy/OneDrive/OrganizeFilesStructure/08_Environment/Config/Maya/script/CAToolbox/"

        self.QLPathCtrlerCube = self.easyToSee + "images/CtrlerCube.jpg"
        self.QLCtrlerCube = ClickableLabel("")
        self.QPxmapCtrlerCube = p2.QtGui.QPixmap(self.QLPathCtrlerCube)
        self.QLCtrlerCube.setPixmap(self.QPxmapCtrlerCube)
        self.QLCtrlerCube.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerCube.clicked.connect(self.FuncCreateCtrlerCube)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerCube,Ls_CtrlerBtnPos[0][0],Ls_CtrlerBtnPos[0][1],p2.QtCore.Qt.AlignTop)

        self.QLPathCtrlerSphere = self.easyToSee + "images/CtrlerSphere.jpg"
        self.QLCtrlerSphere = ClickableLabel("")
        self.QPxmapCtrlerSphere = p2.QtGui.QPixmap(self.QLPathCtrlerSphere)
        self.QLCtrlerSphere.setPixmap(self.QPxmapCtrlerSphere)
        self.QLCtrlerSphere.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerSphere.clicked.connect(self.FuncCreateCtrlerSphere)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerSphere,Ls_CtrlerBtnPos[1][0],Ls_CtrlerBtnPos[1][1],p2.QtCore.Qt.AlignTop)

        self.QLPathCtrlerPrism = self.easyToSee + "images/CtrlerPrism.jpg"
        self.QLCtrlerPrism = ClickableLabel("")
        self.QPxmapCtrlerPrism = p2.QtGui.QPixmap(self.QLPathCtrlerPrism)
        self.QLCtrlerPrism.setPixmap(self.QPxmapCtrlerPrism)
        self.QLCtrlerPrism.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerPrism.clicked.connect(self.FuncCreateCtrlerPrism)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerPrism,Ls_CtrlerBtnPos[2][0],Ls_CtrlerBtnPos[2][1],p2.QtCore.Qt.AlignTop)

        self.QLPathCtrlerRing = self.easyToSee + "images/CtrlerRing.jpg"
        self.QLCtrlerRing = ClickableLabel("")
        self.QPxmapCtrlerRing = p2.QtGui.QPixmap(self.QLPathCtrlerRing)
        self.QLCtrlerRing.setPixmap(self.QPxmapCtrlerRing)
        self.QLCtrlerRing.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerRing.clicked.connect(self.FuncCreateCtrlerRing)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerRing,Ls_CtrlerBtnPos[3][0],Ls_CtrlerBtnPos[3][1],p2.QtCore.Qt.AlignTop)
        
        self.QLPathCtrlerRotPike = self.easyToSee + "images/CtrlerRotPike.jpg"
        self.QLCtrlerRotPike = ClickableLabel("")
        self.QPxmapCtrlerRotPike = p2.QtGui.QPixmap(self.QLPathCtrlerRotPike)
        self.QLCtrlerRotPike.setPixmap(self.QPxmapCtrlerRotPike)
        self.QLCtrlerRotPike.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerRotPike.clicked.connect(self.FuncCreateCtrlerRotPike)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerRotPike,Ls_CtrlerBtnPos[4][0],Ls_CtrlerBtnPos[4][1],p2.QtCore.Qt.AlignTop)
        
        self.QLPathCtrlerRot1Dir = self.easyToSee + "images/CtrlerRot1Dir.jpg"
        self.QLCtrlerRot1Dir = ClickableLabel("")
        self.QPxmapCtrlerRot1Dir = p2.QtGui.QPixmap(self.QLPathCtrlerRot1Dir)
        self.QLCtrlerRot1Dir.setPixmap(self.QPxmapCtrlerRot1Dir)
        self.QLCtrlerRot1Dir.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerRot1Dir.clicked.connect(self.FuncCreateCtrlerRot1Dir)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerRot1Dir,Ls_CtrlerBtnPos[5][0],Ls_CtrlerBtnPos[5][1],p2.QtCore.Qt.AlignTop)
        
        self.QLPathCtrlerTran1Dir = self.easyToSee + "images/CtrlerTran1Dir.jpg"
        self.QLCtrlerTran1Dir = ClickableLabel("")
        self.QPxmapCtrlerTran1Dir = p2.QtGui.QPixmap(self.QLPathCtrlerTran1Dir)
        self.QLCtrlerTran1Dir.setPixmap(self.QPxmapCtrlerTran1Dir)
        self.QLCtrlerTran1Dir.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerTran1Dir.clicked.connect(self.FuncCreateCtrlerTran1Dir)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerTran1Dir,Ls_CtrlerBtnPos[6][0],Ls_CtrlerBtnPos[6][1],p2.QtCore.Qt.AlignTop)
        
        self.QLPathCtrlerGear = self.easyToSee + "images/CtrlerGear.jpg"
        self.QLCtrlerGear = ClickableLabel("")
        self.QPxmapCtrlerGear = p2.QtGui.QPixmap(self.QLPathCtrlerGear)
        self.QLCtrlerGear.setPixmap(self.QPxmapCtrlerGear)
        self.QLCtrlerGear.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerGear.clicked.connect(self.FuncCreateCtrlerGear)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerGear,Ls_CtrlerBtnPos[7][0],Ls_CtrlerBtnPos[7][1],p2.QtCore.Qt.AlignTop)
        
        self.QLPathCtrlerTransCube = self.easyToSee + "images/CtrlerTransCube.jpg"
        self.QLCtrlerTransCube = ClickableLabel("")
        self.QPxmapCtrlerTransCube = p2.QtGui.QPixmap(self.QLPathCtrlerTransCube)
        self.QLCtrlerTransCube.setPixmap(self.QPxmapCtrlerTransCube)
        self.QLCtrlerTransCube.setAlignment(QtCore.Qt.AlignCenter)
        self.QLCtrlerTransCube.clicked.connect(self.FuncCreateCtrlerTransCube)
        self.QGLTab_Rigging.addWidget(self.QLCtrlerTransCube,Ls_CtrlerBtnPos[8][0],Ls_CtrlerBtnPos[8][1],p2.QtCore.Qt.AlignTop)

        #func 2 - one click changes thr sl_objs drawoverrides
        
        self.QPBColorReturn = p2.QtWidgets.QPushButton("ColorReturn", self)
        self.QPBColorYellow = p2.QtWidgets.QPushButton("ColorYellow", self)
        self.QPBColorRed = p2.QtWidgets.QPushButton("ColorRed", self)
        self.QPBColorBlue = p2.QtWidgets.QPushButton("ColorBlue", self)
        
        self.QGLTab_Rigging.addWidget(self.QPBColorReturn,Ls_ChangeColorBtnPos[0][0],Ls_ChangeColorBtnPos[0][1],p2.QtCore.Qt.AlignTop)
        self.QGLTab_Rigging.addWidget(self.QPBColorYellow,Ls_ChangeColorBtnPos[1][0],Ls_ChangeColorBtnPos[1][1],p2.QtCore.Qt.AlignTop)
        self.QGLTab_Rigging.addWidget(self.QPBColorRed,Ls_ChangeColorBtnPos[2][0],Ls_ChangeColorBtnPos[2][1],p2.QtCore.Qt.AlignTop)
        self.QGLTab_Rigging.addWidget(self.QPBColorBlue,Ls_ChangeColorBtnPos[3][0],Ls_ChangeColorBtnPos[3][1],p2.QtCore.Qt.AlignTop)
        
        self.QPBColorReturn.clicked.connect(self.FuncColorReturn)
        self.QPBColorYellow.clicked.connect(self.FuncColorYellow)
        self.QPBColorRed.clicked.connect(self.FuncColorRed)
        self.QPBColorBlue.clicked.connect(self.FuncColorBlue)

        #func 3 - change sl_jnts size.
        self.QLJointSize = p2.QtWidgets.QLabel("JointSize")
        self.QLEJointSize = p2.QtWidgets.QLineEdit("")
        self.QPBJointSizeExe = p2.QtWidgets.QPushButton("Execute", self)

        self.QGLTab_Rigging.addWidget(self.QLJointSize,Ls_JointSizeBtnPos[0][0],Ls_JointSizeBtnPos[0][1],p2.QtCore.Qt.AlignTop)
        self.QGLTab_Rigging.addWidget(self.QLEJointSize,Ls_JointSizeBtnPos[1][0],Ls_JointSizeBtnPos[1][1],p2.QtCore.Qt.AlignTop)
        self.QGLTab_Rigging.addWidget(self.QPBJointSizeExe,Ls_JointSizeBtnPos[2][0],Ls_JointSizeBtnPos[2][1],p2.QtCore.Qt.AlignTop)

        self.QPBJointSizeExe.clicked.connect(self.FuncExeJointSize)
        #UI
        self.QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        self.QVBL_mainLayout.addWidget(self.QWContainer)

    def FuncCreateCtrlerCube(self):
        #BaseSize = 5
        CubePathing =  [
            (-1,1,-1),
            (-1,1,1),
            (1,1,1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (-1,-1,1),
            (-1,1,1),
            (-1,-1,1),
            (1,-1,1),
            (1,1,1),
            (1,-1,1),
            (1,-1,-1),
            (1,1,-1),
            (1,-1,-1),
            (-1,-1,-1),
        ]
        cmds.curve(d=1, p=CubePathing, name = "CtrlerCube")

    def FuncCreateCtrlerSphere(self):
        SpherePathing = []; VertexPos = (0,0,0); VertexAmount = 36 # X times 4
        for i in range(VertexAmount):
            pass
            #BaseSize = 5
            recAngle = math.radians((i/VertexAmount)*360)
            VertexPos = (math.cos(recAngle), math.sin(recAngle),0)
            SpherePathing.append(VertexPos)
        for i in range(VertexAmount):
            recAngle = math.radians((i/VertexAmount)*360)
            VertexPos = (math.cos(recAngle), 0, math.sin(recAngle))
            SpherePathing.append(VertexPos)
        SpherePathing.append(SpherePathing[0])
        temp = copy.deepcopy(SpherePathing)
        intTemp = int(VertexAmount/4)
        for i in range(intTemp):
            SpherePathing.append(temp[-i-1])
        temp = []
        for i in range(VertexAmount):
            recAngle = math.radians((i/VertexAmount)*360)
            VertexPos = (0, math.sin(recAngle), -math.cos(recAngle))
            SpherePathing.append(VertexPos)
        SpherePathing.append(SpherePathing[-36])
        cmds.curve(d=1, p=SpherePathing, name = "CtrlerSphere")

    def FuncCreateCtrlerPrism(self):
        PrismPathing = [
            (1,0,1),
            (1,0,-1),
            (-1,0,-1),
            (-1,0,1),
            (0,math.sqrt(2),0),
            (1,0,-1),
            (0,-math.sqrt(2),0),
            (-1,0,1),
            (1,0,1),
            (0,math.sqrt(2),0),
            (-1,0,-1),
            (0,-math.sqrt(2),0),
            (1,0,1)
        ]
        cmds.curve(d=1, p=PrismPathing, name = "CtrlerPrism")

    def FuncCreateCtrlerRing(self):
        VertexAmount = 36
        VertexPos = (0,0,0); RingPathing = []
        for i in range(VertexAmount):
            recAngle = math.radians((i/VertexAmount)*360)
            VertexPos = (math.cos(recAngle), 0, math.sin(recAngle))
            RingPathing.append(VertexPos)
        RingPathing.append(RingPathing[0])
        cmds.curve(d=1, p=RingPathing, name = "CtrlerRing")

    def FuncCreateCtrlerRotPike(self):
        RotPikePathing = [
            (-0.5, 5.0, 0.5),
            (-0.5, 5.0, -0.5),
            (0.0, 0.0, 0.0),
            (-0.5, 5.0, 0.5),
            (0.5, 5.0, 0.5),
            (0.0, 0.0, 0.0),
            (0.5, 5.0, -0.5),
            (0.5, 5.0, 0.5),
            (0.5, 5.0, -0.5),
            (-0.5, 5.0, -0.5)
        ]

        RotPikePathing.append(RotPikePathing[0])
        cmds.curve(d=1, p=RotPikePathing, name = "CtrlerRotPike")

    def FuncCreateCtrlerRot1Dir(self):
        CtrlerRot1DirPathing = [
        (1.7677669529663689, 1.7677669529663689, 0.0),
        (1.677819114643154, 1.8539955445563654, 0.0),
        (1.5840082542288714, 1.9359981253360319, 0.0),
        (1.4861617958451059, 2.013122047385339, 0.0),
        (1.3842863692034264, 2.084844271874945, 0.0),
        (1.2786104406445689, 2.1508406774443203, 0.0),
        (1.1695405135095442, 2.2110554697423175, 0.0),
        (1.0575762632552563, 2.2657097759244675, 0.0),
        (0.943220946689385, 2.3152481886432623, 0.0),
        (0.8269042313276265, 2.3598954940151318, 0.0),
        (0.7086327083628066, 2.399079050124751, 0.0),
        (0.5885083010279508, 2.4321459691146887, 0.0),
        (0.46676920233285163, 2.4586385092952185, 0.0),
        (0.34375522647702006, 2.478382523021656, 0.0),
        (0.21985357361771146, 2.491519728123323, 0.0),
        (0.09546090155836363, 2.4984725723904257, 0.0),
        (-0.02915717349748625, 2.4998610976741675, 0.0),
        (-0.15369001860166454, 2.4959536891929024, 0.0),
        (-0.2778919467915799, 2.486176296697979, 0.0),
        (-0.4014292741805249, 2.469985609366813, 0.0),
        (-0.5238951445212825, 2.4470831232464354, 0.0),
        (-0.6449135015990431, 2.4174756044732533, 0.0),
        (-0.7641932889785071, 2.3814762534398923, 0.0),
        (-0.8815613722631757, 2.339645390645023, 0.0),
        (-0.996979306265769, 2.2926782106174124, 0.0),
        (-1.1102728452877122, 2.2408144141677684, 0.0),
        (-1.220951306344227, 2.183600855904615, 0.0),
        (-1.3284913039227937, 2.1206935827081184, 0.0),
        (-1.4324294392514265, 2.051995680923809, 0.0),
        (-1.5324376742712993, 1.9776906622030763, 0.0),
        (-1.6283820658843249, 1.898212490926191, 0.0),
        (-1.720350835300362, 1.8141517947999204, 0.0),
        (-1.8088839489020496, 1.8088839489020496, 0.0),
        (-1.896996312052369, 1.896996312052369, 0.0),
        (-1.985191207230601, 1.985191207230601, 0.0),
        (-2.0732976010424435, 2.0732976010424435, 0.0),
        (-2.1614342042132795, 2.1614342042132795, 0.0),
        (-2.249579183577703, 2.249579183577703, 0.0),
        (-2.3377050983581693, 2.3377050983581693, 0.0),
        (-2.4258232296678095, 2.4258232296678095, 0.0),
        (-2.5000000000000004, 2.480577564815938, 0.0),
        (-2.5, 2.35604052751443, 0.0),
        (-2.5, 2.2314953322516167, 0.0),
        (-2.5, 2.1067378112572763, 0.0),
        (-2.5, 1.9821393022476368, 0.0),
        (-2.5, 1.8573910690885658, 0.0),
        (-2.5, 1.732768580255935, 0.0),
        (-2.5, 1.6081567162989026, 0.0),
        (-2.5, 1.4835167828775015, 0.0),
        (-2.5, 1.3588629632783529, 0.0),
        (-2.5, 1.2342018274393596, 0.0),
        (-2.5, 1.1095615610953362, 0.0),
        (-2.5, 0.9850672297988889, 0.0),
        (-2.5, 0.8602116645027584, 0.0),
        (-2.5, 0.7355877007651206, 0.0),
        (-2.5, 0.6110529019437854, 0.0),
        (-2.4871558400595792, 0.5, 0.0),
        (-2.3620889694831475, 0.5, 0.0),
        (-2.237742307060767, 0.5, 0.0),
        (-2.112925490486211, 0.5, 0.0),
        (-1.98843473265591, 0.5, 0.0),
        (-1.8637182176133609, 0.5, 0.0),
        (-1.7390241072819972, 0.5, 0.0),
        (-1.6144216448002071, 0.5, 0.0),
        (-1.4897958503312874, 0.5, 0.0),
        (-1.3651494612431274, 0.5, 0.0),
        (-1.2404859653370766, 0.5, 0.0),
        (-1.115823262414007, 0.5, 0.0),
        (-0.9912638174188817, 0.5, 0.0),
        (-0.8665178023667004, 0.5, 0.0),
        (-0.7419865058598314, 0.5, 0.0),
        (-0.6171602618991272, 0.5, 0.0),
        (-0.5048775466149777, 0.5048775466149781, 0.0),
        (-0.5930818740469747, 0.5930818740469749, 0.0),
        (-0.6812132088953303, 0.6812132088953304, 0.0),
        (-0.7693222753789901, 0.7693222753789903, 0.0),
        (-0.8574648235025216, 0.8574648235025217, 0.0),
        (-0.9456167875234252, 0.9456167875234253, 0.0),
        (-1.0337755623069296, 1.0337755623069298, 0.0),
        (-0.9980727746651711, 1.120245021426811, 0.0),
        (-0.9022905829929514, 1.199892546755962, 0.0),
        (-0.7998232951529464, 1.2707146045128752, 0.0),
        (-0.6913560358592817, 1.331960506066958, 0.0),
        (-0.5782088036379023, 1.3840803728737712, 0.0),
        (-0.4615697217312693, 1.4278751548302302, 0.0),
        (-0.3417756152549756, 1.4620303185850774, 0.0),
        (-0.21939373563283876, 1.485221858755463, 0.0),
        (-0.09542091844683132, 1.4973953021301047, 0.0),
        (0.029149600274320044, 1.4997668613413446, 0.0),
        (0.15353792201206717, 1.4930194810472646, 0.0),
        (0.27690202063386893, 1.475775841309719, 0.0),
        (0.3981787676378521, 1.4473629687935075, 0.0),
        (0.5165296538340479, 1.4084769707932492, 0.0),
        (0.631619249827561, 1.3607664702099034, 0.0),
        (0.7427628465466206, 1.3045036796338692, 0.0),
        (0.8485613375164399, 1.2387610478560696, 0.0),
        (0.9479311478546134, 1.1636511375794694, 0.0),
        (1.040606843117443, 1.080406380795172, 0.0),
        (0.9924832187318223, 0.9924832187318223, 0.0),
        (0.9043819410003046, 0.9043819410003046, 0.0),
        (0.8162304265594202, 0.8162304265594202, 0.0),
        (0.728102075019263, 0.728102075019263, 0.0),
        (0.6399520822025768, 0.6399520822025768, 0.0),
        (0.5517912829201661, 0.5517912829201661, 0.0),
        (0.5508639092751123, 0.5, 0.0),
        (0.6756637844151498, 0.5, 0.0),
        (0.8002289680177653, 0.5, 0.0),
        (0.9249271853901875, 0.5, 0.0),
        (1.0495214160085555, 0.5, 0.0),
        (1.1741312106494608, 0.5, 0.0),
        (1.2987931675902766, 0.5, 0.0),
        (1.4234512142002123, 0.5, 0.0),
        (1.5480955156718945, 0.5, 0.0),
        (1.672718510379384, 0.5, 0.0),
        (1.7973132524309534, 0.5, 0.0),
        (1.922037871414619, 0.5, 0.0),
        (2.046739881045908, 0.5, 0.0),
        (2.171270452879781, 0.5, 0.0),
        (2.295866817539284, 0.5, 0.0),
        (2.4203517588778376, 0.5, 0.0),
        (2.5, 0.5444634350279588, 0.0),
        (2.5, 0.6694888486493674, 0.0),
        (2.5, 0.7940685622611884, 0.0),
        (2.5, 0.9185752834885437, 0.0),
        (2.5, 1.0432974209228139, 0.0),
        (2.5, 1.167862985621098, 0.0),
        (2.5, 1.2925109390549994, 0.0),
        (2.5, 1.4171692942095988, 0.0),
        (2.5, 1.5418215958956005, 0.0),
        (2.5, 1.6664597937837402, 0.0),
        (2.5, 1.7910604887488155, 0.0),
        (2.5, 1.915708663540961, 0.0),
        (2.5, 2.0404672307266774, 0.0),
        (2.5, 2.164852609127672, 0.0),
        (2.5, 2.2895406374296554, 0.0),
        (2.5, 2.4143875259793095, 0.0),
        (2.4727655948696112, 2.4727655948696112, 0.0),
        (2.384652034033294, 2.384652034033294, 0.0),
        (2.2964938900139407, 2.2964938900139407, 0.0),
        (2.208351359304868, 2.208351359304868, 0.0),
        (2.120206386869219, 2.120206386869219, 0.0),
        (2.0320655748390726, 2.0320655748390726, 0.0),
        (1.9439765990224678, 1.9439765990224678, 0.0),
        (1.855803432803397, 1.855803432803397, 0.0),
        (1.855803432803397, 1.855803432803397, 0.0)
        ]

        CtrlerRot1DirPathing.append(CtrlerRot1DirPathing[0])
        cmds.curve(d=1, p=CtrlerRot1DirPathing, name = "CtrlerRot1Dir")

    def FuncCreateCtrlerTran1Dir(self):
        CtrlerTran1DirPathing = [
        (-1.7499999999999998, 0.5, 0.0),
        (1.7500000000000002, 0.5, 0.0),
        (1.7500000000000002, 1.25, 0.0),
        (3.0, -2.7755575615628914e-17, 0.0),
        (1.7500000000000002, -1.25, 0.0),
        (1.7500000000000002, -0.5, 0.0),
        (-1.7499999999999998, -0.5, 0.0),
        (-1.7499999999999998, -1.25, 0.0),
        (-3.0, -2.7755575615628914e-17, 0.0),
        (-1.7499999999999998, 1.25, 0.0),
        (-1.7499999999999998, 1.25, 0.0)
        ]
        CtrlerTran1DirPathing.append(CtrlerTran1DirPathing[0])
        cmds.curve(d=1, p=CtrlerTran1DirPathing, name = "CtrlerTran1Dir")
    
    def FuncCreateCtrlerGear(self):
        CtrlerGearPathing = [
        (-0.8462747849789007, 1.4355304359676908, 0.0),
        (-1.4731391274719736, 2.0623947784607637, 0.0),
        (-2.0623947784607637, 1.4731391274719743, 0.0),
        (-1.4355304359676901, 0.8462747849789014, 0.0),
        (-1.4957469684510285, 0.7323984146262833, 0.0),
        (-1.552676377691546, 0.595637862454051, 0.0),
        (-1.582361684753277, 0.507128735104546, 0.0),
        (-1.607888940964566, 0.4166666666666668, 0.0),
        (-2.4999999999999996, 0.4166666666666671, 0.0),
        (-2.5, -0.41666666666666635, 0.0),
        (-1.607888940964566, -0.41666666666666624, 0.0),
        (-1.5558409745749813, -0.5868838745851087, 0.0),
        (-1.4996648215027426, -0.7240457360952969, 0.0),
        (-1.4711841257953149, -0.7819200277487285, 0.0),
        (-1.4355304359676895, -0.8462747849789021, 0.0),
        (-2.062394778460763, -1.4731391274719758, 0.0),
        (-1.4731391274719727, -2.0623947784607646, 0.0),
        (-0.8462747849789, -1.4355304359676908, 0.0),
        (-0.7323984146262822, -1.4957469684510287, 0.0),
        (-0.595637862454051, -1.552676377691546, 0.0),
        (-0.5071287351045465, -1.5823616847532773, 0.0),
        (-0.4166666666666675, -1.607888940964566, 0.0),
        (-0.4166666666666672, -2.5, 0.0),
        (0.41666666666666635, -2.5, 0.0),
        (0.41666666666666624, -1.6078889409645671, 0.0),
        (0.5868838745851082, -1.5558409745749824, 0.0),
        (0.7240457360952962, -1.4996648215027435, 0.0),
        (0.7819200277487277, -1.4711841257953158, 0.0),
        (0.8462747849789012, -1.4355304359676904, 0.0),
        (1.4731391274719736, -2.0623947784607637, 0.0),
        (2.0623947784607637, -1.4731391274719743, 0.0),
        (1.4355304359676917, -0.8462747849789025, 0.0),
        (1.4957469684510294, -0.7323984146262845, 0.0),
        (1.5526763776915462, -0.595637862454052, 0.0),
        (1.5823616847532773, -0.5071287351045469, 0.0),
        (1.607888940964566, -0.4166666666666679, 0.0),
        (2.4999999999999996, -0.4166666666666671, 0.0),
        (2.5, 0.41666666666666635, 0.0),
        (1.6078889409645662, 0.41666666666666624, 0.0),
        (1.5558409745749817, 0.5868838745851086, 0.0),
        (1.4996648215027433, 0.7240457360952968, 0.0),
        (1.4711841257953158, 0.7819200277487283, 0.0),
        (1.4355304359676904, 0.846274784978902, 0.0),
        (2.062394778460763, 1.4731391274719758, 0.0),
        (1.4731391274719727, 2.0623947784607646, 0.0),
        (0.846274784978901, 1.4355304359676917, 0.0),
        (0.732398414626283, 1.4957469684510294, 0.0),
        (0.5956378624540505, 1.5526763776915466, 0.0),
        (0.5071287351045453, 1.5823616847532775, 0.0),
        (0.4166666666666661, 1.6078889409645662, 0.0),
        (0.4166666666666672, 2.5, 0.0),
        (-0.41666666666666635, 2.5, 0.0),
        (-0.41666666666666574, 1.6078889409645662, 0.0),
        (-0.5868838745851078, 1.555840974574982, 0.0),
        (-0.7240457360952958, 1.4996648215027435, 0.0),
        (-0.781920027748727, 1.471184125795316, 0.0),
        (-0.781920027748727, 1.471184125795316, 0.0)
        ]
        CtrlerGearPathing.append(CtrlerGearPathing[0])
        cmds.curve(d=1, p=CtrlerGearPathing, name = "CtrlerGear")

    def FuncCreateCtrlerTransCube(self):
        #BaseSize = 5
        CubePathing =  [
            (-1,1,-1),
            (-1,1,1),
            (1,1,1),
            (1,1,-1),
            (-1,1,-1),
            (-1,-1,-1),
            (-1,-1,1),
            (-1,1,1),
            (-1,-1,1),
            (1,-1,1),
            (1,1,1),
            (1,-1,1),
            (1,-1,-1),
            (1,1,-1),
            (1,-1,-1),
            (-1,-1,-1),
            (1,-1,-1),
            (1,-1,0),
            (0,-1,0),
            (0,-5,0),
        ]
        RecCubePathing = [(x + 0, y + 5, z + 0) for x, y, z in CubePathing]
        cmds.curve(d=1, p=RecCubePathing, name = "CtrlerTransCube")

    def FuncColorReturn(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i]  + '.overrideColor', 0)
            cmds.setAttr(sl_objs[i]  + '.overrideEnabled', 0)

    def FuncColorYellow(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i] +  '.overrideEnabled', 1)
            cmds.setAttr(sl_objs[i] +  '.overrideColor', 17)

    def FuncColorRed(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i] + '.overrideEnabled', 1)
            cmds.setAttr(sl_objs[i] + '.overrideColor', 13)

    def FuncColorBlue(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i] + '.overrideEnabled', 1)
            cmds.setAttr(sl_objs[i] + '.overrideColor', 6)

    def FuncExeJointSize(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i]+".radius", float(self.QLEJointSize.text()))
            
if __name__ == '__main__':
    Win_JoleneToolbox = cls_Window()
    Win_JoleneToolbox.show(dockable=True)
