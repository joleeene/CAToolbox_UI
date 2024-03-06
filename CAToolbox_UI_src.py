#General Import
import math, copy, re
import PySide2 as p2
import maya.OpenMayaUI as omui
import maya.OpenMaya as om
import shiboken2
import maya.cmds as cmds
from PySide2 import QtGui, QtCore
from PySide2.QtCore import QFile
from maya.app.general.mayaMixin import MayaQWidgetDockableMixin
from PySide2.QtUiTools import QUiLoader  # Import QUiLoader

path = r"C:\Users\JoleneLinxy\OneDrive\OrganizeFilesStructure\08_Environment\Config\Maya\script\CAToolbox_UI"
def PathRectifier(Input_Str):
    return Input_Str.replace("\\", "/")
rec_path = PathRectifier(path)
import sys
sys.path.append(rec_path)
import importlib
#Utils files import
import utils
from utils.utilsTest import *
from utils.createCtrler import *
from utils.modCtrlerColor import *
from utils.CreateIK import *



def mayaMainWindow():
    mainWindowPointer = omui.MQtUtil.mainWindow()
    return shiboken2.wrapInstance(int(mainWindowPointer), p2.QtWidgets.QWidget)

class ClickableLabel(p2.QtWidgets.QLabel):
    clicked = QtCore.Signal()
    def mousePressEvent(self, event):
        self.clicked.emit()

class cls_Window(MayaQWidgetDockableMixin, p2.QtWidgets.QDialog):
    def __init__(self, parent=mayaMainWindow()):
        super(cls_Window, self).__init__(parent)
        #--------------Config. This is mine. You need to change this path to your own.
        self.setWindowTitle("CA2023 Toolbox")
        self.resize(400, 550)
        
        file_path = rec_path+"/ui/CAToolbox_UI.ui"
        ##################################################################################
        ui_loader = QUiLoader()
        ui_file = QFile(file_path)
        self.ui = ui_loader.load(ui_file)
        ########################################## Must do or else it's a seperated window.
        layout = p2.QtWidgets.QVBoxLayout(self)
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

        #Tab_Naming
        self.ui.QPBPrefixExe.clicked.connect(self.FuncExePrefix)
        self.ui.QPBSuffixExe.clicked.connect(self.FuncExeSuffix)
        self.ui.QPBReplaceExe.clicked.connect(self.FuncExeReplace)
        self.ui.QPBWholeExe.clicked.connect(self.FuncExeWhole)

        #Tab_Rigging
        self.ui.QPBCtrlerCube.clicked.connect(createCtrler_Cube)
        self.ui.QPBCtrlerSphere.clicked.connect(createCtrler_Sphere)
        self.ui.QPBCtrlerPrism.clicked.connect(createCtrler_Prism)
        self.ui.QPBCtrlerRing.clicked.connect(createCtrler_Ring)
        self.ui.QPBCtrlerRotPike.clicked.connect(createCtrler_RotPike)
        self.ui.QPBCtrlerRot1Dir.clicked.connect(createCtrler_Rot1Dir)
        self.ui.QPBCtrlerTran1Dir.clicked.connect(createCtrler_Tran1Dir)
        self.ui.QPBCtrlerGear.clicked.connect(createCtrler_Gear)
        self.ui.QPBCtrlerTransCube.clicked.connect(createCtrler_TransCube)
        self.ui.QPBCtrler4DirCirc.clicked.connect(createCtrler_4DirCirc)

        self.ui.QPBColorReturn.clicked.connect(modCtrlerColor_ReturnColor)
        self.ui.QPBColorYellow.clicked.connect(modCtrlerColor_TurnYellow)
        self.ui.QPBColorRed.clicked.connect(modCtrlerColor_TurnRed)
        self.ui.QPBColorBlue.clicked.connect(modCtrlerColor_TurnBlue)

        self.ui.QPBJointSizeExe.clicked.connect(self.FuncExeJointSize)

        self.ui.QPBCreateFKRing.clicked.connect(self.FuncCreateFKRing)
        self.ui.QPBCreateIK.clicked.connect(self.createIK_CreateIK)
        self.ui.QPBCreateLoc.clicked.connect(self.FuncCreateLoc)
        self.ui.QPBGetCrvVtxPList.clicked.connect(self.FuncGetCrvVtxPList)
        self.ui.QPBCVsoftCluster.clicked.connect(self.FuncCreate_CVsoftCluster)
        
        self.ui.QPBJointChain.clicked.connect(self.FuncCreate_JointChain)



        ###
        self.ui.show()  
    ###Func
    def test(self):
        print("VVVVVVVV")
    #Tab_General
    def FuncTest(self):
        selected_nodes = cmds.ls(selection=True, long=False)
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
        for i in range(len(sl_objs)):
            null_object = cmds.group(empty=True, name=sl_objs[i]+"_Off")
            cmds.xform(null_object, worldSpace=True, matrix = world_transform_pool[i])
            # Parent the original object under the null object
            cmds.parent(sl_objs[i], null_object)
        # Reparent the original object to its original parent
            if original_parent_pool[i]:
                cmds.parent(null_object, original_parent_pool[i])

    #Tab_Naming

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
 
    #Tab_Rigging
                
    def FuncExeJointSize(self):
        sl_objs = cmds.ls(selection=True)
        for i in range(len(sl_objs)):
            cmds.setAttr(sl_objs[i]+".radius", float(self.ui.QLEJointSize.text()))

    def FuncCreateFKRing(self):
        #Simple ver FK Ring
        Ls_Ctl = []
        def subFuncCreateFKRing(Arg_t, Arg_ro, Arg_s, Arg_name):
            VertexAmount = 36
            VertexPos = (0,0,0); RingPathing = []
            for i in range(VertexAmount):
                recAngle = math.radians((i/VertexAmount)*360)
                VertexPos = (math.cos(recAngle), 0, math.sin(recAngle))
                RingPathing.append(VertexPos)
            RingPathing.append(RingPathing[0])
            Incoming_Name = Arg_name + "_Ctl"
            a = cmds.curve(d=1, p=RingPathing, name = Incoming_Name)
            cmds.xform(a, t=Arg_t ,ro=Arg_ro, s=Arg_s, worldSpace=True)
            Ls_Ctl.append(Incoming_Name)
            return a

        Ls_sl_objs = cmds.ls(sl=True)

        #Create FK Ring
        for ord in range(len(Ls_sl_objs)):
            sl_obj_wm = cmds.xform(Ls_sl_objs[ord], query=True, matrix=True, worldSpace=True)
            sl_obj_t = [sl_obj_wm[12], sl_obj_wm[13], sl_obj_wm[14]]
            sl_obj_ro = cmds.xform(Ls_sl_objs[ord], query=True, rotation=True, worldSpace=True)
            sl_obj_s = cmds.xform(Ls_sl_objs[ord], query=True, scale=True, worldSpace=True)
            a = subFuncCreateFKRing(sl_obj_t, sl_obj_ro, sl_obj_s, Ls_sl_objs[ord])
        for ord in range(len(Ls_Ctl)):
            if ord+2 <= len(Ls_Ctl):
                cmds.parent(Ls_Ctl[-(ord+1)], Ls_Ctl[-(ord+2)])
            else:
                continue

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

    def createIK_CreateIK(self):#Main
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

    def FuncCreate_JointChain(self):
        count = self.ui.QLEJointChain.text()  # Amount of joints to create.
        count = int(count)
        if count<3:
            print("Input must be larger than 3")
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
            newname = "Bendy" + recIncrement
            cmds.rename(jnt, newname)
            #cmds.setAttr(jnt + ".displayLocalAxis", False)  # Display its orientation.
            ls.append(newname)
            constraint = cmds.parentConstraint(start, newname, weight=1.0 - perc)[0]  # Apply 1st constraint, with inverse of current percentage.
            cmds.parentConstraint(end, newname, weight=perc)  # Apply 2nd constraint, with current percentage as-is.
            cmds.delete(constraint)  # Don't need this anymore.
            perc += steps  # Increase percentage for next iteration.
        ls.reverse()
        for i in range(count-1):
            cmds.parent(ls[i], ls[i+1])
if __name__ == '__main__':
    Win_JoleneToolbox = cls_Window()
    Win_JoleneToolbox.show(dockable=True)
