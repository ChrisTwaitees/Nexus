"""
DCC Independent Content Browser

Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
import sys
from utils import path_utils, qt_utils
from PyQt5.QtCore import (Qt, QMimeData, QRect, QByteArray)
from PyQt5.QtGui import (QFont, QIcon, QDrag, QPixmap, QCursor, QPainter, QPalette, QPen, QBrush, QColor, QScreen)
from PyQt5.QtWidgets import (QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QMainWindow, QWidget,
                             qApp, QAction, QMessageBox, QMenu, QFileDialog, QStyle, QTabWidget, QVBoxLayout,
                             QHBoxLayout, QInputDialog,  QLineEdit, QGridLayout, QScrollArea, QLabel, QFrame, QTreeView)


class ContentBrowserUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.version = "v0.1"
        self.width = 850
        self.height = 650
        self.initUI()
        self.initMenuToolBar()
        self.initWidgets()

        # SHOW
        self.show()

    def initUI(self):
        # Construction
        self.setGeometry(self.width, self.height, self.width, self.height)
        self.center()
        self.setWindowTitle('Content Browser')
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
        )

        # Formatting
        QToolTip.setFont(QFont('SansSerif', 10))

    def initMenuToolBar(self):
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

    def initWidgets(self):
        # WIDGETS
        # widgets container
        self.widgets_container = QWidget()
        self.widgets_container.layout = QHBoxLayout()
        self.widgets_container.setLayout(self.widgets_container.layout)

        # tree browser widget
        self.tree_browser = MyTreeBrowserWidget()

        # tabs widget
        self.tabs_widget = MyTabsWidget(self)

        # adding widgets to widgets container
        self.widgets_container.layout.addWidget(self.tree_browser)
        self.widgets_container.layout.addWidget(self.tabs_widget)

        self.setCentralWidget(self.widgets_container)

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display_version_info(self):
        QMessageBox.information(self, "DCC ContentBrowser Version Info", "DCC Content Browser {0}".format(self.version))

    def open_file_browser(self, start_dir):
        QFileDialog.getOpenFileName(self, "Open File", path_utils.get_os_path(start_dir))
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
            self.tabs_widget.add_tab(new_tab_label)
        else:
            return

    def remove_current_tab(self):
        self.tabs_widget.remove_current_tab()


class MyTreeBrowserWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Entry Browser")
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.tree = QTreeView()
        self.tree.setAnimated(True)

        self.layout.addWidget(self.tree)


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
        self.tab_widget_container.layout.setHorizontalSpacing(10)
        self.tab_widget_container.layout.setVerticalSpacing(10
                                                            )
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
            # TODO implement build from metadata
            browser_icon = MyIconWidget(self, icon_name="voronoi.png")
            browser_icon.setToolTip('This is a <b>QPushButton</b> widget' + str(position))
            self.tab_widget_container.layout.addWidget(browser_icon, *position)

    def add_tab(self, new_name):
        new_tab = QWidget()
        self.tabs.addTab(new_tab, new_name)

    def remove_current_tab(self):
        # TODO implement removal of currently selected tab
        return


class MyIconWidget(QLabel):
    #TODO raise borders, make selectable, read meta, aff
    def __init__(self, parent, icon_name=""):
        super().__init__()
        self.setAcceptDrops(True)
        self.parent = parent
        self.icon_name = icon_name
        self.setText("test")
        self.local_source_file = "G:/Forgotten Snow White/SnowWhite/assets/Dress/dress_Belt.obj"
        self.icon_width = 150
        self.icon_height = 150

        # inits
        self.init_aesthetics()
        self.init_icon()

    def init_aesthetics(self):
        # Setting Aesthetics
        self.highlight_colour = self.palette().color(QPalette.Highlight)
        self.highlight_opacity = 0.23

        # Style Sheets
        self.default_style_sheet = "QLabel {border: 2px solid black;" \
                      "border-radius: 2px;}"
        self.highlighted_style_sheet = "QLabel {border: 4px solid blue;" \
                      "border-radius: 4px;}"
        self.setStyleSheet(self.default_style_sheet)

    def init_icon(self):
        # Drag and Drops


        # Setting default icon pixmap
        self.default_icon_pixmap = self.get_icon(self.icon_name, pixmap=True, w=self.icon_width, h=self.icon_height)
        #TODO establish better method for protecting original icon, QPainter seems to override
        self.protected_default_icon_pixmap = self.get_icon(self.icon_name, pixmap=True, w=self.icon_width, h=self.icon_height)

        self.setPixmap(self.default_icon_pixmap)

        # Creating Highlight Overlay
        self.highlight_pixmap = QPixmap(self.default_icon_pixmap.width(), self.default_icon_pixmap.height())
        self.highlight_pixmap.fill(self.highlight_colour)

        # Using QPainter in Color Dodge to create overlayed highlight of icon
        # TODO implent refresh function in order to update icons when replaced
        self.highlight_painter = QPainter()
        self.highlight_painter.begin(self.default_icon_pixmap)
        self.highlight_painter.setCompositionMode(QPainter.CompositionMode_ColorDodge)
        self.highlight_painter.setOpacity(self.highlight_opacity )
        self.highlight_painter.drawPixmap(0,0,self.highlight_pixmap)
        self.highlight_painter.end()

    # MOUSE PRESS EVENTS
    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            self.drag_start_position = e.pos()
            print('LeftMousePressed')
        if e.button() == Qt.RightButton:
            # right - click menu
            right_click_menu = QMenu('Add', self)

            # menu actions
            # Change Icon
            change_icon_menu = QMenu("Change Icon...")
            change_icon_screengrab = QAction("Use the snipping tool", self)
            change_icon_screengrab.triggered.connect(lambda: self.take_screenshot())
            change_icon_file = QAction("Choose file from directory...")
            change_icon_file.triggered.connect(lambda: self.open_file_browser(start_dir=path_utils.get_icon_path()))
            change_icon_menu.addAction(change_icon_screengrab)
            change_icon_menu.addAction(change_icon_file)
            right_click_menu.addMenu(change_icon_menu)

            # Delete Entry
            delete_entry_action = QAction("Delete Entry...", self)
            delete_entry_action.triggered.connect(lambda: self.delete_entry())
            right_click_menu.addAction(delete_entry_action)

            # Go to Local File Location
            open_file_browser = QAction('Open Local File Directory', self)
            open_file_browser.triggered.connect(lambda: self.open_file_browser(start_dir=""))
            right_click_menu.addAction(open_file_browser)

            # Go to Perforce Virtual Location
            open_perforce_location = QAction('Open Perforce Virtual Location', self)
            open_perforce_location.triggered.connect(lambda: self.open_file_browser(start_dir=""))
            right_click_menu.addAction(open_perforce_location)

            # Go to Icon Location
            open_perforce_location = QAction('Open Icon Source Directory', self)
            open_perforce_location.triggered.connect(lambda: self.open_file_browser(start_dir=path_utils.get_icon_path()))
            right_click_menu.addAction(open_perforce_location)






            right_click_menu.exec_(QCursor.pos())

            print('RightMousePressed')

    # CURSOR HOVERS
    def enterEvent(self, e):
        self.setStyleSheet(self.highlighted_style_sheet)
        self.setPixmap(self.default_icon_pixmap)

    def leaveEvent(self, e):
        self.setStyleSheet(self.default_style_sheet)
        self.setPixmap(self.protected_default_icon_pixmap)



    # DRAG AND DROP - LEAVE
    def mouseMoveEvent(self, e):
        if not (e.buttons() and Qt.LeftButton):
            return
        if (e.pos() - self.drag_start_position).manhattanLength() < QApplication.startDragDistance():
            return
        drag = QDrag(self)


        # TODO handle QMimeData creation depending on datatype
        # csvData = QByteArray()
        # mimedata = QMimeData()
        #
        # with open(self.local_source_file) as source:
        #     data = source.read()
        # mimedata.setData(self.local_source_file, csvData)

        mimedata = QMimeData()
        mimedata.setText(self.local_source_file)

        # Drag and dropping data
        drag.setMimeData(mimedata)
        pixmap = QPixmap(self.size())
        painter = QPainter(pixmap)
        painter.drawPixmap(self.rect(), self.grab())
        painter.end()
        drag.setPixmap(pixmap)
        drag.setHotSpot(e.pos())
        drag.exec_(Qt.CopyAction | Qt.MoveAction)

    # DRAG AND DROP - ENTER
    # provides signal as dragging action enters it
    def dragEnterEvent(self, e):
        self.setStyleSheet(self.highlighted_style_sheet)
        self.setPixmap(self.default_icon_pixmap)
        print("dragEnterEvent")

    def dragLeaveEvent(self, e):
        print("drag leave event")
        self.setStyleSheet(self.default_style_sheet)
        self.setPixmap(self.protected_default_icon_pixmap)

    # triggers on drop
    def dropEvent(self, e):
        print("dropEventTriggered" * 40)

    def take_screenshot(self):
        # TODO implement legitimate screenshot method
        img = QApplication.primaryScreen().grabWindow(0)
        img.scaled(100,100, Qt.KeepAspectRatio)
        self.setPixmap(img)


    def get_icon(self, icon_name, pixmap=True, icon=False, w=100, h=100):
        if icon:
            icon_type = qt_utils.icons_dict(icon_name)
            return self.style().standardIcon(getattr(QStyle, icon_type))
        elif pixmap:
            icon_pixmap = QPixmap(path_utils.get_icon_path(icon_name))
            return icon_pixmap.scaled(w, h, Qt.KeepAspectRatio)


    def open_file_browser(self, start_dir):
        QFileDialog.getOpenFileName(self, "Open File", path_utils.get_os_path(start_dir))

    def refresh_icon(self, icon_name):
        # TODO implement more robust refresh handling
        return

    def delete_entry(self):
        # TODO after removing icon widget, ensure metadata is updated and icon removed
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)

        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("Delete Entry Confirmation")
        msg.setText("Are you sure you want to delete this entry?")

        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)
        if msg.exec_() == QMessageBox.Yes:
            # TODO remove entry from metadata and remove widget from Gridlayout
            print("Removing from entry")
            # Removing widget from parent layout
            self.setParent(None)
            self.deleteLater()
        # TODO reshuffle layout of gridlayout to remove holes in layout
        else:
            return


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = ContentBrowserUI()
    sys.exit(app.exec_())
