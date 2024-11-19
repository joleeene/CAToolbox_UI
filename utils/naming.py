import math, copy, re
import maya.cmds as cmds
import maya.api.OpenMaya as om

class naming():
    def __init__(self, input_ui) -> None:
        self.ui = input_ui
        self.ls_sl_obj=cmds.ls(sl=1)
        pass

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
        print("ss")
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
