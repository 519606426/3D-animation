
import maya.cmds as cmds
import sys
import os

def buttonFunction(args):

    cmds.polyCube()

def buttonFunction1(args):
    
    #path = 'Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes/'
	#sys.path.append("Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes/")
	multipleFilters =  "All native importable files (*.ma *.mb *.obj *.fbx *.abc);; Maya binary (*.mb);; Maya Ascii 	(*.ma);; Obj (*.obj);; FBX (*.fbx);; Alembic Cache (*.abc)"
	files = cmds.fileDialog2(caption = 'Scene Builder', ds = 2, fileMode = 4, okCaption = 'Load', 	fileFilter = multipleFilters)

	fbxFiles = []
	objFiles = []
	abcFiles = []
	maFiles = []
	mbFiles = []
	for x in files:
		if '.fbx' in str(x):
			fbxFiles.append(x)
		if '.obj' in str(x):
			objFiles.append(x)
		if '.abc' in str(x):
			abcFiles.append(x)
		if '.ma' in str(x):
			maFiles.append(x)
		if '.mb' in str(x):
			mbFiles.append(x)

	if len(mbFiles) > 0:
		for x in mbFiles:
			cmds.file(str(x), i = True, type = 'mayaBinary', ignoreVersion = True ,mergeNamespacesOnClash = False)
            
	if len(maFiles) > 0:
		for x in maFiles:
			cmds.file(str(x), i = True, type = 'mayaAscii', ignoreVersion = True ,mergeNamespacesOnClash = False)

	if len(fbxFiles) > 0:
		for x in fbxFiles:
			cmds.file(str(x), i = True, type = 'FBX', ignoreVersion = True ,mergeNamespacesOnClash = False)

	if len(objFiles) > 0:
		for x in objFiles:
			cmds.file(str(x), i = True, type = 'OBJ', ignoreVersion = True ,mergeNamespacesOnClash = False, )

	if len(abcFiles) > 0:
		for x in abcFiles:
			if not cmds.pluginInfo('AbcImport.mll', query = True, loaded = True):
				cmds.loadPlugin('AbcImport.mll')

			cmds.AbcImport(str(x), mode = 'import')

	sys.stdout.write('Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes/')

    
def showUI():
    cmds.window(title="Sence builder", widthHeight=(200, 200))
  
    cmds.columnLayout(adjustableColumn = True)
    cmds.separator(height=20)
    cmds.button(label="Make Cube", command=buttonFunction)
    cmds.button(label="Load",command=buttonFunction1)
    cmds.showWindow()
    
    
    
showUI()




