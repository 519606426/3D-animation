import maya.cmds as cmds
def GUI():
    winName="ShaderTool"

    if ( cmds.window(winName,exists=True)):
        cmds.deleteUI(winName)
    
    cmds.window(winName,title='Shader publishing',w=400,h=600)
    cmds.window(winName,q=True,wh=True)
  
    cmds.rowLayout("obj,shd",nc=2,w=200,h=200)
    cmds.columnLayout( adj=True, columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
    cmds.textScrollList('obj')
    cmds.textScrollList('shd')  
    cmds.textFieldButtonGrp('obj',bl='Import Object', text='Select Object',ed=False, bc='selMultipleObjects()')
    cmds.textFieldButtonGrp('shd',bl='Select Shader', text='Select Shader',ed=False, bc='shadeGrps()')
    cmds.button('Connect()',l='Connect')
    cmds.showWindow()

GUI()

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
    
    
    
cmds.columnLayout(adjustableColumn=True)

cmds.text(label="Shader Publishing", fn="boldLabelFont")
cmds.text(" ")
cmds.button(label="Publish shader")
cmds.button(label="save the slected object")
cmds.text(" ")
cmds.text(" ")

cmds.text(label="Selected File Publishing")

