#MEL: commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;
#https://www.youtube.com/watch?v=lBz8lEqHXYM&ab_channel=TDSuperheroes
#from re import S
import math
import PySide2 as p2
import re
import maya.OpenMayaUI as omui
import shiboken2
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin

sVersion = "0.01"
"""
Log:
2023.10.13 
Naming tool now accepts %N for all func. and smart increment
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
        print(selected_nodes.index)
        
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
 
class Tab_Rigging(p2.QtWidgets.QWidget):
    def __init__(self, parent=None):
        p2.QtWidgets.QWidget.__init__(self,parent)
        #UI
        self.QWContainer = p2.QtWidgets.QWidget()
        self.QGLTab_Naming = p2.QtWidgets.QGridLayout(self.QWContainer)
        self.QWContainer.setFixedHeight(200)
        #button
        self.QPBColorReturn = p2.QtWidgets.QPushButton("ColorReturn", self)
        self.QPBColorYellow = p2.QtWidgets.QPushButton("ColorYellow", self)
        self.QPBColorRed = p2.QtWidgets.QPushButton("ColorRed", self)
        self.QPBColorBlue = p2.QtWidgets.QPushButton("ColorBlue", self)
        
        self.QLJointSize = p2.QtWidgets.QLabel("JointSize")
        self.QLEJointSize = p2.QtWidgets.QLineEdit("")
        self.QPBJointSizeExe = p2.QtWidgets.QPushButton("Execute", self)

        self.QGLTab_Naming.addWidget(self.QPBColorReturn,0,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBColorYellow,0,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBColorRed,1,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBColorBlue,1,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLJointSize,2,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QLEJointSize,2,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_Naming.addWidget(self.QPBJointSizeExe,2,2,p2.QtCore.Qt.AlignTop)
        #interaction
        self.QPBColorReturn.clicked.connect(self.FuncColorReturn)
        self.QPBColorYellow.clicked.connect(self.FuncColorYellow)
        self.QPBColorRed.clicked.connect(self.FuncColorRed)
        self.QPBColorBlue.clicked.connect(self.FuncColorBlue)

        self.QPBJointSizeExe.clicked.connect(self.FuncExeJointSize)
        #show
        self.QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        self.QVBL_mainLayout.addWidget(self.QWContainer)

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
