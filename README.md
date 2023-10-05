# MayaToolbox
For CA 2023 only.

This script is intended to solve annoying Maya problems. The reason why not a plugin is because admin is needed to install a plugin in lab.
Python 3.0+ based.

# HOW TO USE THIS
![image](https://github.com/joleeene/MayaToolbox/assets/52316301/d53fe32c-e2e4-43bf-87b0-02e8c1a52886)
Hit it, and you should see the codes.

![image](https://github.com/joleeene/MayaToolbox/assets/52316301/fabb0371-2404-4fe9-bbe7-403a5f5ff8e2)
Hit this Copy button and head back to Maya.

![image](https://github.com/joleeene/MayaToolbox/assets/52316301/5a85a54c-e0c6-4a7c-89a6-bcf863de5aef)
Press Ctrl+F and search for "Script Editor" at Maya 2023+, else you gotta look for where it is:D(I don't have search bar in my 2022-)
Paste it here and run, and remember to save this file somewhere in your storage. If updates, you can repeat the steps to acquire the new versions.


# HOW TO USE NAMING

1. Select all nodes you want.
2. Input the STRING into the frame box.
3. Hit EXECUTE.

CAUTIONS:
1. DO NOT use fancy string as the first character of a name, including numbers. Like this "1_ObjectCube", is not gonna work. The same rule in naming a var.

ISSUES:
There is a annoying problem:     
     Maya don't seem to allow 2 or more nodes sharing a completely same name. If you have those, and selected them, the Naming tool will effect weirdly. Because "ls -sl" or "cmds.ls(selection = True)" will return the absolute paths of nodes, like this "|Grp1 |Grp2 |Object1", which is annoying. And it is not fixable, for me, for now.
