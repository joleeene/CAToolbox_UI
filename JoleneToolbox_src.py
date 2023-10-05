#MEL: commandPort -name "localhost:7001" -sourceType "mel" -echoOutput;
#https://www.youtube.com/watch?v=lBz8lEqHXYM&ab_channel=TDSuperheroes
import PySide2 as p2
import maya.OpenMayaUI as omui
import shiboken2
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
def mayaMainWindow():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer),p2.QtWidgets.QWidget)
    
class cls_Window(MayaQWidgetDockableMixin, p2.QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(cls_Window, self).__init__(parent)
        self.setWindowTitle("op"); self.resize(500,500)
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
        print("pppp")
        
class Tab_General(p2.QtWidgets.QWidget):
    def __init__(self, parent = None):
        p2.QtWidgets.QWidget.__init__(self, parent)
        lb = p2.QtWidgets.QLabel("c")
        QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        QVBL_mainLayout.addWidget(lb)
        #self.setLayout(QVBL_mainLayout)

class Tab_Naming(p2.QtWidgets.QWidget):
    def __init__(self, parent=None):
        p2.QtWidgets.QWidget.__init__(self,parent)
        QWContainer = p2.QtWidgets.QWidget()
        QGLTab_Naming = p2.QtWidgets.QGridLayout(QWContainer)
        QWContainer.setFixedHeight(100)

        QLPrefix = p2.QtWidgets.QLabel("Prefix");QLSuffix = p2.QtWidgets.QLabel("Suffix")
        QLReplace = p2.QtWidgets.QLabel("Replace");QLWith = p2.QtWidgets.QLabel("With")
        QLEPrefix = p2.QtWidgets.QLineEdit("")

        QLESuffix = p2.QtWidgets.QLineEdit("")
        QLERReplace = p2.QtWidgets.QLineEdit("")
        QLEWith = p2.QtWidgets.QLineEdit("")
        QPBPrefixExe = p2.QtWidgets.QPushButton("Execute", self)
        QPBSuffixExe = p2.QtWidgets.QPushButton("Execute", self)
        QPBReplaceExe = p2.QtWidgets.QPushButton("Execute", self)
        
        QGLTab_Naming.addWidget(QLPrefix,0,0,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QLEPrefix,0,1,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QPBPrefixExe,0,2,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QLSuffix,0,3,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QLESuffix,0,4,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QPBSuffixExe,0,5,p2.QtCore.Qt.AlignTop)
        
        QGLTab_Naming.addWidget(QLReplace,1,0,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QLERReplace,1,1,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QLWith,1,3,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QLEWith,1,4,p2.QtCore.Qt.AlignTop)
        QGLTab_Naming.addWidget(QPBReplaceExe,1,5,p2.QtCore.Qt.AlignTop)

        #Logic
        QPBPrefixExe.clicked.connect(self.FuncAddPrefix)


        QLPlus = p2.QtWidgets.QLabel("Plus")
        QLPlus.setAlignment(p2.QtCore.Qt.AlignTop)
        QLPlus.setFrameShape(p2.QtWidgets.QFrame.Box)
        QVBL_mainLayout = p2.QtWidgets.QVBoxLayout(self)
        QVBL_mainLayout.addWidget(QWContainer)
        QVBL_mainLayout.addWidget(QLPlus)
    def FuncAddPrefix(self):
        
        print("pssppp")

if __name__ == '__main__':
    Win_JoleneToolbox = cls_Window()
    Win_JoleneToolbox.show(dockable=True)