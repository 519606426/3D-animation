
import maya.cmds as mc
 
mc.window(title =('shader import'),widthHeight=(500, 700))

mc.columnLayout()

op = mc.optionMenu( label=('list'), cc = "change_desk()")

pathText = mc.text( label = 'CurrentPath: C:/')

dirList = mc.textScrollList(numberOfRows = 35, append = os.listdir("C:/"), dcc = 'add_path()')

mc.flowLayout( columnSpacing=10 ,width=200)
 

mc.button( label = ('import all shader'))
mc.button( label = ('import current shader'))
 
mc.showWindow()
