#General Import
import math, copy, re
#import PySide2 as p2
import PySide6 as p6
import maya.OpenMayaUI as omui
import maya.api.OpenMaya as om
#import shiboken2
import shiboken6
import maya.cmds as cmds
from PySide6 import QtGui, QtCore
from PySide6.QtCore import QFile
from PySide6.QtCore import Qt
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide6.QtUiTools import QUiLoader


the_path =   r"C:\Users\linxy\OneDrive\OrganizeFilesStructure\08_Environment\Config\Maya\script\CAToolbox_UI"
# def PathRectifier(Input_Str):
#     return Input_Str.replace("\\", "/")
# rec_path = PathRectifier(path)

import sys

if the_path not in sys.path:
    sys.path.append(the_path)
import importlib

#Utils files import
import utils

from utils.utilsTest import *
from utils.createCtrler import *
import utils.createCtrler2 as cc2
from utils.modCtrlerColor import *
from utils.CreateIK import *
importlib.reload(cc2)


def mayaMainWindow():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken6.wrapInstance(int(mainWindowPointer), p6.QtWidgets.QWidget)

class ClickableLabel(p6.QtWidgets.QLabel):
    clicked = QtCore.Signal()
    def mousePressEvent(self, event):
        self.clicked.emit()

class cls_Window(MayaQWidgetDockableMixin, p6.QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(cls_Window, self).__init__(parent)
        
        self.setWindowTitle("CA2023 Toolbox")
        self.resize(500 , 650)
        
        file_path = the_path+"/ui/CAToolbox_UI.ui"
        ##################################################################################
        ui_loader = QUiLoader()
        ui_file = QFile(file_path)
        self.ui = ui_loader.load(ui_file)
        ########################################## Must do or else it's a seperated window.
        layout = p6.QtWidgets.QVBoxLayout(self)
        layout.addWidget(self.ui)
        ##################################################################################

        ### Public var 
        #Tab_General
        self.attrArray = [
            ".translateX",
            ".translateY",
            ".translateZ",
            ".rotateX",
            ".rotateY",
            ".rotateZ"
        ]
        ###

        ###Connection
        #Tab_General
        self.ui.QPBTestFunc.clicked.connect(self.FuncTest)
        self.ui.QPBGetChildNodes.clicked.connect(self.FuncGetChildNodes)
        self.ui.QPBGetRelativeT.clicked.connect(self.FuncGetRelativeT)
        self.ui.QPBSetRelativeT.clicked.connect(self.FuncSetRelativeT)
        self.ui.QPBBackToOrigin.clicked.connect(self.FuncBackToOrigin)
            # self.ui.QPBGetMatrix.clicked.connect(utils.Tab_General.FuncGetMatrix)
            # self.ui.QPBSetMatrix.clicked.connect(utils.Tab_General.FuncSetMatrix)
        self.ui.QPBCreateGarbage.clicked.connect(self.FuncCreateGarbage)
        self.ui.QPBCreateChildJoint.clicked.connect(self.FuncCreateChildJoint)

        self.ui.QPBOutlinerColorReturn.clicked.connect(self.FuncOutlinerColorReturn)
        self.ui.QPBOutlinerColorRed.clicked.connect(self.FuncOutlinerColorRed)
        self.ui.QPBOutlinerColorCyan.clicked.connect(self.FuncOutlinerColorCyan)
        self.ui.QPBOutlinerColorGreen.clicked.connect(self.FuncOutlinerColorGreen)

        #Tab_Naming
        self.ui.QPBPrefixExe.clicked.connect(self.FuncExePrefix2)
        self.ui.QPBSuffixExe.clicked.connect(self.FuncExeSuffix2)
        self.ui.QPBReplaceExe.clicked.connect(self.FuncExeReplace2)
        self.ui.QPBWholeExe.clicked.connect(self.FuncExeWhole2)

        #Tab_Rigging

        self.ui.QPBCtrlerCube.clicked.connect(lambda: cc2.ctrler(n="testctrl",
                p=cc2.ctrler.cube_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSphere.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.sphere_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerPrism.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.prism_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerRing.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.ring_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerRotPike.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.rotPike_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerRot1Dir.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.rot1Dir_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerTran1Dir.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.tran1Dir_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerGear.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.gear_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerTransCube.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.transCube_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrler4DirCirc.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.fourDirCirc_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        
        self.ui.QPBCtrlerM03.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.masterCtl03_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerM02.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.masterCtl02_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerM01.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.masterCtl01_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerBendyLimb.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.bendyLimb_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerHandCtl.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.handCtl_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerFin01.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.finCtl_01_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerFin02.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.finCtl_02_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerFin03.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.finCtl_03_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerFin04.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.finCtl_04_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerFinMeta.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.finCtl_meta_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSpineIkTip.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.spineIkTip_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSpineFk.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.spineFk_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSpineIkRoot.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.spineIkRoot_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSpineIkInv1.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.spineIkInv01_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSpineIkInv2.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.spineIkInv02_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        self.ui.QPBCtrlerSpineIkMid.clicked.connect(lambda: cc2.ctrler(n=self.Ctrler_update_name(),
                p=cc2.ctrler.spineIkMid_v, norm=self.Ctrler_update_direction(), 
                scl=float(self.ui.QLECtrlerSize.text())))
        

        self.ui.QPBColorReturn.clicked.connect(modCtrlerColor_ReturnColor)
        self.ui.QPBColorYellow.clicked.connect(modCtrlerColor_TurnYellow)
        self.ui.QPBColorRed.clicked.connect(modCtrlerColor_TurnRed)
        self.ui.QPBColorBlue.clicked.connect(modCtrlerColor_TurnBlue)
        self.ui.QPBColorPurple.clicked.connect(modCtrlerColor_TurnPurple)
        self.ui.QPBColorPink.clicked.connect(modCtrlerColor_TurnPink)
        self.ui.QPBColorSkin.clicked.connect(modCtrlerColor_TurnSkin)

        self.ui.QPBColorCyan.clicked.connect(modCtrlerColor_TurnCyan)

        self.ui.QPBJointSizeExe.clicked.connect(self.FuncExeJointSize)

        self.ui.QPBCreateFKRing.clicked.connect(self.FuncCreateFKRing)
        self.ui.QPBCreateIKRevFoot.clicked.connect(self.createIK_CreateIKRevFoot)
        self.ui.QPBCreateLoc.clicked.connect(self.FuncCreateLoc)
        self.ui.QPBGetCrvVtxPList.clicked.connect(self.FuncGetCrvVtxPList)
        self.ui.QPBCVsoftCluster.clicked.connect(self.FuncCreate_CVsoftCluster)
        self.ui.QPBCreateIKFKSwitch.clicked.connect(self.FuncCreate_IKFKSwitch)
        
        self.ui.QPBJointChain.clicked.connect(self.FuncCreate_JointChain)

        #Tab_Animation
        self.ui.QPBrivet.clicked.connect(self.FuncRivet)
        self.ui.QPBscreenSpaceMoTrail.clicked.connect(self.FuncScreenSpaceMoTrail)
        self.ui.QPBslAllCtrlWithKeys.clicked.connect(self.FuncslAllCtrlWithKeys)

        ###
        self.ui.show()  
    ###Func
    def test(self):
        print("VVVVVVVV")

    def Ctrler_update_direction(self):
        d=[1,0,0]
        if self.ui.QRBX.isChecked():
            d=[1,0,0]
        if self.ui.QRBY.isChecked():
            d=[0,1,0]
        if self.ui.QRBZ.isChecked():
            d=[0,0,1]
        return d
    
    def Ctrler_update_name(self):
        n="testCtrl"
        if self.ui.QLECtrlName.text():
            n=self.ui.QLECtrlName.text()

        return n

    def RealRestTransform(self, input_obj):
        attrArray = [
            "translateX",
            "translateY",
            "translateZ",
            "rotateX",
            "rotateY",
            "rotateZ"
            ]
        for j in range(len(attrArray)):
                BLattrLocked = cmds.getAttr(input_obj + "." + attrArray[j], lock=True)
                if BLattrLocked:
                    continue
                else:
                    cmds.setAttr(input_obj + "." + attrArray[j],0) 

    #Tab_General
    def FuncTest(self):
        selected_nodes = cmds.ls(selection=True, long=False)
        print("length=", len(selected_nodes))
        print(selected_nodes)

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

        self.ui.QLShow.setText(f"""
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

    def FuncBackToOrigin(self):
        sl_objs = cmds.ls(selection =True)
        if not sl_objs:
            print("Nothing selected or Not having a transform attr.")
            return
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
        ls_null_obj = []
        for i in range(len(sl_objs)):
            nul_obj = cmds.group(empty=True, name=sl_objs[i]+"_Off")
            cmds.xform(nul_obj, worldSpace=True, matrix = world_transform_pool[i])
            # Parent the original object under the null object
            cmds.parent(sl_objs[i], nul_obj)
        # Reparent the original object to its original parent
            if original_parent_pool[i]:
                cmds.parent(nul_obj, original_parent_pool[i])
            ls_null_obj.append(nul_obj)
        cmds.select(cl=1)
        cmds.select(ls_null_obj, add=1)

    def FuncCreateChildJoint(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            iter_newname = sl_objs[i] + "_Jx"
            iter_joint = cmds.createNode("joint", n=iter_newname)
            cmds.parent(iter_joint, sl_objs[i])
            self.RealRestTransform(iter_joint)
        
    def FuncOutlinerColorReturn(self):
        ls_obj = cmds.ls(sl=1)
        for i in range(len(ls_obj)):
            iter_attr0 = ls_obj[i]+".useOutlinerColor"
            iter_attr1 = ls_obj[i]+".outlinerColor"
            cmds.setAttr(iter_attr0, 0)
            cmds.setAttr(iter_attr1, 0,0,0)

    def FuncOutlinerColorRed(self):
        ls_obj = cmds.ls(sl=1)
        for i in range(len(ls_obj)):
            iter_attr0 = ls_obj[i]+".useOutlinerColor"
            iter_attr1 = ls_obj[i]+".outlinerColor"
            cmds.setAttr(iter_attr0, 1)
            cmds.setAttr(iter_attr1, 1, 0.3, 0.3)

    def FuncOutlinerColorCyan(self):
        ls_obj = cmds.ls(sl=1)
        for i in range(len(ls_obj)):
            iter_attr0 = ls_obj[i]+".useOutlinerColor"
            iter_attr1 = ls_obj[i]+".outlinerColor"
            cmds.setAttr(iter_attr0, 1)
            cmds.setAttr(iter_attr1, 0,1,1)

    def FuncOutlinerColorGreen(self):
        ls_obj = cmds.ls(sl=1)
        for i in range(len(ls_obj)):
            iter_attr0 = ls_obj[i]+".useOutlinerColor"
            iter_attr1 = ls_obj[i]+".outlinerColor"
            cmds.setAttr(iter_attr0, 1)
            cmds.setAttr(iter_attr1, 0,1,0)



    #Tab_Naming
    cmds.select

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
        if IncrementKey in self.ui.QLEPrefix.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero -math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                    Zero_Apply = Zero_Apply + Zero
                    
                recIncrement = Zero_Apply + str(Increment)
                recQLEPrefix = self.ui.QLEPrefix.text().replace(IncrementKey, recIncrement)
                print(recQLEPrefix)
                NewName = recQLEPrefix + Re_sl_objs[i]
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
        else:
            for i in range(len(sl_objs)):
                Increment = i+1
                NewName = self.ui.QLEPrefix.text() + Re_sl_objs[i]
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
    
    def FuncExePrefix2(self):
        sl_objs = cmds.ls(sl=1)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        sl_objs_uuid = cmds.ls(sl=1, uuid=1)
        IncrementKey = "$N"
        if IncrementKey in self.ui.QLEPrefix.text():
            howManyZero = len(sl_objs)
            howManyZero = len(str(howManyZero))
            for i in range(len(sl_objs)):
                recQLEPrefix = self.ui.QLEPrefix.text().replace(IncrementKey, str(i+1).zfill(howManyZero+1))
                newname = recQLEPrefix + Re_sl_objs[i]
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
        else:
            for i in range(len(sl_objs)):
                recQLEPrefix = self.ui.QLEPrefix.text()
                newname = recQLEPrefix + Re_sl_objs[i]
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
                
            

    def FuncExeSuffix(self):
        sl_objs = cmds.ls(selection=True)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        print(Re_sl_objs)
        IncrementKey = "$N"
        Zero = "0"
        MaxZero = math.floor(math.log10(len(sl_objs)))+1
        if IncrementKey in self.ui.QLESuffix.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero -math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                    Zero_Apply = Zero_Apply + Zero
                    
                recIncrement = Zero_Apply + str(Increment)
                recQLESuffix = self.ui.QLESuffix.text().replace(IncrementKey, recIncrement)
                NewName = Re_sl_objs[i] + recQLESuffix
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
            else:
                print("No nodes selected")
        else:
            for i in range(len(sl_objs)):
                Increment = i+1
                NewName = Re_sl_objs[i] + self.ui.QLESuffix.text()
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)

    def FuncExeSuffix2(self):
        sl_objs = cmds.ls(sl=1)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        sl_objs_uuid = cmds.ls(sl=1, uuid=1)
        IncrementKey = "$N"
        if IncrementKey in self.ui.QLESuffix.text():
            howManyZero = len(sl_objs)
            howManyZero = len(str(howManyZero))
            for i in range(len(sl_objs)):
                recQLESuffix = self.ui.QLESuffix.text().replace(IncrementKey, str(i+1).zfill(howManyZero+1))
                newname = Re_sl_objs[i] + recQLESuffix
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
        else:
            for i in range(len(sl_objs)):
                recQLESuffix = self.ui.QLESuffix.text()
                newname = Re_sl_objs[i] + recQLESuffix
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
        
    def FuncExeReplace(self):
        sl_objs = cmds.ls(selection=True)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        print(Re_sl_objs)
        IncrementKey = "$N"
        Zero = "0"
        MaxZero = math.floor(math.log10(len(sl_objs)))+1
        if IncrementKey in self.ui.QLEWith.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero -math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                    Zero_Apply = Zero_Apply + Zero
                    
                recIncrement = Zero_Apply + str(Increment)
                recQLEWith = self.ui.QLEWith.text().replace(IncrementKey, recIncrement)
                NewName = Re_sl_objs[i].replace(self.ui.QLEReplace.text(), recQLEWith, 1)
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
            else:
                print("No nodes selected")
        else:
            for i in range(len(sl_objs)):
                Increment =i+1
                NewName = Re_sl_objs[i].replace(self.ui.QLEReplace.text(), self.ui.QLEWith.text(), 1)
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)

    def FuncExeReplace2(self):
        sl_objs = cmds.ls(sl=1)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        sl_objs_uuid = cmds.ls(sl=1, uuid=1)
        IncrementKey = "$N"
        if IncrementKey in self.ui.QLEWith.text():
            howManyZero = len(sl_objs)
            howManyZero = len(str(howManyZero))
            for i in range(len(sl_objs)):
                recQLEWith = self.ui.QLEWith.text().replace(IncrementKey, str(i+1).zfill(howManyZero+1))
                newname = Re_sl_objs[i].replace(self.ui.QLEReplace.text(), recQLEWith, 1)
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
        else:
            for i in range(len(sl_objs)):
                newname = Re_sl_objs[i].replace(self.ui.QLEReplace.text(), self.ui.QLEWith.text(), 1)
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)


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

        if IncrementKey in self.ui.QLEWhole.text():
            for i in range(len(sl_objs)):
                Increment = i+1
                ZeroDigits = MaxZero - math.floor(math.log10(Increment))
                Zero_Apply = ""
                for j in range(ZeroDigits):
                        Zero_Apply = Zero_Apply + Zero
                recIncrement = Zero_Apply + str(Increment)
                recQLEWhole = self.ui.QLEWhole.text().replace(IncrementKey, recIncrement)
                print(recQLEWhole)
                NewName = recQLEWhole
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
            else:
                print("No nodes selected")
        else:
            for i in range(len(sl_objs)):
                Increment = i+1
                NewName = self.ui.QLEWhole.text()
                cmds.rename(sl_objs[i], NewName)
                sl_objs = cmds.ls(selection=True)
    
    def FuncExeWhole2(self):
        sl_objs = cmds.ls(sl=1)
        Re_sl_objs = self.AuxFuncMakeRelativeName(sl_objs) #relative namepath list
        sl_objs_uuid = cmds.ls(sl=1, uuid=1)
        IncrementKey = "$N"
        if IncrementKey in self.ui.QLEWhole.text():
            howManyZero = len(sl_objs)
            howManyZero = len(str(howManyZero))
            for i in range(len(sl_objs)):
                recQLEWhole = self.ui.QLEWhole.text().replace(IncrementKey, str(i+1).zfill(howManyZero+1))
                newname = recQLEWhole
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
        else:
            for i in range(len(sl_objs)):
                newname = self.ui.QLEWhole.text()
                cmds.rename(cmds.ls(sl_objs_uuid[i])[0], newname)
    #Tab_Rigging
                
    def FuncExeJointSize(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i]+".radius", float(self.ui.QLEJointSize.text()))

    def FuncCreateFKRing(self):
        ls_ctl=[]
        #Decide what is the joint primary axis
        ls_sl_objs = cmds.ls(sl=True)
        ls_final_obj=ls_sl_objs[-1]
        x=round(cmds.getAttr(ls_final_obj+".translateX"),6)
        y=round(cmds.getAttr(ls_final_obj+".translateY"),6)
        z=round(cmds.getAttr(ls_final_obj+".translateZ"),6)
        if x==-0:
            x=0
        if y==-0:
            y=0
        if z==-0:
            z=0
        normal=[0,0,0]
        if (x != 0) and (y==0) and (z==0): #joint x axis point to next joint
            normal = [1,0,0]
        elif (y != 0) and (x==0) and (z==0):
            normal = [0,1,0]
        elif (z != 0) and (y==0) and (x==0):
            normal = [0,0,1]
        for i in range(len(ls_sl_objs)):
            a = cmds.circle(nr=normal, name = ls_sl_objs[i]+"_FK_Ctl")
            cmds.matchTransform(a, ls_sl_objs[i], piv=0, rot=0, scl=0, pos=1)
            ls_ctl.append(ls_sl_objs[i]+"_FK_Ctl")
        ls_ctl.reverse()
        for i in range(len(ls_ctl)):
            if i+2 <= len(ls_ctl):
                cmds.parent(ls_ctl[i], ls_ctl[i+1])
            else:continue
        ls_ctl.reverse()
        ls_cstr = []
        for i in range(len(ls_ctl)):
            a = cmds.parentConstraint(ls_ctl[i],ls_sl_objs[i],mo=1)
            ls_cstr.append(a[0])
        print(ls_cstr)
        return [ls_ctl, ls_cstr]

    String_Warning0 = "Nothing selected"
    String_Warning1 = "Not Jnt"
    def get_LR_Dir(self,input_obj): 
        if input_obj == None:
            print(String_Warning0)
            return
        first_2_characters = input_obj[:2]
        if first_2_characters == "L_": 
            s_LR_Dir = first_2_characters
        elif first_2_characters == "R_": 
            s_LR_Dir = first_2_characters
        elif first_2_characters == "T_": 
            s_LR_Dir = first_2_characters
        elif first_2_characters == "B_": 
            s_LR_Dir = first_2_characters
        elif input_obj[:4] == "Dir_":#Debug 
            s_LR_Dir = "Dir_"
        else:
            s_LR_Dir = ""
        return s_LR_Dir

    def get_sl_obj_and_LR_Dir(self):
        input_sl_obj = cmds.ls(sl=True)[0]
        if input_sl_obj == None:
            print(String_Warning0)
            return
        Ls_sl_ChildObjs = cmds.listRelatives(input_sl_obj, ad=True)
        Ls_sl_ChildObjs.append(input_sl_obj)
        Ls_BindJnt = Ls_sl_ChildObjs
        Ls_BindJnt.reverse()
        LR_Dir = self.get_LR_Dir(input_sl_obj) # Pending refactor
        return [Ls_BindJnt, LR_Dir]

    def get_IKFKjnt_list_after_dup(self, Input_sl_obj, Input_IKorFK, Input_OriginJointList, Input_LR_Prefix):
        cmds.duplicate(Input_sl_obj, rc=True)
        Ls_JustDupIKFKJntName = []
        suffix = "1"
        Ls_JustDupIKFKJntName = [i + suffix for i in Input_OriginJointList]
        Ls_TrgIKFKJntName = [i + suffix for i in Input_OriginJointList]
        
        LR_Prefix = Input_LR_Prefix
        LR_PrefixPlusIKFK = Input_LR_Prefix + Input_IKorFK
        Ls_TrgIKFKJntName = [i.replace(LR_Prefix, LR_PrefixPlusIKFK) for i in Ls_TrgIKFKJntName]
        Ls_TrgIKFKJntName = [i[:-1] for i in Ls_TrgIKFKJntName]

        for i in range(len(Ls_JustDupIKFKJntName)):
            cmds.rename(Ls_JustDupIKFKJntName[i], Ls_TrgIKFKJntName[i])
        return Ls_TrgIKFKJntName

    def get_sl_obj_world_PSR(self,InputJnt):
        InputJntMx = cmds.xform(InputJnt, query=True, matrix=True, worldSpace=True)
        InputJntT = [InputJntMx[12], InputJntMx[13], InputJntMx[14]]
        InputJntRo = cmds.xform(InputJnt, query=True, rotation=True, worldSpace=True)
        InputJntS = cmds.xform(InputJnt, query=True, scale=True, worldSpace=True)
        a = [InputJntT, InputJntRo, InputJntS]
        return a

    def createIK_CreateIKRevFoot(self):#Main
        #IK Part
        Ls_origin_jnt=self.get_sl_obj_and_LR_Dir()[0]; LR_Dir=self.get_sl_obj_and_LR_Dir()[1]
        Ls_IKJnt=self.get_IKFKjnt_list_after_dup(Ls_origin_jnt[0], "IK" , Ls_origin_jnt, LR_Dir)
        print(Ls_IKJnt)
        ThighFootIkhNewName = LR_Dir+"ThighFoot_Ikh"
        FootBallIkhNewName = LR_Dir+"FootBall_Ikh"
        BallTipIkhNewName = LR_Dir+"BallTip_Ikh"
        cmds.ikHandle(sj=Ls_IKJnt[0], ee=Ls_IKJnt[2], sol="ikRPsolver", n=ThighFootIkhNewName)
        cmds.ikHandle(sj=Ls_IKJnt[2], ee=Ls_IKJnt[3], sol="ikSCsolver", n=FootBallIkhNewName)
        cmds.ikHandle(sj=Ls_IKJnt[3], ee=Ls_IKJnt[4], sol="ikSCsolver", n=BallTipIkhNewName)

        #Create Ctrler
        IKFootCtrlerNewName = LR_Dir+"IKFoot_Ctl"
        IKFootCtrler = createCtrler_Cube(IKFootCtrlerNewName)
        IKFootJntWorldPSR = get_sl_obj_world_PSR(Ls_IKJnt[2])
        cmds.xform(IKFootCtrler, t=IKFootJntWorldPSR[0] ,ro=[0,0,0], s=IKFootJntWorldPSR[2], worldSpace=True)
        

        IKBallRollCtrlerNewName = LR_Dir+"IKBall_Ctl"
        IKBallRollCtrler = cmds.circle( nr =(0,0,1), c=(0,0,0),r=2, ch=0, n=IKBallRollCtrlerNewName)
        IKBallJntWorldPSR = get_sl_obj_world_PSR(Ls_IKJnt[3])
        cmds.xform(IKBallRollCtrler, t=IKBallJntWorldPSR[0] ,ro = [0,0,0], s=IKBallJntWorldPSR[2], worldSpace=True)
        cmds.parent(BallTipIkhNewName, IKBallRollCtrlerNewName)

        RevIKBallCtrlerNewName = LR_Dir+"RevIKBall_Ctl"
        RevIKBallCtrler = createCtrler_Rot1Dir(RevIKBallCtrlerNewName) #Inherit
        cmds.xform(RevIKBallCtrler, t=IKBallJntWorldPSR[0] ,ro = [0,0,0], s=IKBallJntWorldPSR[2], worldSpace=True)
        cmds.parent(FootBallIkhNewName,RevIKBallCtrlerNewName)
        
        cmds.parent(ThighFootIkhNewName,RevIKBallCtrlerNewName)

        RevIKTipToeCtrlerNewName = LR_Dir+"RevIKTipToe_Ctl"
        RevIKTipToeCtrler = createCtrler_Rot1Dir(RevIKTipToeCtrlerNewName) #Inherit
        IKTipJntWorldPSR = get_sl_obj_world_PSR(Ls_IKJnt[4])
        cmds.xform(RevIKTipToeCtrler, t=IKTipJntWorldPSR[0] ,ro = [0,0,0], s=IKTipJntWorldPSR[2], worldSpace=True)
        cmds.parent(IKBallRollCtrlerNewName,RevIKTipToeCtrlerNewName)
        cmds.parent(RevIKBallCtrlerNewName,RevIKTipToeCtrlerNewName)

        RevIKHeelCtrlerNewName = LR_Dir+"RevIKHeel_Ctl"
        RevIKHeelCtrler = createCtrler_Rot1Dir(RevIKHeelCtrlerNewName)  #Inherit
        IKHeelJntWorldPSR = get_sl_obj_world_PSR(Ls_IKJnt[5])
        cmds.xform(RevIKHeelCtrler, t=IKHeelJntWorldPSR[0] ,ro = [0,0,0], s=IKHeelJntWorldPSR[2], worldSpace=True)
        cmds.parent(RevIKTipToeCtrlerNewName,RevIKHeelCtrlerNewName)

        IKPoleCtrlerNewName = LR_Dir+"IKPole_Ctl"
        IKPoleCtrler = createCtrler_Prism(IKPoleCtrlerNewName)#Inherit
        IKTibiaWorldPSR = get_sl_obj_world_PSR(Ls_IKJnt[1])
        IKTibiaWorldPSR[0][2] += 10
        IKPoleT = IKTibiaWorldPSR[0]
        cmds.xform(IKPoleCtrler, t=IKPoleT ,ro = [0,0,0], s=IKTibiaWorldPSR[2], worldSpace=True)
        cmds.poleVectorConstraint(IKPoleCtrlerNewName, ThighFootIkhNewName)


        # Create a null object
        def CreateDistNullNode(InputLR, InputName, InputTrgPrt, InputTrgTransform):
            tempNodeNewName = InputLR + InputName
            tempNodeNewName = cmds.createNode('transform', name=tempNodeNewName)
            if InputTrgPrt != None:
                cmds.parent(tempNodeNewName, InputTrgPrt)
            cmds.matchTransform(tempNodeNewName, InputTrgTransform, pos=True,rot=True,scale=True)
            return tempNodeNewName

        IKFootDistNewName = CreateDistNullNode(LR_Dir, "IKFootDist_Nul", IKFootCtrlerNewName, IKFootCtrlerNewName)
        cmds.parent(IKPoleCtrlerNewName, IKFootCtrlerNewName)
        cmds.parent(RevIKHeelCtrlerNewName, IKFootCtrlerNewName)
        IKThighDistNewName = CreateDistNullNode(LR_Dir, "IKThighDist_Nul", None, Ls_IKJnt[0])


        #Create Node Network
        IKFootDistBtweenNodeNewName = LR_Dir + "IKFootDistBetween_Nod"
        IKFootDistBtweenNode = cmds.createNode("distanceBetween", name=IKFootDistBtweenNodeNewName)
        IKFootDistBtweenNode_name = cmds.ls(IKFootDistBtweenNode)[0]
        cmds.connectAttr(IKFootDistNewName+".worldMatrix[0]", IKFootDistBtweenNode_name+".inMatrix1")
        cmds.connectAttr(IKThighDistNewName+".worldMatrix[0]", IKFootDistBtweenNode_name+".inMatrix2")

        MultiDvdCalcRateNodeNewName=LR_Dir+"MultiDvdCalcRate"
        MultiDvdCalcRateNode=cmds.createNode("multiplyDivide", n=MultiDvdCalcRateNodeNewName)
        MultiDvdCalcRateNode_name = cmds.ls(MultiDvdCalcRateNode)[0]
        OriginDist = cmds.getAttr(Ls_IKJnt[1]+".translateY") + cmds.getAttr(Ls_IKJnt[2]+".translateY")
        cmds.setAttr(MultiDvdCalcRateNode_name+".input2X", OriginDist)
        cmds.setAttr(MultiDvdCalcRateNode_name+".operation", 2)
        MultiDvdApplyRateNodeNewName=LR_Dir+"MultiDvdApplyRate"
        MultiDvdApplyRateNode=cmds.createNode("multiplyDivide", n=MultiDvdApplyRateNodeNewName)
        MultiDvdApplyRateNode_name = cmds.ls(MultiDvdApplyRateNode)[0]
        cmds.connectAttr(IKFootDistBtweenNode_name+".distance", MultiDvdCalcRateNodeNewName+".input1X")
        ThighTibiaDist = cmds.getAttr(Ls_IKJnt[1]+".translateY")
        TibiaFootDist = cmds.getAttr(Ls_IKJnt[2]+".translateY")
        cmds.setAttr(MultiDvdApplyRateNode_name+".input2X", ThighTibiaDist)
        cmds.setAttr(MultiDvdApplyRateNode_name+".input2Y", TibiaFootDist)
        cmds.connectAttr(MultiDvdCalcRateNode_name+".outputX", MultiDvdApplyRateNodeNewName+".input1X")
        cmds.connectAttr(MultiDvdCalcRateNode_name+".outputX", MultiDvdApplyRateNodeNewName+".input1Y")

        ConditionNodeNewName = LR_Dir+"Condi_Nod"
        ConditionNode = cmds.createNode("condition", n=ConditionNodeNewName)
        ConditionNode_name = cmds.ls(ConditionNode)[0]
        cmds.setAttr(ConditionNode_name+".colorIfFalseR", ThighTibiaDist)
        cmds.setAttr(ConditionNode_name+".colorIfFalseG", TibiaFootDist)
        cmds.setAttr(ConditionNode_name+".operation", 2)
        IKThighFootLengthSum = cmds.getAttr(Ls_IKJnt[1]+".translateY") + cmds.getAttr(Ls_IKJnt[2]+".translateY")
        cmds.setAttr(ConditionNode_name+".secondTerm", IKThighFootLengthSum)
        cmds.connectAttr(MultiDvdApplyRateNodeNewName+".outputX", ConditionNode_name+".colorIfTrueR")
        cmds.connectAttr(MultiDvdApplyRateNodeNewName+".outputY", ConditionNode_name+".colorIfTrueG")
        cmds.connectAttr(IKFootDistBtweenNode_name+".distance", ConditionNode_name+".firstTerm")

        cmds.connectAttr(ConditionNode_name+".outColorR", Ls_IKJnt[1]+".translateY")
        cmds.connectAttr(ConditionNode_name+".outColorG", Ls_IKJnt[2]+".translateY")

    def FuncCreateLoc(self):
        a = cmds.exactWorldBoundingBox()
        cx = (a[0]+a[3])*0.5
        cy = (a[1]+a[4])*0.5
        cz = (a[2]+a[5])*0.5
        loc = cmds.spaceLocator()
        cmds.xform(loc, t=(cx,cy,cz))

    def FuncGetCrvVtxPList(self):
        def get_curve_vertex_positions():
            sl_crv = cmds.ls(selection=True)
            #Return Only the first selected crv object.
            if not sl_crv:
                print("Please select a nurbsCurve.")
                return

            A_VertexPos = []
            I_Vertex = cmds.getAttr(sl_crv[0] + '.spans') + cmds.getAttr(sl_crv[0] + '.degree')
            
            for i in range(I_Vertex):
                V3_VertexPos = cmds.pointPosition(sl_crv[0] + '.cv[' + str(i) + ']', world=True)
                A_VertexPos.append(V3_VertexPos)

            return A_VertexPos

        curve_vertex_positions = get_curve_vertex_positions()
        #print every vertexPos per line, thus increasing readablity.
        for i in curve_vertex_positions:
            print(i)
 
    def FuncCreate_CVsoftCluster(self):
        def softSelection():
            selection = om.MSelectionList()
            softSelection = om.MRichSelection()
            om.MGlobal.getRichSelection(softSelection)
            softSelection.getSelection(selection)
            
            dagPath = om.MDagPath()
            component = om.MObject()
            
            iter = om.MItSelectionList( selection,om.MFn.kCurveCVComponent )
            elements = []
            while not iter.isDone(): 
                iter.getDagPath( dagPath, component )
                dagPath.pop()
                node = dagPath.fullPathName()
                fnComp = om.MFnSingleIndexedComponent(component)   
                        
                for i in range(fnComp.elementCount()):
                    elements.append([node, fnComp.element(i), fnComp.weight(i).influence()] )
                iter.next()
            return elements

        def createSoftCluster():
            softElementData = softSelection()
            selection = ["%s.cv[%d]" % (el[0], el[1])for el in softElementData ] 
            
            cmds.select(selection, r=True)
            cluster = cmds.cluster(relative=False)
            
            for i in range(len(softElementData)):
                cmds.percent(cluster[0], selection[i], v=softElementData[i][2])
            cmds.select(cluster[1], r=True)
            
        createSoftCluster()

    def FuncCreate_IKFKSwitch(self):
        #select the joints from root to tip(the parts you want to be controled by switch, may not be all)
        #general
        ls_obj=cmds.ls(sl=1)
        ls_fk_obj = []
        for i in range(len(ls_obj)):
            newname=ls_obj[i]+"_FK"
            a = cmds.createNode("joint", n=newname)
            cmds.matchTransform(a, ls_obj[i], piv=0,pos=1,rot=1,scl=0)
            ls_fk_obj.append(newname)
            if i>0:
                cmds.parent(ls_fk_obj[i], ls_fk_obj[i-1])
            cmds.makeIdentity(a, apply=1)
        #fk
        cmds.select(cl=1)
        for i in range(len(ls_obj)):
            cmds.select(ls_fk_obj[i],add=1)
            
        temp = self.FuncCreateFKRing()
        ls_fk_ctl=temp[0]
        ls_fk_cstr=temp[1]
        #ik
        print("ls_fk_ctl",ls_fk_ctl,"ls_fk_cstr", ls_fk_cstr)
        ls_ik_obj = []
        for i in range(len(ls_obj)):
            newname = ls_obj[i]+"_IK"
            a = cmds.createNode("joint", n=newname)
            cmds.matchTransform(a, ls_obj[i], piv=0, pos=1,rot=1,scl=0)
            ls_ik_obj.append(newname)
            if i>0:
                cmds.parent(ls_ik_obj[i], ls_ik_obj[i-1])
            cmds.makeIdentity(a, apply=1)

        
        ik_ikh = cmds.ikHandle(sj=ls_ik_obj[0], ee=ls_ik_obj[-1], sol="ikRPsolver")[0]
        ik_ctl = cmds.circle(n="IK_Ctl"); cmds.matchTransform(ik_ctl, ik_ikh); cmds.parent(ik_ikh, ik_ctl)
        #
        fk_ctl_grp=cmds.group(em=1, n="FK_Ctl_Grp")
        ik_ctl_grp=cmds.group(em=1, n="IK_Ctl_Grp")
        sup_grp = cmds.group(em=1, n="SUP")
        cmds.parent(ls_fk_obj[0], sup_grp);cmds.parent(ls_ik_obj[0], sup_grp)
        cmds.select(cl=1); cmds.select(ls_fk_obj[0],add=1);cmds.select(ls_ik_obj[0],add=1)
        self.FuncCreateGarbage()
        cmds.parent(ls_fk_ctl[0],fk_ctl_grp); cmds.parent(ik_ctl, ik_ctl_grp)
        
        #If Warning: Cannot parent components or objects in the underworld.
        #That's bc the ctrl construction history are not clear in order to further adjustments. dont' care about it
        #create option ctrl.
        cmds.select(cl=1)
        option_ctl = createCtrler_Gear("Option_Ctl"); cmds.select(option_ctl,add=1)
        #Setting
        cmds.addAttr(ln="IKFK_Switch", min=0, max=1, dv=0, k=1,h=0)
        cmds.addAttr(ln="Stretch", at="bool", min=0, max=1, dv=1, k=1,h=0)


        cmds.matchTransform(option_ctl, ls_obj[0],piv=0, scl=0, pos=1, rot=0)
        cmds.parent(fk_ctl_grp,option_ctl);cmds.parent(ik_ctl_grp,option_ctl)
        
        #Create Switch
        nod_rev = cmds.createNode("reverse")
        cmds.connectAttr(option_ctl+".IKFK_Switch", nod_rev+".inputX")
        ls_nod_blendColor=[]; ls_nod_vero=[]
        for i in range(len(ls_obj)):
            iter_nod_bc = cmds.createNode("blendColors")
            ls_nod_blendColor.append(iter_nod_bc)
            iter_nod_vero = cmds.createNode("animBlendNodeAdditiveRotation")
            ls_nod_vero.append(iter_nod_vero)
            cmds.setAttr(iter_nod_vero+".rotationInterpolation", 1)
            
            #connect translate
            cmds.connectAttr(ls_ik_obj[i]+".translate", iter_nod_bc+".color1")
            cmds.connectAttr(ls_fk_obj[i]+".translate", iter_nod_bc+".color2")
            cmds.connectAttr(nod_rev+".outputX", iter_nod_bc+".blender")
            cmds.connectAttr(iter_nod_bc+".output", ls_obj[i]+".translate")
            #connect rotation
            cmds.connectAttr(ls_ik_obj[i]+".rotate", iter_nod_vero+".inputA")
            cmds.connectAttr(ls_fk_obj[i]+".rotate", iter_nod_vero+".inputB")
            cmds.connectAttr(option_ctl+".IKFK_Switch", iter_nod_vero+".weightB")
            cmds.connectAttr(nod_rev+".outputX", iter_nod_vero+".weightA")
            cmds.connectAttr(iter_nod_vero+".output", ls_obj[i]+".rotate")

    #Tab_Animaiton

    def FuncRivet(self):
        # # https://gist.github.com/rjmoggach/a78d428b6d49b2422fad754ee54eec5e
        # #  Copyright (C) 2000-2001 Michael Bazhutkin - Copyright (C) 2000 studio Klassika
        # #  www.geocites.com/bazhutkin
        # #  bazhutkin@mail.ru
        # # 
        # #   Rivet (button) 1.0
        # #   Script File
        # #   MODIFY THIS AT YOUR OWN RISK
        # # 
        # #   Creation Date:  April 13, 2001
        # # 
        # # 
        # #   Description:
        # # 	Use "Rivet" to constrain locator to polygon or NURBS surfaces
        # # 	Select two edges on polygon object
        # # 	or select one point on NURBS surface and call rivet
        # # 	Parent your rivets and buttons to this locator

        # # logic: select 2 edges to create a nurbsLoft namely a surface, then constraint the locator to it using pointOnSurfaceInfo.        
        nameObject = None
        nod_posi = None

        parts = []
        ls_sl_components = cmds.ls(sl=1, fl=1) #fl = flatten. It would output vtx[1:5] instead of vtx[1], vtx[2]....[5] if fl = 0.

        if len(ls_sl_components) > 0:
            if len(ls_sl_components) != 2:
                cmds.error("No two edges selected")
                return 

            # Tokenize the first edge and get object name and edge index
            parts = ls_sl_components[0].split(".")
            nameObject = parts[0]
            edge1 = int(ls_sl_components[0].split("[")[1].replace("]", ""))

            # Tokenize the second edge and get the edge index
            edge2 = int(ls_sl_components[1].split("[")[1].replace("]", ""))

            # Create the nodes
            nod_cfme = cmds.createNode("curveFromMeshEdge", name="rivetCurveFromMeshEdge1")
            # cmds.setAttr(f"{nod_cfme}.ihi", 1)
            cmds.setAttr(f"{nod_cfme}.edgeIndex[0]", edge1)

            nod_cfme2 = cmds.createNode("curveFromMeshEdge", name="rivetCurveFromMeshEdge2")
            # cmds.setAttr(f"{nod_cfme2}.ihi", 1)
            cmds.setAttr(f"{nod_cfme2}.edgeIndex[0]", edge2)

            nod_loft = cmds.createNode("loft", name="rivetLoft1")
            cmds.setAttr(f"{nod_loft}.inputCurve", size=2)
            cmds.setAttr(f"{nod_loft}.uniform", 1)
            cmds.setAttr(f"{nod_loft}.reverseSurfaceNormals", 1)

            nod_posi = cmds.createNode("pointOnSurfaceInfo", name="rivetPointOnSurfaceInfo1")
            cmds.setAttr(f"{nod_posi}.turnOnPercentage", 1)
            cmds.setAttr(f"{nod_posi}.parameterU", 0.5)
            cmds.setAttr(f"{nod_posi}.parameterV", 0.5)

            # Connect attributes
            cmds.connectAttr(f"{nod_loft}.outputSurface", f"{nod_posi}.inputSurface")
            cmds.connectAttr(f"{nod_cfme}.outputCurve", f"{nod_loft}.inputCurve[0]")
            cmds.connectAttr(f"{nod_cfme2}.outputCurve", f"{nod_loft}.inputCurve[1]")
            cmds.connectAttr(f"{nameObject}.worldMesh", f"{nod_cfme}.inputMesh")
            cmds.connectAttr(f"{nameObject}.worldMesh", f"{nod_cfme2}.inputMesh")

        else:
            list_surface = cmds.ls(selection=True, fl=True)
            size = len(list_surface)

            if size > 0:
                if size != 1:
                    cmds.error("No one point selected")
                    return ""

                # Tokenize and retrieve object and UV coordinates
                parts = list_surface[0].split(".")
                nameObject = parts[0]
                u = float(parts[1].split("[")[1].split("]")[0])
                v = float(parts[2].split("[")[1].split("]")[0])

                nod_posi = cmds.createNode("pointOnSurfaceInfo", name="rivetPointOnSurfaceInfo1")
                cmds.setAttr(f"{nod_posi}.turnOnPercentage", 0)
                cmds.setAttr(f"{nod_posi}.parameterU", u)
                cmds.setAttr(f"{nod_posi}.parameterV", v)

                cmds.connectAttr(f"{nameObject}.ws", f"{nod_posi}.is")

            else:
                cmds.error("No edges or point selected")
                return ""

        # Create the locator and aim constraint
        loc_trg = cmds.createNode("transform", name="rivet1")
        locShape_trg = cmds.createNode("locator", name=f"{loc_trg}Shape", parent=loc_trg)

        nameAC = cmds.createNode("aimConstraint", parent=loc_trg, name=f"{loc_trg}_rivetAimConstraint1")
        cmds.setAttr(f"{nameAC}.target[0].targetWeight", 1)
        cmds.setAttr(f"{nameAC}.aimVector", 0, 1, 0, type="double3")
        cmds.setAttr(f"{nameAC}.upVector", 0, 0, 1, type="double3")

        # Connect the locator attributes
        cmds.connectAttr(f"{nod_posi}.position", f"{loc_trg}.translate")
        cmds.connectAttr(f"{nod_posi}.normal", f"{nameAC}.target[0].targetTranslate")
        cmds.connectAttr(f"{nod_posi}.tangentV", f"{nameAC}.worldUpVector")
        cmds.connectAttr(f"{nameAC}.constraintRotateX", f"{loc_trg}.rotateX")
        cmds.connectAttr(f"{nameAC}.constraintRotateY", f"{loc_trg}.rotateY")
        cmds.connectAttr(f"{nameAC}.constraintRotateZ", f"{loc_trg}.rotateZ")

        
        

        if (self.ui.QCBrivetMoTrail.checkState() == Qt.Checked):
            mtShape = cmds.createNode("motionTrailShape", n = "testMoTrailShape")
            mtSelf = cmds.createNode("motionTrail", n = "testMoTrail")
            mtXform = cmds.listRelatives(mtShape, p=1)[0]

            cmds.connectAttr(f"{mtSelf}.extraKeyframeTimes", f"{mtShape}.extraKeyframeTimes")
            cmds.connectAttr(f"{mtSelf}.frames", f"{mtShape}.frames")
            cmds.connectAttr(f"{mtSelf}.increment", f"{mtShape}.increment")
            cmds.connectAttr(f"{mtSelf}.keyframeFlags", f"{mtShape}.keyframeFlags")
            cmds.connectAttr(f"{mtSelf}.keyframeTimes", f"{mtShape}.keyframeTimes")
            cmds.connectAttr(f"{mtSelf}.points", f"{mtShape}.points")
            cmds.connectAttr(f"{mtSelf}.startTime", f"{mtShape}.startTime")
            cmds.connectAttr(f"{mtSelf}.localPosition", f"{mtShape}.localPosition")

            cmds.connectAttr(f"{loc_trg}.message", f"{mtShape}.transformToMove")
            cmds.connectAttr(f"{loc_trg}.worldMatrix", f"{mtSelf}.inputMatrix")
            cmds.connectAttr(f"{locShape_trg}.localPosition", f"{mtSelf}.localPosition")
            cmds.setAttr(f"{mtSelf}.startTime", cmds.playbackOptions(q=1, minTime=1))
            cmds.setAttr(f"{mtSelf}.endTime", cmds.playbackOptions(q=1, maxTime=1))
        
        # Select the locator
        cmds.select(loc_trg)

        #if self.ui.QCBrivetMoTrail.checked
        return loc_trg

    def FuncScreenSpaceMoTrail(self):
        def get_active_cam():
            #https://forums.autodesk.com/t5/maya-programming/query-currently-active-viewport-camera/td-p/8814385 
            #i prefer to be conservative on this code. usually the last cam is the one u set active.
            for i in cmds.getPanel(type="modelPanel"):
                cam=cmds.modelEditor(i,q=1,av=1,cam=1)
                cam = cam.split(r"|")[1]
            return cam

        def get_pos(input_obj):
            pos = cmds.xform(input_obj, q=1, ws=1, t=1)
            return om.MVector(pos)
        
        def get_plane_normal(input_plane):
            mx_plane = cmds.xform(input_plane, q=1, m=1, ws=1)            
            return om.MVector(mx_plane[8], mx_plane[9], mx_plane[10])
        
        def ray_plane_intersect(pos_loc, pos_cam, pos_plane, normal_plane):
            vec_cam_n_loc = pos_loc - pos_cam
            vec_cam_n_loc.normalize()
            vec_cam_n_plane = pos_plane - pos_cam
            dotProd_cam_loc___cam_plane = vec_cam_n_loc * vec_cam_n_plane
            if dotProd_cam_loc___cam_plane < 1e-6:
                return

            aa = vec_cam_n_plane / dotProd_cam_loc___cam_plane #dist between cam & plane / cos == 
            bb = aa * vec_cam_n_loc #dist between cam & intersect point
            res = pos_cam + bb * (vec_cam_n_loc)
            return res
        
        f_default_plane_dist = -10
        trg_obj = cmds.ls(sl=1)[0]
        if not trg_obj: 
            print("plz select 1 obj")
            return
        cam_active = get_active_cam()
        nod_plane = cmds.polyPlane(ax=[0,0,1], ch=0, sh=1, sw=1)[0]
        print(trg_obj, cam_active, nod_plane)
        cmds.parent(nod_plane, cam_active)
        self.RealRestTransform(nod_plane)
        cmds.setAttr(f"{nod_plane}.translateZ", f_default_plane_dist)
        
        pos_trg_obj = get_pos(trg_obj)
        pos_cam_active = get_pos(cam_active)
        pos_nod_plane = get_pos(nod_plane)
        n_plane = get_plane_normal(nod_plane)
        pos_intersect_point  = ray_plane_intersect(pos_trg_obj, pos_cam_active, pos_nod_plane, n_plane)
        
        #run timeline
        f_startframe, f_endframe = cmds.playbackOptions(q=1, min=1), cmds.playbackOptions(q=1, max=1)
        where_was_i = cmds.currentTime(q=1)
        ls_res_world_pos = []
        ls_loc_trg = []
        for i in range(int(f_startframe), int(f_endframe)+1):
            cmds.currentTime(i)
            pos_trg_obj = get_pos(trg_obj)
            pos_cam_active = get_pos(cam_active)
            pos_nod_plane = get_pos(nod_plane)
            n_plane = get_plane_normal(nod_plane)
            pos_intersect_point  = ray_plane_intersect(pos_trg_obj, pos_cam_active, pos_nod_plane, n_plane)
            ls_res_world_pos.append(pos_intersect_point)
            loc_trg = cmds.createNode("transform", name="shitt"+str(i))
            locShape_trg = cmds.createNode("locator", name=f"{loc_trg}Shape", parent=loc_trg)
            ls_loc_trg.append(loc_trg)
            cmds.xform(loc_trg, t=pos_intersect_point)
            cmds.parent(loc_trg, cam_active)
        #tried on calc matrix to do it, failed.
        cmds.currentTime(where_was_i)
        ls_loc_trg_pos = []
        for i in range(len(ls_loc_trg)):
            a = cmds.xform(ls_loc_trg[i], q=1, ws=1, t=1)
            ls_loc_trg_pos.append(a)
        crv_screenSpace_MoTrail = cmds.curve(d=1, p=ls_loc_trg_pos, n="ScreenSpaceMoTrail", ws=1)
        crvShape_screenSpace_MoTrail = cmds.listRelatives(crv_screenSpace_MoTrail, f=1, s=1)[0]
        cmds.setAttr(f"{crvShape_screenSpace_MoTrail}.dispCV", 1)
        cmds.setAttr(f"{crvShape_screenSpace_MoTrail}.overrideEnabled", 1)
        cmds.setAttr(f"{crvShape_screenSpace_MoTrail}.overrideColor", 14)
        cmds.parent(crv_screenSpace_MoTrail, cam_active)
        cmds.delete(nod_plane, ls_loc_trg)


    def FuncslAllCtrlWithKeys(self):
        pass

        


        




    def FuncCreate_JointChain(self):
        count = self.ui.QLEJointChain.text()  # Amount of joints to create.
        count = int(count)
        if count<3:
            print("Input must be larger than 3")
            one = cmds.ls(sl=1)[0]
            two = cmds.ls(sl=1)[1]
            jnt1 = cmds.createNode("joint")
            jnt2 = cmds.createNode("joint")
            cmds.matchTransform(jnt1, one)
            cmds.matchTransform(jnt2, two)
            cmds.parent(jnt1, jnt2)

            return
        
        a = cmds.ls(sl=1)
        start = a[0]  # Change to object to start from.
        end = a[1]  # Chagne to object to end to.

        steps = 1.0 / (count - 1)  # Will use count to calculate how much it should increase percentage by each iteration. Need to do -1 so the joints reach both start and end points.
        perc = 0  # This will always go between a range of 0.0 - 1.0, and we'll use this in the constraint's weights.
        Zero = "0"
        MaxZero = math.floor(math.log10(count))+1
        ls=[]
        for i in range(count):
            jnt = cmds.createNode("joint")  # Create a new joint.
            Increment=i+1
            ZeroDigits=MaxZero-math.floor(math.log10(Increment))
            Zero_Apply=""
            for j in range(ZeroDigits):
                Zero_Apply = Zero_Apply + Zero
            recIncrement = Zero_Apply + str(Increment)
            #newname = "Bendy" + recIncrement
            #cmds.rename(jnt, newname)
            #cmds.setAttr(jnt + ".displayLocalAxis", False)  # Display its orientation.
            ls.append(jnt)
            constraint = cmds.parentConstraint(start, jnt, weight=1.0 - perc)[0]  # Apply 1st constraint, with inverse of current percentage.
            cmds.parentConstraint(end, jnt, weight=perc)  # Apply 2nd constraint, with current percentage as-is.
            cmds.delete(constraint)  # Don't need this anymore.
            perc += steps  # Increase percentage for next iteration.
        ls.reverse()
        for i in range(count-1):
            cmds.parent(ls[i], ls[i+1])
if __name__ == '__main__':
    Win_JoleneToolbox = cls_Window()
    Win_JoleneToolbox.show(dockable=True)
