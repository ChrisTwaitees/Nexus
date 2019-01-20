"""
Various Utility Functions used for the PyQt Based Content Browser


Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


# reference: https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/
def icons_dict(icon_name):
    icon_dict = {"Exit": "SP_BrowserStop", "OpenFile": "SP_DialogOpenButton", "Check": "SP_DialogApplyButton",
                 "Save": "SP_DialogSaveButton", "Refresh": "SPBrowserReload", "Add": "SP_FileDialogNewFolder",
                 "New": "SP_FileDialogNewFolder", "Delete": "SP_DialogDiscardButton", "Trash": "SP_TrashIcon",
                 "Next": "SP_ToolBarHorizontalExtensionButton", "NewTab": "SP_ToolBarHorizontalExtensionButton",
                 "Info": "SP_MessageBoxInformation"
                 }
    return icon_dict[icon_name]


