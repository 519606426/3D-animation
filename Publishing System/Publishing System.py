import maya.cmds as mc

window1 = mc.window(title="Publishing System", widthHeight=(400,400))
mc.columnLayout(adjustableColumn=True)
mc.button(label="Sync current file")
mc.button(label="Save the selected object")
mc.text(" ")
mc.text(" ")
mc.text(label="File Publishing", fn="boldLabelFont")
mc.text(" ")
mc.text(label="Selected File Publishing")


o = mc.optionMenu(label = "File Format") # Create options menu
mc.menuItem(label = "USD", parent = o) # Add to menu content USD
mc.menuItem(label = "Almembic", parent = o) # Add to menu content Almembic
mc.menuItem(label = "FBX", parent = o) # Add to menu content FBX
mc.button(label = "Publish", w=100, h=50, command='mc.showWindow(window2)')
mc.showWindow(window1)

window2 = mc.window(title="ProgressBar", widthHeight=(300,150))
mc.columnLayout(adjustableColumn=True)
progressControl = mc.progressBar(maxValue = 6, width = 300)
mc.button(label = "Close", command = "mc.progressBar(progressControl, edit = True, step = 2)")
