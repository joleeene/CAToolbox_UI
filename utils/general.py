import math, copy, re
import maya.cmds as cmds
import maya.api.OpenMaya as om

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


