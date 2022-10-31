import maya.cmds as cmds

cmds.window(title='My shader tool', widthHeight=(500, 700) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

child1 = cmds.rowColumnLayout(numberOfColumns=1)
cmds.swatchDisplayPort('slPP', wh=(60, 60), sn=myShader)
cmds.textFieldButtonGrp( label='Shader Name', text='name', buttonLabel='Set' )

cmds.attrColorSliderGrp( at='%s.color' % objName )


cmds.colorSliderGrp( label='Label', rgb=(1, 0, 0) )



cmds.textFieldGrp( label='Publish shader', text='Text' )
cmds.button( label = ('Publish shader'),c = 'fileImport()')



cmds.setParent( '..' )




child2 = cmds.rowColumnLayout(numberOfColumns=1)
op = cmds.optionMenu( label=('Path'), cc = "change_desk()")
cmds.menuItem(label = "C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders", parent = op)
dirList = cmds.textScrollList(numberOfRows = 35, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders"), dcc = 'add_path()')
cmds.button( label = ('Import shader'),c = 'fileImport()')


def fileImport():
    
 basicFilter = "*.json"
 cmds.fileDialog2(fileFilter=basicFilter, dialogStyle=2,cap='fileImport',okc='Select',cc='Cancel')






cmds.setParent( '..' )

child3 = cmds.rowColumnLayout(numberOfColumns=1)
myShader = cmds.shadingNode('anisotropic', asShader=True)


def Connect():

    cmds.rowLayout("obj,shd",nc=2,w=400,h=600)
    cmds.columnLayout( adj=True, columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
    cmds.textScrollList('obj')
    cmds.textScrollList('shd')  
    cmds.textFieldButtonGrp('obj',bl='Import Object', text='Select Object',ed=False, bc='selObjects()')
    cmds.textFieldButtonGrp('shd',bl='Import Shaders', text='Import Shaders',ed=False, bc='shadeGrps()')
    cmds.button('Connect()',l='Connect')

Connect()

    
def selObjects():
    sel=cmds.ls(sl=True)
    cmds.textScrollList('obj',e=True,ra=True)
    cmds.textScrollList('obj',e=True,numberOfRows=len(sel)+10, allowMultiSelection=True,
			append=sel)

def shadeGrps():			
    Shader=cmds.ls(mat=True)
    cmds.textScrollList('shd',e=True,ra=True)
    cmds.textScrollList('shd',e=True,numberOfRows=10,append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders"))

def Connect():
    cmds.shadingConnection( 'shd', e=True, cs=0 )
    cmds.shadingConnection( 'obj', q=True, cs=True )


cmds.setParent( '..' )









cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Publish shaders'), (child2, 'Import shaders'), (child3, 'Connect')) )



cmds.showWindow()