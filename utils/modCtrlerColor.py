import maya.cmds as cmds

def modCtrlerColor_ReturnColor(self):
    Ls_sl_obj = cmds.ls(selection=True)
    for i in range(len(Ls_sl_obj)):
        cmds.setAttr(Ls_sl_obj[i]  + '.overrideColor', 0)
        cmds.setAttr(Ls_sl_obj[i]  + '.overrideEnabled', 0)

def modCtrlerColor_TurnYellow(self):
    Ls_sl_obj = cmds.ls(selection=True)
    for i in range(len(Ls_sl_obj)):
        cmds.setAttr(Ls_sl_obj[i] +  '.overrideEnabled', 1)
        cmds.setAttr(Ls_sl_obj[i] +  '.overrideColor', 17)

def modCtrlerColor_TurnRed(self):
    Ls_sl_obj = cmds.ls(selection=True)
    for i in range(len(Ls_sl_obj)):
        cmds.setAttr(Ls_sl_obj[i] + '.overrideEnabled', 1)
        cmds.setAttr(Ls_sl_obj[i] + '.overrideColor', 13)

def modCtrlerColor_TurnBlue(self):
    Ls_sl_obj = cmds.ls(selection=True)
    for i in range(len(Ls_sl_obj)):
        cmds.setAttr(Ls_sl_obj[i] + '.overrideEnabled', 1)
        cmds.setAttr(Ls_sl_obj[i] + '.overrideColor', 6)
