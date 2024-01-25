#Stretch, RevFoot, IKFKSwitch
import maya.cmds as cmds
from .createCtrler import *
String_Warning0 = "Nothing selected"
String_Warning1 = "Not Jnt"
def get_LR_Dir(input_obj): 
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
    elif first_2_characters == "Dir_":#Debug 
        s_LR_Dir = "Dir_"
    else:
        s_LR_Dir = ""
    return s_LR_Dir

def get_sl_obj_and_LR_Dir():
    input_sl_obj = cmds.ls(sl=True)[0]
    if input_sl_obj == None:
        print(String_Warning0)
        return
    Ls_sl_ChildObjs = cmds.listRelatives(input_sl_obj, ad=True)
    Ls_sl_ChildObjs.append(input_sl_obj)
    Ls_BindJnt = Ls_sl_ChildObjs
    Ls_BindJnt.reverse()
    LR_Dir = get_LR_Dir(input_sl_obj) # Pending refactor
    return [Ls_BindJnt, LR_Dir]

def get_IKFKjnt_list_after_dup(input_sl_obj, IKorFK, OriginJointList):
    cmds.duplicate(input_sl_obj, rc=True)
    Ls_JustDupIKFKJntName = []
    suffix = "1"
    Ls_JustDupIKFKJntName = [i + suffix for i in OriginJointList]
    Ls_TrgIKFKJntName = [i + suffix for i in OriginJointList]

    LR_Prefix = "Dir_"
    LR_PrefixPlusIKFK = "Dir_" + IKorFK
    Ls_TrgIKFKJntName = [i.replace(LR_Prefix, LR_PrefixPlusIKFK) for i in Ls_TrgIKFKJntName]
    Ls_TrgIKFKJntName = [i[:-1] for i in Ls_TrgIKFKJntName]

    for i in range(len(Ls_JustDupIKFKJntName)):
        cmds.rename(Ls_JustDupIKFKJntName[i], Ls_TrgIKFKJntName[i])
    return Ls_TrgIKFKJntName

def get_sl_obj_world_PSR(InputJnt):
    InputJntMx = cmds.xform(InputJnt, query=True, matrix=True, worldSpace=True)
    InputJntT = [InputJntMx[12], InputJntMx[13], InputJntMx[14]]
    InputJntRo = cmds.xform(InputJnt, query=True, rotation=True, worldSpace=True)
    InputJntS = cmds.xform(InputJnt, query=True, scale=True, worldSpace=True)
    a = [InputJntT, InputJntRo, InputJntS]
    return a

def createIK_CreateIK():#Main
    #IK Part
    Ls_origin_jnt=get_sl_obj_and_LR_Dir()[0]; LR_Dir=get_sl_obj_and_LR_Dir()[1]
    Ls_IKJnt=get_IKFKjnt_list_after_dup(Ls_origin_jnt,"IK" , Ls_origin_jnt)

    ThighFootIkhNewName = LR_Dir+"ThighFoot_Ikh"
    FootBallIkhNewName = LR_Dir+"FootBall_Ikh"
    BallTipIkhNewName = LR_Dir+"BallTip_Ikh"
    cmds.ikHandle(sj=Ls_IKJnt[0], ee=Ls_IKJnt[2], sol="ikRPsolver", n=ThighFootIkhNewName)
    cmds.ikHandle(sj=Ls_IKJnt[2], ee=Ls_IKJnt[3], sol="ikSCsolver", n=FootBallIkhNewName)
    cmds.ikHandle(sj=Ls_IKJnt[3], ee=Ls_IKJnt[4], sol="ikSCsolver", n=BallTipIkhNewName)

    #Create Ctrler
    IKFootCtrler = createCtrler_Cube()
    IKFootJntWorldPSR = get_sl_obj_world_PSR(Ls_IKJnt[2])
    cmds.xform(IKFootCtrler, t=IKFootJntWorldPSR[0] ,ro=[0,0,0], s=IKFootJntWorldPSR[2], worldSpace=True)
    IKFootCtrlerNewName = LR_Dir+"IKFoot_Ctl"; cmds.rename(IKFootCtrler, IKFootCtrlerNewName)

    IKBallRollCtrlerNewName = LR_Dir+"IKBall_Ctl"
    IKBallRollCtrler = cmds.circle( nr =(0,0,1), c=(0,0,0),r=5, n=IKBallRollCtrlerNewName)
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
    cmds.createNode("distanceBetween", name=IKFootDistBtweenNodeNewName)
    cmds.connectAttr(IKFootDistNewName+".worldMatrix[0]", IKFootDistBtweenNodeNewName+".inMatrix1")
    cmds.connectAttr(IKThighDistNewName+".worldMatrix[0]", IKFootDistBtweenNodeNewName+".inMatrix2")

    MultiDvdCalcRateNodeNewName=LR_Dir+"MultiDvdCalcRate"
    cmds.createNode("multiplyDivide", n=MultiDvdCalcRateNodeNewName)
    MultiDvdApplyRateNodeNewName=LR_Dir+"MultiDvdApplyRate"
    cmds.createNode("multiplyDivide", n=MultiDvdApplyRateNodeNewName)
    cmds.connectAttr(IKFootDistBtweenNodeNewName+".distance", MultiDvdCalcRateNodeNewName+".input1X")
    cmds.setAttr(MultiDvdApplyRateNodeNewName+".input2x", Ls_IKJnt[1]+".translateY")
    cmds.setAttr(MultiDvdApplyRateNodeNewName+".input2y", Ls_IKJnt[2]+".translateY")
    cmds.connectAttr(MultiDvdCalcRateNodeNewName+".output1x", MultiDvdApplyRateNodeNewName+".input1x")
    cmds.connectAttr(MultiDvdCalcRateNodeNewName+".output1x", MultiDvdApplyRateNodeNewName+".input1y")

    ConditionNodeNewName = LR_Dir+"Condi_Nod"
    cmds.createNode("condition", n=ConditionNodeNewName)
    cmds.setAttr(ConditionNodeNewName+".colorIfFalseR", Ls_IKJnt[1]+".translateY")
    cmds.setAttr(ConditionNodeNewName+".colorIfFalseG", Ls_IKJnt[2]+".translateY")
    cmds.setAttr(ConditionNodeNewName+".operation", 2)
    IKThighFootLengthSum = cmds.getAttr(Ls_IKJnt[1]+".translateY") + cmds.getAttr(Ls_IKJnt[2]+".translateY")
    cmds.setAttr(ConditionNodeNewName+".secondTerm", IKThighFootLengthSum)
    cmds.connectAttr(ConditionNodeNewName+".colorIfFalseR", MultiDvdCalcRateNodeNewName+".outputX")
    cmds.connectAttr(ConditionNodeNewName+".colorIfFalseG", MultiDvdCalcRateNodeNewName+".outputY")
    cmds.connectAttr(ConditionNodeNewName+".firstTerm", IKFootDistNewName+".distance")

    cmds.connectAttr(ConditionNodeNewName+".outColorR", Ls_IKJnt[1]+".translateY")
    cmds.connectAttr(ConditionNodeNewName+".outColorG", Ls_IKJnt[2]+".translateY")

def op():
    print("sassssd")