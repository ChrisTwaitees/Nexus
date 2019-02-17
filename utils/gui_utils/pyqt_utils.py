"""
Various Utility Functions used for the PyQt Based Content Browser


Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
import sys
import webbrowser
import os
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc


# reference:https://joekuan.wordpress.com/2015/09/23/list-of-qt-icons/
def icons_dict(icon_name):
    icon_dict = {"Exit": "SP_BrowserStop", "OpenFile": "SP_DialogOpenButton", "Check": "SP_DialogApplyButton",
                 "Save": "SP_DialogSaveButton", "Refresh": "SP_BrowserReload", "Add": "SP_FileDialogNewFolder",
                 "New": "SP_FileDialogNewFolder", "Delete": "SP_DialogDiscardButton", "Trash": "SP_TrashIcon",
                 "Next": "SP_ToolBarHorizontalExtensionButton", "NewTab": "SP_ToolBarHorizontalExtensionButton",
                 "Info": "SP_MessageBoxInformation", "ArrowDown": "SP_ArrowDown", "ArrowUp": "SP_ArrowUp",
                 "ArrowBack": "SP_ArrowBack", "ArrowLeft": "SP_ArrowLeft", "ArrowRight": "SP_ArrowRight",
                 "ArrowForward": "SP_ArrowForward", "Help": "SP_MessageBoxQuestion"
                 }
    return icon_dict[icon_name]


def get_icon(parent, icon_name):
        icon_type = icons_dict(icon_name)
        return parent.style().standardIcon(getattr(qw.QStyle, icon_type))


def get_user_text(parent, header="", label=""):
    return SimpleConfirmDialog(parent, header, label).get_user_text()


def get_user_int(parent, header="", label=""):
    return SimpleConfirmDialog(parent, header, label).get_user_int()


def delete_widgets_in_layout(parent):
    for i in reversed(range(parent.layout.count())):
        parent.layout.itemAt(i).widget().setParent(None)


def set_stylesheet(object, style):
     css_path_dir = os.path.dirname(__file__)
     css_path = os.path.join(css_path_dir, "style", "%s.css"%style)
     if os.path.exists(css_path):
         with open(css_path, 'r') as css:
             object.setStyleSheet(css.read())


class SimpleWindow(qw.QMainWindow):
    def __init__(self, name, width=500, height=500, docs_page="https://github.com/ChrisTwaitees", style="dark"
                 ):
        super(SimpleWindow, self).__init__()

        self.window_title = name
        self.width = width
        self.height = height
        self.style = style

        self.docs_page = docs_page

        self.create_window()
        self.create_menu_bar()
        self.create_widgets()
        self.create_layouts()
        set_stylesheet(self, self.style)

        self.center()

    def create_window(self):
        self.setGeometry(self.width, self.height, self.width, self.height)
        self.setWindowTitle(self.window_title)

    def create_menu_bar(self):
        SimpleMenuBar(self, docs_page=self.docs_page)

    def create_widgets(self):
        self.widgets = qw.QWidget()

    def create_layouts(self):
        self.layout = qw.QVBoxLayout()
        self.widgets.setLayout(self.layout)
        self.setCentralWidget(self.widgets)

    def center(self):
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def derived_from(self, object):
        return isinstance(qw.QMainWindow(), object)


class SimpleMenuBar(qw.QMenu):
    # TODO handler if widget is not derived from QMainWindow
    def __init__(self, widget, docs_page=""):
        super(SimpleMenuBar, self).__init__()

        if widget.derived_from(qw.QMainWindow):
            self.menubar = widget.menuBar()
        else:
            self.menubar = qw.QMenu()

        # FILE MENU
        file_menu = self.menubar.addMenu('&File')
        # Exit action
        exit_icon = self.get_icon("Exit")
        exit_act = qw.QAction(exit_icon, '&Exit', widget)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qw.qApp.quit)
        file_menu.addAction(exit_act)

        # help
        help_menu = self.menubar.addMenu('&Help')
        # Exit action
        help_icon = self.get_icon("Help")
        help_act = qw.QAction(help_icon, '&Open Support Page', widget)
        help_act.setShortcut('Ctrl+H')
        help_act.setStatusTip("Open Tool's Support Page")
        help_act.triggered.connect(lambda: self.open_browser(docs_page))
        help_menu.addAction(help_act)

    def add_menu(self):
        pass

    def open_browser(self, url):
        webbrowser.open(url, new=0, autoraise=1)

    def get_icon(self, icon_name):
        icon_type = icons_dict(icon_name)
        return self.style().standardIcon(getattr(qw.QStyle, icon_type))


class RaisedVBoxWidget(qw.QFrame):
    def __init__(self):
        super(RaisedVBoxWidget, self).__init__()
        self.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        self.widgets = qw.QWidget()
        self.widgets.layout = qw.QVBoxLayout()
        self.widgets.setLayout(self.widgets.layout)
        self.setLayout(self.widgets.layout)

    def addWidget(self, widget):
        self.widgets.layout.addWidget(widget)


class RaisedHBoxWidget(qw.QFrame):
    def __init__(self):
        super(RaisedVBoxWidget, self).__init__()
        self.setFrameStyle(qw.QFrame.Panel | qw.QFrame.Raised)
        self.widgets = qw.QWidget()
        self.widgets.layout = qw.QHBoxLayout()
        self.widgets.setLayout(self.widgets.layout)
        self.setLayout(self.widgets.layout)

    def addWidget(self, widget):
        self.widgets.layout.addWidget(widget)


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


class SimpleCollapsibleWidget(qw.QGroupBox):
    def __init__(self, title="title"):
        super(SimpleCollapsibleWidget, self).__init__()
        self.setTitle(title)
        self.setCheckable(True)
        self.setChecked(True)

        self.original_height = self.minimumHeight()
        self.toggled.connect(lambda: self.toggle_group())

    def toggle_group(self):
        if self.isChecked():
            self.setMinimumHeight(self.original_height)
        else:
            self.setFixedHeight(self.fontMetrics().height())

class HighlightWidget(qw.QWidget):
    def __init__(self, parent, alpha=125):
        super(HighlightWidget, self).__init__(parent)
        self.parent = parent
        self.opacity = alpha
        self.highlight_colour = parent.palette().color(qg.QPalette.Highlight)
        self.highlight_colour.setAlpha(alpha)

        self.palette = qg.QPalette(parent.palette())
        self.palette.setColor(self.palette.Background, qc.Qt.transparent)

        self.setPalette(self.palette)
        self.hide()

    def paintEvent(self, event):
        painter = qg.QPainter()
        painter.begin(self)
        painter.setOpacity(self.opacity)
        painter.setRenderHint(qg.QPainter.Antialiasing)
        painter.fillRect(event.rect(), qg.QBrush(self.highlight_colour))
        painter.setPen(qg.QPen(qc.Qt.NoPen))
