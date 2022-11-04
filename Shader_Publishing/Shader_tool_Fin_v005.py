import maya.cmds as cmds
import json
import os

cmds.window(title='HT shader tool', widthHeight=(500, 700) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )

child1 = cmds.rowColumnLayout(numberOfColumns=1)
myShader = cmds.shadingNode('anisotropic', asShader=True)
cmds.swatchDisplayPort('slPP', wh=(60, 60), sn=myShader)

newNode = cmds.shadingNode( 'blinn', asShader=True )
newNodeAttr = newNode + '.normalCamera'
cmds.attrColorSliderGrp( label='Color', rgb=(1, 0, 0), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Transparency', rgb=(1, 0, 0), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Ambient color', rgb=(2, 4, 123), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Incandescence', rgb=(2, 4, 123), at=newNodeAttr)

txt_field = cmds.textField('txtName')
cmds.button(label='Rename', width=300, c=renameObject)

cmds.textField("FilePath", text="", pht="No Folder Selected...", ed=True, dif=True, editable=True, bgc=[0.3, 0.3, 0.3], h=24)
cmds.rowColumnLayout (numberOfColumns = 4, columnWidth = ( [1,200], [2,56], [3,32],[4,32] ) )
cmds.button( label="Publish",c=ExportFile, ann="Publish Selected Shader")
cmds.optionMenu ("fileTypeOM",height=24 )
cmds.menuItem("fbxMI", label='FBX' )
cmds.menuItem("objMI", label='OBJ' )
cmds.iconTextButton( style='iconOnly', h=24, image1="folder-new.png", c=GetPath, ann="Select folder for publishing" )
cmds.iconTextButton( style='iconOnly', h=24, image1="folder-open.png", c=ShowPath, ann="Show selected folder" )
cmds.setParent("..")


cmds.text( label='Version' )
cmds.button( label = "Select Path",c = 'FileImport()')
dirList = cmds.textScrollList(numberOfRows = 15, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shader_Geo_group"))

def renameObject(*args):
    a = cmds.ls(sl=True)
    txt = cmds.textField(txt_field , q=True, tx=True)
    
    cmds.rename(a[0], txt)
    cmds.confirmDialog(icn='information', message='Done!')
    cmds.showWindow()

def GetPath(*args):
    

    getpath = cmds.fileDialog2(fm = 3, okc='Select Folder')
    cmds.textField ("FilePath", e=True, tx=getpath)


def ShowPath(*args):
    

    showpath = cmds.textField ("FilePath", q=True, tx=True)
    if showpath:
        os.startfile(showpath)
    else:
        cmds.confirmDialog(t='Info', icon="information", m='Please select a Folder', button='Ok')


def ExportFile(*args):
      
    fileType = ""
    fileTypeSelected = cmds.optionMenu("fileTypeOM", value=True, q=True)
    
    if fileTypeSelected == "FBX":
        fileType = "FBX export"
    if fileTypeSelected == "OBJ":
        fileType = "OBJexport"

    meshSel = cmds.ls(sl=True)
    for objSel in meshSel:
        
        if objSel:
            path = cmds.textField ("FilePath", q=True, tx=True)
            
            cmds.select(objSel)
            objNames = cmds.ls(sl=True)
            splitName = objNames[0].split('|')
            objName = splitName[-1]
            
            exportPath = path+'/'+objName+'.obj'
            cmds.file (exportPath, es=True, force=True, type=fileType, op="groups=0; ptgroups=0; materials=0; smoothing=1; normals=0")



def FileImport():
	if CheckForBonusTools:
		multipleFilters =  'Files (*.ma *.mb);; Maya binary (*.mb);; Maya Ascii (*.ma)'
	else:
		multipleFilters =  'Files (*.ma *.mb;;Maya binary (*.mb);; Maya Ascii (*.ma)'
	files = cmds.fileDialog2(caption = 'Choose files to import', ds = 2, fileMode = 4, okCaption = 'Import', fileFilter = multipleFilters, hideNameEdit = False)
	
	for x in files:
		if any(y in x for y in ['.ma', '.MA']):
			fileType = 'mayaAscii'
			options = ''
			ImportFiles(fileType, x, options)
			
		if any(y in x for y in ['.mb', '.MB']):
			fileType = 'mayaBinary'
			options = ''
			ImportFiles(fileType, x, options)

def CheckForBonusTools(*args):
	for x in sys.path:
		if 'MayaBonusTools' in x:
			return True
	return False

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
    local_desk = cmds.optionMenu(op, v=True, q=True)
    desk_list = os.listdir(local_desk) 
    CurrentDir = local_desk 
    cmds.text(pathText, e=True, label= "CurrentPath: " + CurrentDir)
    cmds.textScrollList(dirList, e=True, removeAll=True)
    cmds.textScrollList(dirList, e=True, append=desk_list) 

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
    cmds.button(c = 'FileImport()',l='Assign')

Assign()

    
def selObjects():
    sel=cmds.ls(sl=True)
    cmds.textScrollList('obj',e=True,ra=True)
    cmds.textScrollList('obj',e=True,numberOfRows=len(sel)+10, allowMultiSelection=True,append=sel)

def shadeGrps():			
    Shader=cmds.ls(mat=True)
    cmds.textScrollList('shd',e=True,ra=True)
    cmds.textScrollList('shd',e=True,numberOfRows=10,append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shader_Pub"))


    
    
    
    
cmds.setParent( '..' )




cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Publish shaders'), (child2, 'Storing/Recording'), (child3, 'Load/Assign')) )



cmds.showWindow()