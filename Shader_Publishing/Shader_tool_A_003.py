import maya.cmds as cmds

cmds.window(title='HT shader tool', widthHeight=(500, 700) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

child1 = cmds.rowColumnLayout(numberOfColumns=2)



cmds.setParent( '..' )




child2 = cmds.rowColumnLayout(numberOfColumns=2)
op = cmds.optionMenu( label=('Path'), cc = "change_desk()")
cmds.menuItem(label = "C:/", parent = op)
cmds.menuItem(label = "D:/", parent = op)
cmds.menuItem(label = "E:/", parent = op)
pathText = cmds.text( label = 'CurrentPath: C:/')
dirList = cmds.textScrollList(numberOfRows = 35, append = os.listdir("C:/"), dcc = 'add_path()')
pathText = cmds.text( label = 'CurrentPath: C:/')
cmds.button( label = ('Import shader'))
cmds.setParent( '..' )

child3 = cmds.rowColumnLayout(numberOfColumns=2)
myShader = cmds.shadingNode('anisotropic', asShader=True)


def Connect():

    cmds.rowLayout("obj,shd",nc=2,w=400,h=600)
    cmds.columnLayout( adj=True, columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
    cmds.textScrollList('obj')
    cmds.textScrollList('shd')  
    cmds.textFieldButtonGrp('obj',bl='Select Geometry', text='Select Geometry',ed=False, bc='selMultipleObjects()')
    cmds.textFieldButtonGrp('shd',bl='Select Shaders', text='Select Shaders',ed=False, bc='shadeGrps()')
    cmds.button('Connect()',l='Connect')

Connect()

def selObjName():
    sel=cmds.ls(sl=True)[0]
    cmds.textFieldButtonGrp('obj',e=True,text=sel)
    
    
def selMultipleObjects():
    sel=cmds.ls(sl=True)
    cmds.textScrollList('obj',e=True,ra=True)
    cmds.textScrollList('obj',e=True,numberOfRows=len(sel)+10, allowMultiSelection=True,
			append=sel)

def shadeGrps():			
    Shader=cmds.ls(mat=True)
    cmds.textScrollList('shd',e=True,ra=True)
    cmds.textScrollList('shd',e=True,numberOfRows=10,append=Shader)

def Connect():
    cmds.shadingConnection( 'shd', e=True, cs=0 )
    cmds.shadingConnection( 'obj', q=True, cs=True )


cmds.setParent( '..' )








cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Publish shaders'), (child2, 'Import shaders'), (child3, 'Connect')) )



cmds.showWindow()