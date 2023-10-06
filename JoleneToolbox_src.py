#MEL: commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;
#https://www.youtube.com/watch?v=lBz8lEqHXYM&ab_channel=TDSuperheroes
import PySide2 as p2
import maya.OpenMayaUI as omui
import shiboken2
import maya.cmds as cmds
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
def mayaMainWindow():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer),p2.QtWidgets.QWidget)
    
class cls_Window(MayaQWidgetDockableMixin, p2.QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(cls_Window, self).__init__(parent)
        self.setWindowTitle("CA2023 Toolbox"); self.resize(300,500)
        TabGrp_TabGrp = p2.QtWidgets.QTabWidget()
        #self.Tab_General = p2.QtWidgets.QWidget(); self.TabGrp_TabGrp.addTab(self.Tab_General, "General")
        TabGrp_TabGrp.addTab(Tab_General(), "Ggg" )
        TabGrp_TabGrp.addTab(Tab_Naming(), "Naming")

        BtTestFunction = p2.QtWidgets.QPushButton('Press to print something')
        
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
        #UI
        self.QWContainer = p2.QtWidgets.QWidget()
        self.QGLTab_General = p2.QtWidgets.QGridLayout(self.QWContainer)
        self.QWContainer.setFixedHeight(200)

        self.QLGetChildNodes = p2.QtWidgets.QLabel("GetChildNodes")
        self.QLShow =p2.QtWidgets.QLabel("Display return value")
        self.QPBGetChildNodes = p2.QtWidgets.QPushButton("GetChildNodes")
        
        self.QGLTab_General.addWidget(self.QLGetChildNodes,0,0,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QPBGetChildNodes,0,1,p2.QtCore.Qt.AlignTop)
        self.QGLTab_General.addWidget(self.QLShow,1,0,p2.QtCore.Qt.AlignTop)
        
        #show
        self.QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        self.QVBL_mainLayout.addWidget(self.QWContainer)
        
        self.QPBGetChildNodes.clicked.connect(self.FuncGetChildNodes)
        #Func
    def FuncGetChildNodes(self):
        selected_nodes = cmds.ls(selection = True)
        print(selected_nodes)
        pass

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
        
        self.QLPlus = p2.QtWidgets.QLabel("Plus")
        self.QLPlus.setAlignment(p2.QtCore.Qt.AlignTop)
        self.QLPlus.setFrameShape(p2.QtWidgets.QFrame.Box)
        
        #button
        self.QPBPrefixExe.clicked.connect(self.FuncExePrefix)
        self.QPBSuffixExe.clicked.connect(self.FuncExeSuffix)
        self.QPBReplaceExe.clicked.connect(self.FuncExeReplace)
        self.QPBWholeExe.clicked.connect(self.FuncExeWhole)
        
        #Show
        self.QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        self.QVBL_mainLayout.addWidget(self.QWContainer)
        self.QVBL_mainLayout.addWidget(self.QLPlus)

    def FuncExePrefix(self):
        selected_nodes = cmds.ls(selection=True)
        print(selected_nodes)
        IncrementKey = "$N"
        if IncrementKey in self.QLEPrefix.text():
            for i in range(len(selected_nodes)):
                Increment = i+1
                recQLEPrefix = self.QLEPrefix.text().replace(IncrementKey, str(Increment))
                NewName = recQLEPrefix + selected_nodes[i]
                cmds.rename(selected_nodes[i], NewName) 
            else:
                print("No nodes selected")
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
        if selected_nodes:
            for i in selected_nodes:
                #First occurrence.
                NewName = i.replace(self.QLEReplace.text(), self.QLEWith.text(), 1)
                cmds.rename(i, NewName)
        else:
            print("No nodes selected")

    def FuncExeWhole(self):
        #Must add Increment
        selected_nodes = cmds.ls(selection=True)
        print(selected_nodes)
        for i in range(len(selected_nodes)):
            Increment = i+1
            NewName = self.QLEWhole.text() + str(Increment)
            cmds.rename(selected_nodes[i], NewName) 
        else:
            print("No nodes selected")
    
    def SupFuncIncrement(self, str): #Pending
        pass

    # def FuncExeReplace(self):
    #     selected_objects = cmds.ls(selection=True)

    #     search_string = "_g"  # Specify the part you want to replace
    #     replace_string = "_G"  # Specify the replacement string

    #     # Check if any object is selected
    #     if selected_objects:
    #         for selected_object in selected_objects:
    #             # Check if the search string is present in the node name
    #             if search_string in selected_object:
    #                 # Perform the name replacement
    #                 new_name = selected_object.replace(search_string, replace_string)

    #                 # Rename the object with the new name
    #                 cmds.rename(selected_object, new_name)
    #             else:
    #                 # If the search string is not found, print a message
    #                 print("Search string not found in object name:", selected_object)
    #     else:
    #         # If no objects are selected, print a message
    #         print("No objects selected.")
        

if __name__ == '__main__':
    Win_JoleneToolbox = cls_Window()
    Win_JoleneToolbox.show(dockable=True)
