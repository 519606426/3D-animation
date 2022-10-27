import maya.cmds as cmds
import json

cmds.window(title='HT shader tool', widthHeight=(500, 700) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

child1 = cmds.rowColumnLayout(numberOfColumns=1)
cmds.swatchDisplayPort('slPP', wh=(60, 60), sn=myShader)
cmds.textFieldButtonGrp( label='Shader Name', text='name', buttonLabel='Set', bc='set()')

newNode = cmds.shadingNode( 'blinn', asShader=True )
newNodeAttr = newNode + '.normalCamera'
cmds.attrColorSliderGrp( label='Color', rgb=(1, 0, 0), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Transparency', rgb=(1, 0, 0), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Ambient color', rgb=(2, 4, 123), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Incandescence', rgb=(2, 4, 123), at=newNodeAttr)



cmds.textFieldGrp( label='Publish shader', text='Text' )
cmds.button( label = ('Publish shader'),c = 'filePublish()')

cmds.text( label='Version' )
cmds.button( label = "Select Path",c = 'filePublish()')
dirList = cmds.textScrollList(numberOfRows = 15, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders"))




def set():
    
 basicFilter = "*.json"
 cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2,cap='fileImport',okc='Publish',cc='Cancel')


def filePublish():
    
 basicFilter = "*.json"
 cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2,cap='fileImport',okc='Publish',cc='Cancel')


cmds.setParent( '..' )




child2 = cmds.rowColumnLayout(numberOfColumns=1)
op = cmds.optionMenu( label=('Path'), cc = "change_desk()")
cmds.menuItem(label = "C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders", parent = op)
dirList = cmds.textScrollList(numberOfRows = 35, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders"))
cmds.button( label = ('Storing shader'),c = 'fileImport()')


def fileImport():
    
 basicFilter = "*.json"
 cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2,cap='fileImport',okc='Storing',cc='Cancel')

def change_disk():
    global CurrentDir
    local_desk = cmds.optionMenu(op, v=True, q=True) #获取下拉菜单标签内容
    desk_list = os.listdir(local_desk) #查询磁盘下所有的文件与文件夹
    CurrentDir = local_desk #将当前磁盘路径赋予变量
    cmds.text(pathText, e=True, label= "CurrentPath: " + CurrentDir) #将当前路径标签修改为此时路径
    cmds.textScrollList(dirList, e=True, removeAll=True) #移除旧文件列表
    cmds.textScrollList(dirList, e=True, append=desk_list) #

cmds.setParent( '..' )

child3 = cmds.rowColumnLayout(numberOfColumns=1)
myShader = cmds.shadingNode('anisotropic', asShader=True)


def Assign():

    cmds.rowLayout("obj,shd",nc=2,w=400,h=600)
    cmds.columnLayout( adj=True, columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
    cmds.textScrollList('obj')
    cmds.textScrollList('shd')  
    cmds.textFieldButtonGrp('obj',bl='Import Object', text='Select Object',ed=False, bc='selObjects()')
    cmds.textFieldButtonGrp('shd',bl='Import Shaders', text='Import Shaders',ed=False, bc='shadeGrps()')
    cmds.button('Assign()',l='Assign')

Assign()

    
def selObjects():
    sel=cmds.ls(sl=True)
    cmds.textScrollList('obj',e=True,ra=True)
    cmds.textScrollList('obj',e=True,numberOfRows=len(sel)+10, allowMultiSelection=True,append=sel)

def shadeGrps():			
    Shader=cmds.ls(mat=True)
    cmds.textScrollList('shd',e=True,ra=True)
    cmds.textScrollList('shd',e=True,numberOfRows=10,append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shaders"))

def Assign():
    cmds.shadingConnection( 'shd', e=True, cs=0 )
    cmds.shadingConnection( 'obj', q=True, cs=True )

cmds.setParent( '..' )




cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Publish shaders'), (child2, 'Storing/Recording'), (child3, 'Load/Assign')) )



cmds.showWindow()