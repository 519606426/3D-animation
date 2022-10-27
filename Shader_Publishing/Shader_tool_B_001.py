import maya.cmds as cmds

cmds.window(title='My shader tool', widthHeight=(500, 700) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

child1 = cmds.rowColumnLayout(numberOfColumns=2)

cmds.textFieldButtonGrp( label='Shader01', text='name', buttonLabel='Set' )
cmds.swatchDisplayPort('slPP', wh=(60, 60), sn=myShader)
objName = cmds.shadingNode('phong', asShader=True)
cmds.attrColorSliderGrp( at='%s.color' % objName )
cmds.colorSliderGrp( label='Label', rgb=(1, 0, 0) )
cmds.colorSliderGrp( label='Label', rgb=(1, 0, 0) )
cmds.attrColorSliderGrp( at='%s.color' % objName )



cmds.textFieldButtonGrp( label='Publish shader', text='Text', buttonLabel='open file' )



cmds.setParent( '..' )




child2 = cmds.rowColumnLayout(numberOfColumns=2)
op = cmds.optionMenu( label=('Path'), cc = "change_desk()")
cmds.menuItem(label = "C:/", parent = op)
Text = cmds.text( label = 'CurrentPath: C:/')
dirList = cmds.textScrollList(numberOfRows = 35, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders"), dcc = 'add_path()')
Text = cmds.text( label = 'CurrentPath: C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scripts/Shaders')
cmds.button( label = ('Publish shader'),c = 'fileBatchImport()')








cmds.setParent( '..' )

child3 = cmds.rowColumnLayout(numberOfColumns=2)
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

def selObjName():
    sel=cmds.ls(sl=True)[0]
    cmds.textFieldButtonGrp('obj',e=True,text=sel)
    
    
def selObjects():
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