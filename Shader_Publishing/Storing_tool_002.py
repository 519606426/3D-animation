import maya.cmds as cmds
import os
import json
import pprint

cmds.window(title='HT shader tool', widthHeight=(500, 700) )
cmds.rowColumnLayout(numberOfColumns=1)
cmds.textFieldButtonGrp( label='Library', buttonLabel='save', bc='save()')

directory = "C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shader_Geo_group"

dirList = cmds.textScrollList(numberOfRows = 35, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shader_Geo_group"))
cmds.rowColumnLayout(numberOfColumns=3)
cmds.button( label = ('Import'),c = 'save()')
cmds.button( label = ('Refresh'),c = 'find()')
cmds.button( label = ('Close'),c = 'close()')

USERAPPDIR = cmds.internalVar(userAppDir=True)
DIRECTORY = os.path.join(USERAPPDIR, "controllerLibrary")
def createDirectory(directory=DIRECTORY):

def save():
path = os.path.join(directory,"{0}.ma".format(name))
infoFile = os.path.join(directory,"{0}.json".format(name))
        info["name"] = name
        info["path"] = path
if screenshot:
            self.saveScreenshot(name,directory)
 cmds.file(rename=path)
if cmds.ls(selection=True):
            cmds.file(force=True,type="mayaAscii",exportSelected=True)
else:
            cmds.file(save=True,type="mayaAscii",force=True)
with open(infoFile,"w") as f:
            json.dump(info,f,indent=4)

        self[name] = path
def find(self,directory=DIRECTORY):
        self.clear()

        if not os.path.exists(directory):
            return None

        files = os.listdir(directory)
        mayaFiles = [f for f in files if f.endswith(".ma")]
 for ma in mayaFiles:
            name,ext = os.path.splitext(ma)
            path = os.path.join(directory,ma)

infoFile = "{0}.json".format(name)
            if infoFile in files:
                infoFile = os.path.join(directory,infoFile)
                with open(infoFile,"r") as f:
                    info = json.load(f)
            else:
                print(u"no{0}file".format(infoFile))
                info = {}
            screenshot = "{0}.jpg".format(name)
            if screenshot in files:
                info["screenshot"] = os.path.join(directory,screenshot)
            info["name"]=name
            info["path"]=path
            self[name]=info
    def load(self,name):
        path = self[name]["path"]
        cmds.file(path,i=True,usingNamespaces=False)
    def saveScreenshot(self,name,directory=DIRECTORY):
        path = os.path.join(directory,"{0}.jpg".format(name))
        cmds.viewFit()
        cmds.setAttr("defaultRenderGlobals.imageFormat",8)
        cmds.playblast(completeFilename=path,forceOverwrite=True,format="image",width=200,height=200,
                       showOrnaments=False,startTime=1,endTime=1,viewer=False)

        return path






cmds.showWindow()