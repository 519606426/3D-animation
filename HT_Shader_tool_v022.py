import maya.cmds as cmds
import json
import os

cmds.window(title='HT shader tool', widthHeight=(500, 700) )
form = cmds.formLayout()
tabs = cmds.tabLayout(innerMarginWidth=5, innerMarginHeight=5)
cmds.formLayout( form, edit=True, attachForm=((tabs, 'top', 0), (tabs, 'left', 0), (tabs, 'bottom', 0), (tabs, 'right', 0)) )


child1 = cmds.rowColumnLayout(numberOfColumns=1)

SceneDir = str(cmds.file(q=True, exn=True))

myShader = cmds.shadingNode('anisotropic', asShader=True)
cmds.swatchDisplayPort('slPP', wh=(60, 60), sn=myShader)

newNode = cmds.shadingNode( 'blinn', asShader=True )
newNodeAttr = newNode + '.normalCamera'
cmds.attrColorSliderGrp( label='Color', rgb=(1, 0, 0), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Transparency', rgb=(1, 0, 0), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Ambient color', rgb=(2, 4, 123), at=newNodeAttr)
cmds.attrColorSliderGrp( label='Incandescence', rgb=(2, 4, 123), at=newNodeAttr)


cmds.columnLayout(adjustableColumn = True, cal = "center", w=300)


cmds.textField(tx = SceneDir)
cmds.button( label="Publish", command = 'PublishShaders()')

ShaderVerInput = cmds.intField(width = 50, v=0)

cmds.button(label = 'Apply Shaders', command = 'ImportShaders()')

cmds.setParent("..")

ShaderPUB_Dir = ""
BaseSurfacingName = ""

if(len(SceneDir) > 0):
    ShaderPUB_Dir = SceneDir.replace("wip", "publish")
    ShaderDirArray=[]
    for i in ShaderPUB_Dir.split('/'):
        ShaderDirArray.append(i)
    FileNameArray=[]
    for i in ShaderDirArray[-1].split('.'):
        FileNameArray.append(i)
    BaseSurfacingName = FileNameArray[0] + ".v"
    ShaderDirArray.remove(ShaderDirArray[-1])
    ShaderPUB_Dir = '/'.join(ShaderDirArray) + "/" 


def PublishShaders():
    selected = cmds.ls(selection = True) 
    ShadersToExport = []
    MeshDataToExport = []
    MeshMaterials={} 
    
    if(len(selected) == 0):
        print("No Meshes Selected - Exporting All Shaders")
        selected = cmds.ls('mRef_*')
        cmds.select(selected)
        
    else:
        print("Meshes Selected: Exporting Shaders")
    if(not cmds.listRelatives(selected[0], s=True)):
        print("Selected Group or Transform")
        selected = cmds.listRelatives(selected[0], c=True)
    for i in range(len(selected)):
        selectedMesh = cmds.listRelatives(selected[i], shapes=True)[0]
        selectedMeshShading = cmds.listConnections(selectedMesh, type="shadingEngine")[0]
        selectedMat = cmds.listConnections(selectedMeshShading + ".surfaceShader")[0]
        
        MeshMaterials[selectedMesh +":"+ selectedMat] = {"AttachedMaterial": selectedMat }
        ShadersToExport.append(selectedMat)
        
    cmds.select(ShadersToExport)
    fileIncrementer = 1
    while os.path.exists(ShaderPUB_Dir + BaseSurfacingName + str(fileIncrementer) +".mb"):
        fileIncrementer += 1

    json_object = json.dumps(MeshMaterials, indent = 4)
    print(ShaderPUB_Dir + BaseSurfacingName + str(fileIncrementer) +".json")
    with open(ShaderPUB_Dir + BaseSurfacingName + str(fileIncrementer) +".json", "w") as outfile:
        outfile.write(json_object)
    cmds.file(ShaderPUB_Dir + BaseSurfacingName + str(fileIncrementer) +".mb", force=True, op="v=0;", typ="mayaBinary", pr=True, es=True)
    print ("Shaders Exported: "+str(ShadersToExport) + "| As: " + BaseSurfacingName + str(fileIncrementer) +".mb")
    cmds.select(cl = True)


def ImportShaders():
    SelectedShaderVer = cmds.intField(ShaderVerInput, q = True, value = True)
    SceneGeometryList = cmds.ls(selection = True)
    PreviouslyVisitedDirectories=[]
    if(len(SceneGeometryList) == 0):
        print("No Meshes Selected - Importing All Shaders")
        AllSceneGeometryList = cmds.ls(geometry=True)
        SceneGeometryList = AllSceneGeometryList
    else:
        print("Meshes Selected: " +str(SceneGeometryList)+ "Importing Shaders")

    for SceneGeometry in range(len(SceneGeometryList)):
        ModelReferenceDir = cmds.referenceQuery(SceneGeometryList[SceneGeometry], filename=True)
        ShaderPUB_Dir = ModelReferenceDir.replace("model/source", "surfacing")
        
        ShaderPUB_DirArray=[]
        for DirSplitFwdSlsh in ShaderPUB_Dir.split('/'):
            ShaderPUB_DirArray.append(DirSplitFwdSlsh)
        FileNameArray=[]
        for DirSplitPeriod in ShaderPUB_DirArray[-1].split('.'):
            FileNameArray.append(DirSplitPeriod)
        BaseSurfacingName = FileNameArray[0]
        BaseSurfacingName = BaseSurfacingName.replace("model", "surface")
        ShaderPUB_DirArray.remove(ShaderPUB_DirArray[-1])
        ShaderPUB_Dir = '/'.join(ShaderPUB_DirArray) + "/"
        
        fileIncrementer = 1
        while os.path.exists(ShaderPUB_Dir + BaseSurfacingName + ".v"+ str(fileIncrementer) +".mb"):
            fileIncrementer += 1
        ShaderVer = fileIncrementer - 1

        if(SelectedShaderVer > 0):
            ShaderVer = SelectedShaderVer
        
        LatestShaderMB_Dir = ShaderPUB_Dir + BaseSurfacingName + ".v"+ str(ShaderVer) +".mb"        
        LatestShaderJSON_Dir = ShaderPUB_Dir + BaseSurfacingName + ".v"+ str(ShaderVer) +".json"   
        if(os.path.exists(LatestShaderMB_Dir) & os.path.exists(LatestShaderJSON_Dir)):
            if(LatestShaderMB_Dir not in PreviouslyVisitedDirectories):
                PreviouslyVisitedDirectories.append(LatestShaderMB_Dir)
                with open(LatestShaderJSON_Dir, 'r') as infile:
                    data=infile.read()
                obj = json.loads(data)
            
                cmds.file(LatestShaderMB_Dir, i=True, type="mayaBinary", ra=True, rdn=True, mnc=False, ns="v_"+str(ShaderVer)+BaseSurfacingName, op="v=0", pr=True, an=True, itr="keep", mnr=True)
                
                for set in obj:
                    Obj_Material=[]
                    for i in set.split(':'):            
                        Obj_Material.append(i)
                    ObjTransformList = cmds.ls("*:"+Obj_Material[0]+"*")
                    MaterialList = cmds.ls("*v_"+str(ShaderVer)+BaseSurfacingName+"*:"+Obj_Material[1]+"*")
                    if(ObjTransformList):
                        ObjTransform = ObjTransformList[0]
                        Material = MaterialList[0]
                        print("Mesh: " + ObjTransform + " | Material: " + Material + " | Shader Ver. Being Applied: " + str(ShaderVer))
                        cmds.select(ObjTransform)
                        cmds.hyperShade(assign=str(Material))
                        cmds.select(cl=True)
                    else:
                        print("Error")
                infile.close()
        else:
            print("Error")


cmds.setParent( '..' )




child2 = cmds.rowColumnLayout(numberOfColumns=1)



class HTshader(object):
    
    
    def __init__(self):
    
        self.form = cmds.formLayout(numberOfDivisions=100)
        self.getListMat = cmds.ls(mat=1)
        self.scrollListMat = cmds.textScrollList(w=211, h=245, append=self.getListMat, sc=lambda *args: self.selectedItemFunc(1), dcc=lambda *args: self.selectedItemFunc(2))
        cmds.formLayout(self.form, edit=True, attachForm=[(self.scrollListMat, 'top', 0), (self.scrollListMat, 'left', 2)])
        self.assignMat = cmds.button(label='Assign', w=102, h=34, command=lambda *args: self.assignToSelectedFunc())
       
        self.deleteMat = cmds.button(label='Delete', w=102, h=34, command=lambda *args: self.deleteMatFunc())
        cmds.formLayout(self.form, edit=True, attachForm=[(self.deleteMat, 'top', 40), (self.deleteMat, 'left', 219)])

       
        self.refreshList = cmds.button(label='Refresh', w=102, h=34, command=lambda *args: self.refreshListFunc())
        cmds.formLayout(self.form, edit=True, attachForm=[(self.refreshList, 'top', 80), (self.refreshList, 'left', 219)])
       
        cmds.formLayout(self.form, edit=True, attachForm=[(self.assignMat, 'top', 0), (self.assignMat, 'left', 219)])
        cmds.setParent('..')

    def selectedItemFunc(self, value):
        selected = cmds.textScrollList(self.scrollListMat, q=True, si=True)


        if value == 1: 
            return selected
        elif value == 2: 
            cmds.select(selected[0])

    def assignToSelectedFunc(self):
        selected = cmds.ls(sl=True)

        for i in selected:
            cmds.hyperShade(a=self.selectedItemFunc(1)[0])
            
            
    def refreshListFunc(self):
        cmds.textScrollList(self.scrollListMat, edit=True, removeAll=True)
        getListMat = cmds.ls(mat=1)
        cmds.textScrollList(self.scrollListMat, edit=True, append=getListMat)

    def deleteMatFunc(self):
        try:
            cmds.delete(self.selectedItemFunc(1)[0])
            self.refreshListFunc()
        except TypeError:
            print('Choose the material.')
            
            

def SelectObj():
    getListMat = cmds.ls(mat=1)
    cmds.rowLayout("obj",nc=2,w=400,h=600)
    cmds.columnLayout( adj=True, columnAttach=('left', 5), rowSpacing=10, columnWidth=250 )
    cmds.textScrollList('obj')
    cmds.textFieldButtonGrp('obj',bl='Import Object', text='Select Object',ed=False, bc='selObjects()')
    
SelectObj()

def selObjects():
    sel=cmds.ls(sl=True)
    cmds.textScrollList('obj',e=True,ra=True)
    cmds.textScrollList('obj',e=True,numberOfRows=len(sel)+10, allowMultiSelection=True,append=sel)

HTshader()



    
cmds.setParent( '..' )

cmds.tabLayout( tabs, edit=True, tabLabel=((child1, 'Publish shaders'),(child2, 'Load/Assign')) )

cmds.showWindow()
