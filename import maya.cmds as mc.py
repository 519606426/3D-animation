import maya.cmds as mc

def addpre(pre):
    sel = mc.ls(sl=1)
    for i in sel:
        mc.rename(i, pre+i)
        


mc.window()
mc.columnLayout()
mc.text(label="Loading the latest version", h=30, fn = "boldLabelFont")


mc.button(label = "layout", w=300, h=50, command="b=mc.textField(a,q=1,tx=1);addpre(b)")
mc.button(label = "animation", w=300, h=50, command="b=mc.textField(a,q=1,tx=1);addpre(b)")
mc.button(label = "lighting", w=300, h=50, command="b=mc.textField(a,q=1,tx=1);addpre(b)")
mc.text(label="Lighting", h=30, fn = "boldLabelFont")

mc.button(label = "lighting_1", w=300, h=20, command="b=mc.textField(a,q=1,tx=1);addpre(b)")
mc.button(label = "lighting_2", w=300, h=20, command="b=mc.textField(a,q=1,tx=1);addpre(b)")
mc.button(label = "lighting_3", w=300, h=20, command="b=mc.textField(a,q=1,tx=1);addpre(b)")

mc.text(label="Setting the value about the lighting", h=30,fn = "boldLabelFont")

mc.text(label="color temperature",fn = "boldLabelFont")
a = mc.textField(tx = "int:", w=300)
mc.text(label="brightness",fn = "boldLabelFont")
a = mc.textField(tx = "int:", w=300)
mc.text(label="color",fn = "boldLabelFont")
a = mc.textField(tx = "int:", w=300)

mc.showWindow()