import maya.cmds as cmd



def exportMesh():
  #selObj = cmds.ls(sl = 1)
  path = '/*save shaders*/'
  #FileName = selObj
  for i in checkSelect():
    mainPath = path +'/' +i
    cmds.file(mainPath, pr=1, es=1, force=1, options="groups=1;ptgroups=1;materials=1;smoothing=1;normals=1",type="FBX export")


def mainGui():
  windowName = 'Export_Tool'
  windowTitle = 'Export_Tool1.0'


  cmd.window(windowName,title = windowTitle)
  cmd.columnLayout(adj = True)


  cmd.button(l='Export', c='exportMesh()')

  cmd.showWindow(windowName)


mainGui()