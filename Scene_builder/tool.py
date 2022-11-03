import maya.cmds as cmds

def buttonFunction_select(args):
   
    
    #path = 'Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes/'
	#sys.path.append("Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes/")
	multipleFilters =  "All native importable files (*.ma *.mb *.obj *.fbx *.abc);; Maya binary (*.mb);; Maya Ascii 	(*.ma);; Obj (*.obj);; FBX (*.fbx);; Alembic Cache (*.abc)"
	files = cmds.fileDialog2(caption = 'Scene Builder', ds = 2, fileMode = 4, okCaption = 'Load', 	fileFilter = multipleFilters)
    #sys.path.append('Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes')
        #os.path.commonprefix(['Users/mine/Desktop/3D Animation/Assessment2_GroupX/scenes'])
     
    
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


def buttonFunction_animation(args):
    cmds.file("scenes/wip/sequence/lng01/lng01_010/animation/lng01_010_anim.v003.mb", i=True)
#    cmds.file("scenes/publish/sequence/lng01/lng01_010/animation/source/lng01_010_anim.v003.mb", i=True)
    
def buttonFunction_layout(args):        
#    cmds.file("scenes/publish/sequence/lng01/lng01_010/layout/cache/alembic/lng01_010_layout.v002.abc", i=True)
    cmds.file("scenes/wip/sequence/lng01/lng01_010/layout/lng01_010_layout.v002.mb", i=True)
def buttonFunction_Light(args):
    cmds.file("scenes/wip/sequence/lng01/lng01_010/light/lng01_010_light.v002.mb", i=True)

def showUI():

    cmds.window(title="Sence builder", widthHeight=(200, 200))
  
    cmds.columnLayout(adjustableColumn = True)
    cmds.separator(height=20)
    cmds.text("Load")
    cmds.button(label="Select",command=buttonFunction_select)
    cmds.button(label="Animation",command=buttonFunction_animation)
    cmds.button(label="Layout",command=buttonFunction_layout)
   # cmds.button(label="Light",command=buttonFunction_Light)
    cmds.showWindow()
    
    
    
showUI()
