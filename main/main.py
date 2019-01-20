"""
DCC Independent Content Browser

Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
import sys
from utils import path_utils, qt_utils
from PyQt5.QtCore import (Qt, QMimeData, QRect)
from PyQt5.QtGui import (QFont, QIcon, QDrag, QPixmap)
from PyQt5.QtWidgets import (QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QMainWindow, QWidget,
                             qApp, QAction, QMessageBox, QMenu, QFileDialog, QStyle, QTabWidget, QVBoxLayout,
                             QInputDialog,  QLineEdit, QGridLayout, QScrollArea, QLabel, QFrame)


class ContentBrowserUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.version = "v0.1"
        self.initUI()

        # SHOW
        self.show()


    def initUI(self):
        # Construction
        self.setGeometry(400, 400, 400, 400)
        self.center()
        self.setWindowTitle('Content Browser')

        # Formatting
        QToolTip.setFont(QFont('SansSerif', 10))

        # STATUS BAR
        self.statusBar().showMessage('Ready')

        # MENUBAR
        menubar = self.menuBar()

        # FILE MENU
        file_menu = menubar.addMenu('&File')
        # Exit action
        exit_icon = self.fetch_icon("Exit")
        exit_act = QAction(exit_icon, '&Exit', self)
        exit_act.setShortcut('Ctrl+Q')
        exit_act.setStatusTip('Exit application')
        exit_act.triggered.connect(qApp.quit)
        file_menu.addAction(exit_act)

        # Add Action
        import_menu = QMenu('Add', self)
        # TODO connect path reader and perforce integration
        import_icon = self.fetch_icon("OpenFile")
        import_perf_action = QAction(import_icon, 'Add from P4F', self)
        import_perf_action.setStatusTip('Adds entry to current tab via Perforce Virtual Path')
        import_perf_action.triggered.connect(lambda: self.open_file_browser(start_dir=""))

        # TODO define start directories externally
        import_local_action = QAction('Add from Local Directory', self)
        import_local_action.setStatusTip('Adds from Local Directory')
        import_local_action.triggered.connect(lambda: self.open_file_browser(start_dir=""))
        import_menu.addAction(import_local_action)
        import_menu.addAction(import_perf_action)
        file_menu.addMenu(import_menu)

        # INFO MENU
        info_menu = menubar.addMenu('&Info')
        # Info action
        info_icon = self.fetch_icon("Info")
        info_act = QAction(info_icon, '&Info', self)
        info_act.setShortcut('Ctrl+I')
        info_act.setStatusTip('Information on this Version of DCC Browser')
        info_act.triggered.connect(lambda: self.display_version_info())

        info_menu.addAction(info_act)

        # TOOL BAR
        # TODO implement icon based utilities like loading, adding, assigning icon to selection, opening metadata source
        toolbar = self.addToolBar("Exit")

        # Add New Entry Action
        add_icon = self.fetch_icon("Add")
        add_action = QAction(add_icon, "Add New", self)
        add_action.setShortcut("Ctrl+O")
        add_action.setStatusTip("Adds New Entry to current Tab")
        # TODO start directory should be dependent on current tab
        add_action.triggered.connect(lambda: self.open_file_browser(start_dir=""))
        toolbar.addAction(add_action)


        # Add Tab
        add_tab_icon = self.fetch_icon("NewTab")
        add_tab_action = QAction(add_tab_icon , "Add New Tab", self)
        add_tab_action.setStatusTip("Adds New Custom Tab")
        add_tab_action.triggered.connect(lambda: self.add_tab())
        toolbar.addAction(add_tab_action)

        # Delete tab
        delete_tab_icon = self.fetch_icon("Trash")
        delete_tab_action = QAction(delete_tab_icon , "Delete Current Tab", self)
        delete_tab_action.setStatusTip("Deletes Current Tab")
        delete_tab_action.triggered.connect(lambda: self.remove_current_tab())
        toolbar.addAction(delete_tab_action)

        # TABS
        self.tab_widget = MyTabsWidget(self)
        self.setCentralWidget(self.tab_widget)


    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display_version_info(self):
        QMessageBox.information(self, "DCC ContentBrowser Version Info", "DCC Content Browser {0}".format(self.version))

    def open_file_browser(self, start_dir):
        QFileDialog.getOpenFileName(self, "Open File", path_utils.return_formatted_path(start_dir))
        self.statusBar().showMessage("Adding : {0}".format("TestProp"))

    def fetch_icon(self, icon_name):
        icon_type = qt_utils.icons_dict(icon_name)
        return self.style().standardIcon(getattr(QStyle, icon_type))

    def delete_entry(self):
        # TODO implement removal of entry in content browser and metadata file
        self.statusBar().showMessage("Removing : {0}".format("TestProp"))

    def add_tab(self):
        # TODO implement the adding of tabs dynamically
        # ask user for the name of the new tab
        new_tab_label, pressed = QInputDialog.getText(self, "New Tab", "New Tab Name: ", QLineEdit.Normal, "")
        # create new tab
        if pressed and new_tab_label:
            self.tab_widget.add_tab(new_tab_label)
        else:
            return

    def remove_current_tab(self):
        self.tab_widget.remove_current_tab()


class MyTabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Tabs layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.icon_horizontal_max = 4

        # Tabs Parent
        self.tabs = QTabWidget()

        # TODO implement custom tab widget class to allow dynamic tab creation/deletion
        # Create first tab
        self.tab = QWidget()

        # Set tabs layout
        self.tab.layout = QVBoxLayout()
        self.tab.setLayout(self.tab.layout)

        # Creating tab's widget container for scroll area
        self.tab_widget_container = QWidget()
        self.tab_widget_container.setAcceptDrops(True)

        # Tab widget layout
        self.tab_widget_container.layout = QGridLayout()
        self.tab_widget_container.setLayout(self.tab_widget_container.layout)

        # Setting spacing between each icon/widget
        self.tab_widget_container.layout.setHorizontalSpacing(20)
        self.tab_widget_container.layout.setVerticalSpacing(20)

        # Processing Entries
        self.add_entries()

        # Defining Scroll Area for tab
        self.tab_scroll_area = QScrollArea()
        self.tab_scroll_area.setGeometry(QRect(0, 0, 200, 200))
        self.tab_scroll_area.setWidget(self.tab_widget_container)

        # Adding tab's widget container
        self.tab.layout.addWidget(self.tab_scroll_area)


        # Add tabs
        self.tabs.addTab(self.tab, "Local")
        self.layout.addWidget(self.tabs)


    def add_entries(self):
        test = ["hello", "I", "Had", "No", "Idea", "More", "Entries", "Oh Yes",
                "hello", "I", "Had", "No", "Idea", "More", "Entries", "Oh Yes",
                "hello", "I", "Had", "No", "Idea", "More", "Entries", "Oh Yes",
                "hello", "I", "Had", "No", "Idea", "More", "Entries", "Oh Yes",
                "hello", "I", "Had", "No", "Idea", "More", "Entries", "Oh Yes",
                "hello", "I", "Had", "No", "Idea", "More", "Entries", "Oh Yes"]
        columns = self.icon_horizontal_max

        if len(test) != 0:
            if len(test) % self.icon_horizontal_max != 0:
                rows = int(len(test) / self.icon_horizontal_max) + 1
            else:
                rows = int(len(test) / self.icon_horizontal_max)
        else:
            return

        positions = [(i, j) for i in range(rows) for j in range(columns)]
        for position, name in zip(positions, test):
            button = MyCustomIconWidget("voronoi.png")
            button.setToolTip('This is a <b>QPushButton</b> widget' + str(position))
            self.tab_widget_container.layout.addWidget(button, *position)


    def add_tab(self, new_name):
        new_tab = QWidget()
        self.tabs.addTab(new_tab, new_name)

    def remove_current_tab(self):
        # TODO implement removal of currently selected tab
        return


class MyCustomIconWidget(QLabel):
    #TODO raise borders, make selectable, read meta, aff
    def __init__(self, icon_name):
        super().__init__()
        # Drag and Drops
        self.setAcceptDrops(True)

        # Getting icon pixmap
        self.icon_pixmap = self.get_icon(icon_name, pixmap=True, w=100, h=100)
        self.setPixmap(self.icon_pixmap)

    # provides signal as dragging action enters it
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("text/plain"):
            print("dragEnterEvent")
            e.accept()
        else:
            e.ignore()

    # triggers on drop
    def dropEvent(self, e):
        print("dropEvent")

    # provides signal as dragging action enters it
    def dragMoveEvent(self, e):
        print("dragMovement")

    # triggers when drag object leaves screenspace of widget
    def dragLeaveEvent(self, e):
        print("dragLeaveEvent")
        self.setPixmap(self.icon_pixmap)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('LeftMousePressed')
        if e.button() == Qt.RightButton:
            print('RightMousePressed')

    def get_icon(self, icon_name, pixmap=True, icon=False, w=100, h=100):
        if icon:
            icon_type = qt_utils.icons_dict(icon_name)
            return self.style().standardIcon(getattr(QStyle, icon_type))
        elif pixmap:
            icon_pixmap = QPixmap(path_utils.return_icon_path(icon_name))
            return icon_pixmap.scaled(w, h, Qt.KeepAspectRatio)




if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ContentBrowserUI()
    sys.exit(app.exec_())
