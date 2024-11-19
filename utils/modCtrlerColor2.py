import math, copy, re
import maya.cmds as cmds
import maya.api.OpenMaya as om

class modCtrlerColor2():
    def __init__(self):
        pass

    def func_get_shape(self, prm_obj):
        shapes = cmds.listRelatives(prm_obj, shapes=1)
        if shapes:
            return shapes[0] 
        else:
            return None 
    def set_override_color(self, color=None):
        self.ls_sl_obj = cmds.ls(sl=1)
        if not self.ls_sl_obj:
            print("No objects selected.")
            return

        for i in self.ls_sl_obj:
            s = self.func_get_shape(i)
            if color is None:
                # Disable override
                cmds.setAttr(f"{s}.overrideEnabled", 0)
                cmds.setAttr(f"{s}.overrideColor", 0)
            else:
                # Enable overrids and set color
                cmds.setAttr(f"{s}.overrideEnabled", 1)
                cmds.setAttr(f"{s}.overrideColor", color)

    def modCtrlerColor_ReturnColor(self):
        self.set_override_color(None)

    def modCtrlerColor_TurnYellow(self):
        self.set_override_color(17)

    def modCtrlerColor_TurnRed(self):
        self.set_override_color(13)

    def modCtrlerColor_TurnBlue(self):
        self.set_override_color(6)

    def modCtrlerColor_TurnPurple(self):
        self.set_override_color(31)

    def modCtrlerColor_TurnCyan(self):
        self.set_override_color(18)

    def modCtrlerColor_TurnSkin(self):
        self.set_override_color(21)

    def modCtrlerColor_TurnPink(self):
        self.set_override_color(20)