#MEL: commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;
#https://www.youtube.com/watch?v=lBz8lEqHXYM&ab_channel=TDSuperheroes
from re import S
import PySide2 as p2
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
        #self.Tab_General = p2.QtWidgets.QWidget(); self.TabGrp_TabGrp.addTab(self.Tab_General, "General")
        TabGrp_TabGrp.addTab(Tab_General(), "General" )
        TabGrp_TabGrp.addTab(Tab_Naming(), "Naming")

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
        self.depot = []
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

        
        self.QLShow =p2.QtWidgets.QLabel("Display return value")
        self.QLShow.setAlignment(p2.QtCore.Qt.AlignTop)
        self.QLShow.setFrameShape(p2.QtWidgets.QFrame.Box)

        self.QGLTab_General.addWidget(self.QPBGetChildNodes,0,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBGetRelativeT,0,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBSetRelativeT,1,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBSetToZero,1,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBGetMatrix,2,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBSetMatrix,2,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QLShow,3,0,p2.QtCore.Qt.AlignTop)
     
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

    def FuncExePrefix(self):
        selected_nodes = cmds.ls(selection=True)
        print(selected_nodes)
        IncrementKey = "$N"
        if IncrementKey in self.QLEPrefix.text():
            for i in range(len(selected_nodes)):
                Increment = i+1
                StrIncrement = "0" + str(Increment)
                recQLEPrefix = self.QLEPrefix.text().replace(IncrementKey, StrIncrement)
                NewName = recQLEPrefix + selected_nodes[i]
                cmds.rename(selected_nodes[i], NewName) 
        else:
            for i in range(len(selected_nodes)):
                Increment = i+1
                NewName = self.QLEPrefix.text() + selected_nodes[i]
                cmds.rename(selected_nodes[i], NewName) 

    def FuncExeSuffix(self):
        selected_nodes = cmds.ls(selection=True)
        print(selected_nodes)
        IncrementKey = "$N"
        if IncrementKey in self.QLESuffix.text():
            for i in range(len(selected_nodes)):
                Increment = i+1
                recQLESuffix = self.QLESuffix.text().replace(IncrementKey, str(Increment))
                NewName = selected_nodes[i] + recQLESuffix
                cmds.rename(selected_nodes[i], NewName) 
            else:
                print("No nodes selected")
        else:
            for i in range(len(selected_nodes)):
                Increment = i+1
                NewName = selected_nodes[i] + self.QLESuffix.text()
                cmds.rename(selected_nodes[i], NewName) 
            
    def FuncExeReplace(self):
        selected_nodes = cmds.ls(selection=True)
        print(selected_nodes)
        IncrementKey = "$N"
        if IncrementKey in self.QLEWith.text():
            for i in range(len(selected_nodes)):
                Increment = i+1
                recQLEWith = self.QLEWith.text().replace(IncrementKey, str(Increment))
                NewName = selected_nodes[i].replace(self.QLEReplace.text(), recQLEWith, 1)
                cmds.rename(selected_nodes[i], NewName)
            else:
                print("No nodes selected")
        else:
            for i in range(len(selected_nodes)):
                Increment =i+1
                NewName = selected_nodes[i].replace(self.QLEReplace.text(), self.QLEWith.text(), 1)
                cmds.rename(selected_nodes[i], NewName)

    def FuncExeWhole(self):
        #Must add Increment
        selected_nodes = cmds.ls(selection=True)
        
        print(selected_nodes)
        for i in range(len(selected_nodes)):
            Increment = i+1
            #Pending optimization:
            #i+1 % 10 
            if (i+1<=9):
                StrIncrement = "0" +str(Increment)
                NewName = self.QLEWhole.text() + StrIncrement
                cmds.rename(selected_nodes[i], NewName) 
            else:
                StrIncrement =  str(Increment)
                NewName = self.QLEWhole.text() + StrIncrement
                cmds.rename(selected_nodes[i], NewName) 
        else:
            print("No nodes selected")
        
    def SupFuncIncrement(self, str): #Pending
        pass
 
if __name__ == '__main__':
    Win_JoleneToolbox = cls_Window()
    Win_JoleneToolbox.show(dockable=True)
