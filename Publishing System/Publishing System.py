try:
    from shiboken2 import wrapInstance
except ImportError:
    from shiboken import wrapInstance

try:
    from PySide2.QtGui import QIcon
    from PySide2.QtWidgets import QWidget
except ImportError:
    from PySide.QtGui import QIcon, QWidget
import maya.cmds as cmds

from maya import OpenMayaUI as OpenMayaUI
import logging
import random
import json
import sys
import re

"""
window1 = mc.window(title="Publishing System", widthHeight=(400,400))
cmds.columnLayout(adjustableColumn=True)
cmds.button(label="Sync current file")
cmds.button(label="Save the selected object")
cmds.text(" ")
cmds.text(" ")
cmds.text(label="File Publishing", fn="boldLabelFont")
cmds.text(" ")
cmds.text(label="Selected File Publishing")

o = mc.optionMenu(label = "File Format") # Create options menu
cmds.menuItem(label = "USD", parent = o) # Add to menu content USD
cmds.menuItem(label = "Almembic", parent = o) # Add to menu content Almembic
cmds.menuItem(label = "FBX", parent = o) # Add to menu content FBX
cmds.button(label = "Publish", w=100, h=50, command='mc.showWindow(window2)')
cmds.showWindow(window1)

window2 = mc.window(title="ProgressBar", widthHeight=(300,150))
cmds.columnLayout(adjustableColumn=True)
progressControl = mc.progressBar(maxValue = 6, width = 300)
cmds.button(label = "Close", command = "mc.progressBar(progressControl, edit = True, step = 2)")
"""
# Logging Setup
logging.basicConfig()
logger = logging.getLogger("gt_transfer_transforms")
logger.setLevel(logging.INFO)

# Script Name
script_name = 'Transfer Transforms'

# Stored Values Dict - Get/Set Function
gt_transfer_transforms_dict = {'tx': 0.0,
                               'ty': 0.0,
                               'tz': 0.0,

                               'rx': 0.0,
                               'ry': 0.0,
                               'rz': 0.0,

                               'sx': 1.0,
                               'sy': 1.0,
                               'sz': 1.0,
                               }


# Main Form ============================================================================
def build_gui_transfer_transforms():
    window_name = 'build_gui_transfer_transforms'
    if cmds.window(window_name, exists=True):
        cmds.deleteUI(window_name)
# Main GUI Start Here =================================================================================

    window_gui_transfer_transforms = cmds.window(window_name, title=script_name,
                                                 titleBar=True, mnb=False, mxb=False, sizeable=True)

    cmds.window(window_name, e=True, s=True, wh=[1, 1])

    content_main = cmds.columnLayout(adj=True)

    # Title Text
    title_bgc_color = (.4, .4, .4)
    cmds.separator(h=10, style='none')  # Empty Space
    cmds.rowColumnLayout(nc=1, cw=[(1, 240)], cs=[(1, 10)], p=content_main)  # Window Size Adjustment
    cmds.rowColumnLayout(nc=3, cw=[(1, 10), (2, 170), (3, 50)], cs=[(1, 10), (2, 0), (3, 0)],
                         p=content_main)  # Title Column
    cmds.text(' ', bgc=title_bgc_color)  # Tiny Empty Green Space
    cmds.text(script_name, bgc=title_bgc_color, fn='boldLabelFont', align='left')
    cmds.button(l='Help', bgc=title_bgc_color, c=lambda x: build_gui_help_transfer_transforms())
    cmds.separator(h=10, style='none')  # Empty Space

    # Body ====================
    body_column = cmds.rowColumnLayout(nc=1, cw=[(1, 230)], cs=[(1, 10)], p=content_main)

    cmds.rowColumnLayout(nc=1, cw=[(1, 230)], cs=[(1, 20)])
    transform_column_width = [100, 1]

    # Translate
    translate_x_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                            label1='  Translate X', label2='Invert Value', v1=True, v2=False)

    translate_y_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                            label1='  Translate Y', label2='Invert Value', v1=True, v2=False)

    translate_z_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                            label1='  Translate Z', label2='Invert Value', v1=True, v2=False)

    cmds.separator(h=10, p=body_column)

    # Rotate
    cmds.rowColumnLayout(nc=1, cw=[(1, 230)], cs=[(1, 20)], p=body_column)
    rotate_x_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                         label1='  Rotate X', label2='Invert Value', v1=True, v2=False)

    rotate_y_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                         label1='  Rotate Y', label2='Invert Value', v1=True, v2=False)

    rotate_z_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                         label1='  Rotate Z', label2='Invert Value', v1=True, v2=False)

    cmds.separator(h=10, p=body_column)

    # Scale  
    cmds.rowColumnLayout(nc=1, cw=[(1, 230)], cs=[(1, 20)], p=body_column)
    scale_x_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                        label1='  Scale X', label2='Invert Value', v1=True, v2=False)

    scale_y_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                        label1='  Scale Y', label2='Invert Value', v1=True, v2=False)

    scale_z_checkbox = cmds.checkBoxGrp(columnWidth2=transform_column_width, numberOfCheckBoxes=2,
                                        label1='  Scale Z', label2='Invert Value', v1=True, v2=False)

    cmds.separator(h=10, p=body_column)

    # Left Side Tag text fields

    # side_text_container = cmds.rowColumnLayout( p=content_main, numberOfRows=1, adj=True)
    cmds.rowColumnLayout(nc=2, cw=[(1, 100), (2, 100)], cs=[(1, 15), (2, 0)], p=body_column)
    cmds.text('Left Side Tag:')
    cmds.text('Right Side Tag:')

    cmds.separator(h=7, style='none', p=body_column)  # Empty Space

    cmds.rowColumnLayout(nc=2, cw=[(1, 100), (2, 100)], cs=[(1, 15), (2, 0)], p=body_column)
    left_tag_text_field = cmds.textField(text='left_',
                                         enterCommand=lambda x: transfer_transforms_side_to_side('left'))
    right_tag_text_field = cmds.textField(text='right_',
                                          enterCommand=lambda x: transfer_transforms_side_to_side('right'))

    cmds.separator(h=7, style='none', p=body_column)  # Empty Space

    cmds.rowColumnLayout(nc=1, cw=[(1, 210)], cs=[(1, 10)], p=body_column)
    cmds.button(l='From Right to Left', c=lambda x: transfer_transforms_side_to_side('right'))
    cmds.button(l='From Left to Right', c=lambda x: transfer_transforms_side_to_side('left'))
    cmds.separator(h=7, style='none', p=body_column)  # Empty Space
    cmds.separator(h=10, p=body_column)

    cmds.rowColumnLayout(nc=2, cw=[(1, 112), (2, 113)], cs=[(1, 10), (2, 5)], p=content_main)
    cmds.separator(h=5, style='none')  # Empty Space
    cmds.separator(h=5, style='none')  # Empty Space
    cmds.button(l='Export Transforms', c=lambda x: validate_import_export('export'))
    cmds.button(l='Import Transforms', c=lambda x: validate_import_export('import'))
    cmds.separator(h=3, style='none')  # Empty Space

    cmds.rowColumnLayout(nc=1, cw=[(1, 230)], cs=[(1, 10)], p=content_main)
    cmds.button(l='Transfer (Source/Targets)', bgc=(.6, .6, .6), c=lambda x: transfer_transforms())
    cmds.separator(h=5, style='none')  # Empty Space

    cmds.separator(h=10, p=content_main)

    # Copy and Paste Transforms
    copy_text_container = cmds.rowColumnLayout(p=content_main, numberOfRows=1, adj=True)
    cmds.text('Copy and Paste Transforms', p=copy_text_container)
    cmds.separator(h=7, style='none', p=content_main)  # Empty Space

    cmds.rowColumnLayout(nc=4, cw=[(1, 21), (2, 63), (3, 62), (4, 62)], cs=[(1, 15), (2, 0), (3, 3), (4, 3)],
                         p=content_main)

    cmds.text(' ')
    cmds.text('X', bgc=[.5, 0, 0])
    cmds.text('Y', bgc=[0, .5, 0])
    cmds.text('Z', bgc=[0, 0, .5])

    cmds.rowColumnLayout(nc=4, cw=[(1, 20), (2, 65), (3, 65), (4, 65)], cs=[(1, 15), (2, 0)], p=content_main)

    cmds.text('T')
    tx_copy_text_field = cmds.textField(text='0.0', ann='tx', cc=lambda x: update_get_dict(tx_copy_text_field))
    ty_copy_text_field = cmds.textField(text='0.0', ann='ty')
    tz_copy_text_field = cmds.textField(text='0.0', ann='tz')

    cmds.text('R')
    rx_copy_text_field = cmds.textField(text='0.0', ann='rx')
    ry_copy_text_field = cmds.textField(text='0.0', ann='ry')
    rz_copy_text_field = cmds.textField(text='0.0', ann='rz')

    cmds.text('S')
    sx_copy_text_field = cmds.textField(text='1.0', ann='sx')
    sy_copy_text_field = cmds.textField(text='1.0', ann='sy')
    sz_copy_text_field = cmds.textField(text='1.0', ann='sz')

    cmds.separator(h=7, style='none', p=content_main)  # Empty Space

    cmds.rowColumnLayout(nc=2, cw=[(1, 115), (2, 115)], cs=[(1, 10), (2, 0)], p=content_main)

    cmds.button(l='Get TRS', c=lambda x: transfer_transforms_copy_paste('get'))
    cmds.button(l='Set TRS', c=lambda x: transfer_transforms_copy_paste('set'))

    cmds.separator(h=7, style='none', p=content_main)  # Empty Space

    def update_get_dict(textfield):
        """
        Stores provided value to the settings dictionary 
        
        Args:
            textfield (cmds.textField): Textfield used to extract the values. Text = Float, Ann = Attr
        
        """
        text = cmds.textField(textfield, q=True, text=True)
        ann = cmds.textField(textfield, q=True, ann=True)
        previous_value = gt_transfer_transforms_dict.get(ann)
        try:
            new_value = float(text)
            gt_transfer_transforms_dict[ann] = new_value
        except Exception as e:
            logger.debug(str(e))
            cmds.textField(textfield, e=True, text=previous_value)

    def extract_checkbox_transform_value(checkbox_grp, attribute_name):
        """
        Returns the checkbox transform value to determine if in use, inverted and the name of the attribute
        
        Returns:
            list (list): [is_used, is_inverted, attribute_name]
        
        """
        is_used = cmds.checkBoxGrp(checkbox_grp, q=True, value1=True)
        is_inverted = cmds.checkBoxGrp(checkbox_grp, q=True, value2=True)
        attribute_name = attribute_name
        return [is_used, is_inverted, attribute_name]

    def get_desired_transforms():
        """
        Returns a list with all the TRS data
        
                Returns:
                    transforms (list): T(XYZ) R(XYZ) S(XYZ)
        
        """
        transforms = []
        tx = extract_checkbox_transform_value(translate_x_checkbox, 'tx')
        ty = extract_checkbox_transform_value(translate_y_checkbox, 'ty')
        tz = extract_checkbox_transform_value(translate_z_checkbox, 'tz')

        rx = extract_checkbox_transform_value(rotate_x_checkbox, 'rx')
        ry = extract_checkbox_transform_value(rotate_y_checkbox, 'ry')
        rz = extract_checkbox_transform_value(rotate_z_checkbox, 'rz')

        sx = extract_checkbox_transform_value(scale_x_checkbox, 'sx')
        sy = extract_checkbox_transform_value(scale_y_checkbox, 'sy')
        sz = extract_checkbox_transform_value(scale_z_checkbox, 'sz')

        transforms.append(tx)
        transforms.append(ty)
        transforms.append(tz)

        transforms.append(rx)
        transforms.append(ry)
        transforms.append(rz)

        transforms.append(sx)
        transforms.append(sy)
        transforms.append(sz)
        return transforms

        # Main Function Starts --------------------------------------------
    def transfer_transforms():
        """
        Transfer the transforms from source to target according to provided settings
        """
        if len(cmds.ls(selection=True)) != 0:
            source = cmds.ls(selection=True)[0]
            targets = cmds.ls(selection=True)
            targets.remove(source)

            # Settings
            transforms = get_desired_transforms()
            errors = []

            # Transfer 
            for transform in transforms:
                if transform[0]:  # Using Transform?
                    if transform[1]:  # Inverted?
                        source_transform = (cmds.getAttr(source + '.' + transform[2]) * -1)
                    else:
                        source_transform = cmds.getAttr(source + '.' + transform[2])

                    for target in targets:
                        if not cmds.getAttr(target + '.' + transform[2], lock=True):
                            cmds.setAttr(target + '.' + transform[2], source_transform)
                        else:
                            errors.append(target + ' "' + transform[2] + '" is locked.')
            if len(errors) != 0:
                unique_message = '<' + str(random.random()) + '>'
                if len(errors) == 1:
                    is_plural = ' attribute was '
                else:
                    is_plural = ' attributes were '
                unique_message += '<span style=\"color:#FF0000;text-decoration:underline;\">'
                unique_message += str(len(errors)) + '</span><span style=\"color:#FFFFFF;\"> locked' + is_plural
                unique_message += 'ignored. (Open Script Editor to see a list)</span>'
                cmds.inViewMessage(amg=unique_message, pos='botLeft', fade=True, alpha=.9)
                sys.stdout.write(str(len(errors)) + ' locked ' + is_plural + 'ignored. '
                                                                             '(Open Script Editor to see a list)\n')
                for error in errors:
                    print(str(error))
        else:
            cmds.warning('Select source 1st, then targets 2nd, 3rd...')

    # Main Function Ends --------------------------------------------

    def transfer_transforms_side_to_side(source_side):
        """
        Uses the naming convention to pair elements and mirror transforms
        """
        if len(cmds.ls(selection=True)) != 0:

            # Settings
            left_side_tag = parse_text_field(cmds.textField(left_tag_text_field, q=True, text=True))[0]
            right_side_tag = parse_text_field(cmds.textField(right_tag_text_field, q=True, text=True))[0]
            transforms = get_desired_transforms()
            errors = []

            selection = cmds.ls(selection=True)

            right_side_objects = []
            left_side_objects = []

            for obj in selection:
                if right_side_tag in obj:
                    right_side_objects.append(obj)

            for obj in selection:
                if left_side_tag in obj:
                    left_side_objects.append(obj)

            for left_obj in left_side_objects:
                for right_obj in right_side_objects:
                    remove_side_tag_left = left_obj.replace(left_side_tag, '')
                    remove_side_tag_right = right_obj.replace(right_side_tag, '')
                    if remove_side_tag_left == remove_side_tag_right:
                        print(right_obj + ' was paired with ' + left_obj)

                        # Transfer Right to Left
                        if source_side is 'right':
                            for transform in transforms:
                                if transform[0]:  # Using Transform?
                                    if transform[1]:  # Inverted?
                                        source_transform = (cmds.getAttr(right_obj + '.' + transform[2]) * -1)
                                    else:
                                        source_transform = cmds.getAttr(right_obj + '.' + transform[2])

                                    if not cmds.getAttr(left_obj + '.' + transform[2], lock=True):
                                        cmds.setAttr(left_obj + '.' + transform[2], source_transform)
                                    else:
                                        errors.append(left_obj + ' "' + transform[2] + '" is locked.')

                        # Transfer Left to Right
                        if source_side is 'left':
                            for transform in transforms:
                                if transform[0]:  # Using Transform?
                                    if transform[1]:  # Inverted?
                                        source_transform = (cmds.getAttr(left_obj + '.' + transform[2]) * -1)
                                    else:
                                        source_transform = cmds.getAttr(left_obj + '.' + transform[2])

                                    if not cmds.getAttr(right_obj + '.' + transform[2], lock=True):
                                        cmds.setAttr(right_obj + '.' + transform[2], source_transform)
                                    else:
                                        errors.append(right_obj + ' "' + transform[2] + '" is locked.')

            if len(errors) != 0:
                unique_message = '<' + str(random.random()) + '>'
                if len(errors) == 1:
                    is_plural = ' attribute was '
                else:
                    is_plural = ' attributes were '
                unique_message += '<span style=\"color:#FF0000;text-decoration:underline;\">'
                unique_message += str(len(errors))
                unique_message += '</span><span style=\"color:#FFFFFF;\"> locked' + is_plural
                unique_message += 'ignored. (Open Script Editor to see a list)</span>'
                cmds.inViewMessage(amg=unique_message, pos='botLeft', fade=True, alpha=.9)
                sys.stdout.write(str(len(errors)) + ' locked ' + is_plural + 'ignored. '
                                                                             '(Open Script Editor to see a list)\n')
                for error in errors:
                    print(str(error))
        else:
            cmds.warning('Select all elements you want to match before running the script')
            # Side to Side Function Ends --------------------------------------------

    # Copy Paste Function Starts --------------------------------------------
    def transfer_transforms_copy_paste(operation):
        """
        Validate operation before Getting and Settings transforms (Copy and Paste)
        """
        copy_text_fields = [tx_copy_text_field, ty_copy_text_field, tz_copy_text_field,
                            rx_copy_text_field, ry_copy_text_field, rz_copy_text_field,
                            sx_copy_text_field, sy_copy_text_field, sz_copy_text_field]

        if operation == 'get':
            if len(cmds.ls(selection=True)) != 0:
                # Object to Get
                source = cmds.ls(selection=True)[0]

                # Settings
                transforms = get_desired_transforms()

                # Transfer 
                for transform in transforms:  # Using Transform, Inverted?, Attribute
                    if transform[0]:  # Using Transform?
                        source_transform = cmds.getAttr(source + '.' + transform[2])
                        source_transform_truncated = ('{:.3f}'.format(source_transform))

                        gt_transfer_transforms_dict[transform[2]] = source_transform

                        for text_field in copy_text_fields:
                            if cmds.textField(text_field, q=True, ann=True) == transform[2]:
                                cmds.textField(text_field, e=True, text=source_transform_truncated, en=True)
            else:
                cmds.warning('Select an object to get its transforms')

        if operation == 'set':
            if len(cmds.ls(selection=True)) != 0:
                # Objects to Set
                targets = cmds.ls(selection=True)

                # Settings
                transforms = get_desired_transforms()
                errors = []

                # Transfer 
                for transform in transforms:  # Using Transform, Inverted?, Attribute
                    if transform[0]:  # Using Transform?
                        for target in targets:
                            if not cmds.getAttr(target + '.' + transform[2], lock=True):
                                if transform[1]:  # Inverted?
                                    cmds.setAttr(target + '.' + transform[2],
                                                 (float(gt_transfer_transforms_dict.get(transform[2]) * -1)))
                                else:
                                    cmds.setAttr(target + '.' + transform[2],
                                                 float(gt_transfer_transforms_dict.get(transform[2])))
                            else:
                                errors.append(target + ' (' + transform[2] + ') is locked.')

                if len(errors) != 0:
                    unique_message = '<' + str(random.random()) + '>'
                    if len(errors) == 1:
                        is_plural = ' attribute was '
                    else:
                        is_plural = ' attributes were '
                    unique_message += '<span style=\"color:#FF0000;text-decoration:underline;\">'
                    unique_message += str(len(errors))
                    unique_message += '</span><span style=\"color:#FFFFFF;\"> locked' + is_plural
                    unique_message += 'ignored. (Open Script Editor to see a list)</span>'
                    cmds.inViewMessage(amg=unique_message, pos='botLeft', fade=True, alpha=.9)
                    sys.stdout.write(str(len(errors)) + ' locked ' + is_plural + 'ignored. '
                                                                                 '(Open Script Editor to see a list)\n')
                    for error in errors:
                        print(str(error))

            else:
                cmds.warning('Select objects to set their transforms')
    
    # Copy Paste Function Ends --------------------------------------------

    def validate_import_export(operation):
        """
        Creates undo chunk for import and export operations
        """
        function_name = script_name + ' ' + operation.capitalize() + ' Transforms'
        cmds.undoInfo(openChunk=True, chunkName=function_name)

        try:
            if operation == 'import':
                import_trs_transforms()

            if operation == 'export':
                export_trs_transforms()

        except Exception as e:
            logger.debug(str(e))
        finally:
            cmds.undoInfo(closeChunk=True, chunkName=function_name)

    # Valida Import Export Ends --------------------------------------------  

    # Show and Lock Window
    cmds.showWindow(window_gui_transfer_transforms)
    cmds.window(window_name, e=True, s=False)

    # Set Window Icon
    qw = OpenMayaUI.MQtUtil.findWindow(window_name)
    widget = wrapInstance(int(qw), QWidget)
    icon = QIcon(':/transform.svg')
    widget.setWindowIcon(icon)

    # Deselect Text Field
    cmds.setFocus(window_name)

    # Main GUI Ends Here =================================================================================

