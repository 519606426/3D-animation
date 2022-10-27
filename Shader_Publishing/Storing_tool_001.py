import maya.cmds as cmds


cmds.window(title='HT shader tool', widthHeight=(500, 700) )
cmds.rowColumnLayout(numberOfColumns=1)
cmds.textFieldButtonGrp( label='Library', buttonLabel='save', bc='save()')

directory = "C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shader_Geo_group"

dirList = cmds.textScrollList(numberOfRows = 35, append = os.listdir("C:/Users/61451/Documents/GitHub/3D-animation/Assessment2_Group4/scenes/publish/shader_Geo_group"))
cmds.rowColumnLayout(numberOfColumns=3)
cmds.button( label = ('Import'),c = 'fileImport()')
cmds.button( label = ('Refresh'),c = 'find()')
cmds.button( label = ('Close'),c = 'close()')








cmds.showWindow()