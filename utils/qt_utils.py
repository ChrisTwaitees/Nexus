"""
Various Utility Functions used for the PyQt Based Content Browser


Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
import sys

# reference:https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/
def icons_dict(icon_name):
    icon_dict = {"Exit": "SP_BrowserStop", "OpenFile": "SP_DialogOpenButton", "Check": "SP_DialogApplyButton",
                 "Save": "SP_DialogSaveButton", "Refresh": "SP_BrowserReload", "Add": "SP_FileDialogNewFolder",
                 "New": "SP_FileDialogNewFolder", "Delete": "SP_DialogDiscardButton", "Trash": "SP_TrashIcon",
                 "Next": "SP_ToolBarHorizontalExtensionButton", "NewTab": "SP_ToolBarHorizontalExtensionButton",
                 "Info": "SP_MessageBoxInformation", "ArrowDown": "SP_ArrowDown", "ArrowUp": "SP_ArrowUp",
                 "ArrowBack": "SP_ArrowBack", "ArrowLeft": "SP_ArrowLeft", "ArrowRight": "SP_ArrowRight",
                 "ArrowForward": "SP_ArrowForward"
                 }
    return icon_dict[icon_name]


def get_icon(parent, icon_name):
        icon_type = icons_dict(icon_name)
        return parent.style().standardIcon(getattr(qw.QStyle, icon_type))


class SimpleConfirmDialog(qw.QInputDialog):
    def __init__(self, parent, header="", label=""):
        super().__init__(parent)
        self.parent = parent
        self.header = header
        self.label = label

    def get_user_text(self):
        return self.getText(self.parent, self.header, self.label)

    def get_user_int(self):
        return self.getText(self.parent, self.header, self.label)


def get_user_text(parent, header="", label=""):
    return SimpleConfirmDialog(parent, header, label).get_user_text()


def get_user_int(parent, header="", label=""):
    return SimpleConfirmDialog(parent, header, label).get_user_int()
