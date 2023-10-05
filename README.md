# MayaToolbox
For CA 2023 only.

This script is intended to solve annoying Maya problems. The reason why not a plugin is because admin is needed to install a plugin in lab.
Python 3.0+ based.

# HOW TO USE NAMING

1. Select all nodes you want.
2. Input the STRING into the frame box.
3. Hit EXECUTE.

CAUTIONS:
1. DO NOT use fancy string as the first character of a name, including numbers. Like this "1_ObjectCube", is not gonna work. The same rule in naming a var.

ISSUES:
There is a annoying problem:     
     Maya don't seem to allow 2 or more nodes sharing a completely same name. If you have those, and selected them, the Naming tool will effect weirdly. Because "ls -sl" or "cmds.ls(selection = True)" will return the absolute paths of nodes, like this "|Grp1 |Grp2 |Object1", which is annoying. And it is not fixable, for me, for now.
