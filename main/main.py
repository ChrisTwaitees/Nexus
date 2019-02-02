"""
DCC Independent Content Browser

Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
import sys
from utils import path_utils, qt_utils
from nexus_metadata import nexus_metadata as nxs
from PyQt5.QtCore import (Qt, QMimeData, QRect, QByteArray)
from PyQt5.QtGui import (QFont, QIcon, QDrag, QPixmap, QCursor, QPainter, QPalette, QPen, QBrush, QColor, QScreen,
                         QStandardItem, QStandardItemModel)
from PyQt5.QtWidgets import (QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QMainWindow, QWidget,
                             qApp, QAction, QMessageBox, QMenu, QFileDialog, QStyle, QTabWidget, QVBoxLayout,
                             QHBoxLayout, QInputDialog,  QLineEdit, QGridLayout, QScrollArea, QLabel, QFrame, QTreeView,
                             QHeaderView, QFileSystemModel, QSizePolicy)


class ContentBrowserUI(QMainWindow):
    def __init__(self):
        super().__init__()

        self.version = "v0.1"
        self.width = 1000

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
        # stylesheet = \
        #     ".QWidget {\n" \
        #     + "border: 20px solid black;\n" \
        #     + "border-radius: 4px;\n" \
        #     + "background-color: rgb(255, 255, 255);\n" \
        #     + "}"
        # self.setStyleSheet(stylesheet)

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

        # Add from Local Directory Action
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

        # Refresh TABS and Tree
        refresh_icon = self.fetch_icon("Refresh")
        refresh_action = QAction(refresh_icon, "Refresh Nexus", self)
        refresh_action.setStatusTip("Refreshes Nexus")
        refresh_action.triggered.connect(lambda: self.refresh_tabs_and_tree())
        toolbar.addAction(refresh_action)

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

        # initializing tabs
        self.tabs_widget.build_tabs()

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

    def refresh_tabs_and_tree(self):
        self.tabs_widget.build_tabs()


class MyTreeBrowserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "NEXUS BROWSER: "
        self.width = 300
        self.icon_size = 20
        self.collapsed = False
        self.initWidget()

    def initWidget(self):

        # layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)
        self.setLayout(self.layout)
        self.setMaximumWidth(self.width)

        # Header and Collapsible
        self.initCollapsibleHeader()

        # NEXUS
        self.nxs_tree = QTreeView()
        self.nxs_tree.setContextMenuPolicy(Qt.CustomContextMenu)
        self.nxs_tree.customContextMenuRequested.connect(self.open_menu)

        self.nxs_tree.model = QStandardItemModel()
        self.nxs_tree.model.setHorizontalHeaderLabels([self.tr("Nexus Items")])

        self.add_items(self.nxs_tree.model)
        self.nxs_tree.setModel(self.nxs_tree.model)
        self.layout.addWidget(self.nxs_tree)

        # LOCAL
        self.local_tree = QTreeView()
        self.local_tree.model = QFileSystemModel()
        self.local_tree.model.setRootPath("C:/Users/Chris Thwaites/Desktop/IDEs")
        self.local_tree.setModel(self.local_tree.model)
        self.local_tree.setAnimated(True)

        self.layout.addWidget(self.local_tree)

    def initCollapsibleHeader(self):
        # collapse icons
        self.leftArrow = qt_utils.get_icon(self, "ArrowLeft")
        self.rightArrow = qt_utils.get_icon(self, "ArrowRight")

        # header widget
        self.collapsible_header = QWidget()
        self.collapsible_header.setMaximumWidth(self.width)
        # layout
        self.collapsible_header.layout = QHBoxLayout()
        self.collapsible_header.setLayout(self.collapsible_header.layout)

        # header and button widget
        self.collapsible_button = QPushButton()
        self.collapsible_button.clicked.connect(lambda: self.collapse())
        self.collapsible_button.setIcon(self.leftArrow)
        self.collapsible_button.setFixedSize(self.icon_size, self.icon_size)
        self.collapsible_header.layout.addWidget(self.collapsible_button)

        self.header = QLabel(self.title)
        self.collapsible_header.layout.addWidget(self.header)


        # Adding to layout
        self.layout.addWidget(self.collapsible_header)

    def collapse(self):
        if not self.collapsed:
            self.header.setText("")
            self.collapsible_button.setIcon(self.rightArrow)
            self.setMaximumWidth(self.icon_size*3)
            self.collapsed = True
        else:
            self.header.setText(self.title)
            self.collapsible_button.setIcon(self.leftArrow)
            self.setMaximumWidth(self.width)
            self.collapsed = False

    def add_items(self, parent):
        nxs_data = nxs.NexusMetaData().get_metadata()
        if len(nxs_data.keys()):
            for tab in nxs_data.keys():
                tab_name = QStandardItem(tab)
                parent.appendRow(tab_name)
                for group in nxs_data[tab].keys():
                    group_name = QStandardItem(group)
                    tab_name.appendRow(group_name)
                    for entry in nxs_data[tab][group].keys():
                        entry_name = QStandardItem(entry)
                        group_name.appendRow(entry_name)

    def refresh(self):
        # TODO implement refresh function to delete all entries and then re-add
        self.add_items(self.local_tree.model)

    def open_menu(self, position):
        indexes = self.treeView.selectedIndexes()
        if len(indexes) > 0:

            level = 0
            index = indexes[0]
            while index.parent().isValid():
                index = index.parent()
                level += 1

        menu = QMenu()
        if level == 0:
            menu.addAction(self.tr("Edit person"))
        elif level == 1:
            menu.addAction(self.tr("Edit object/container"))
        elif level == 2:
            menu.addAction(self.tr("Edit object"))

        menu.exec_(self.treeView.viewport().mapToGlobal(position))


class MyTabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)

        # Tabs layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)
        self.icon_horizontal_max = 4
        self.icon_size = 125

        self.icon_spacing = 10
        self.minimum_width = (self.icon_horizontal_max * self.icon_size) + (self.icon_horizontal_max * self.icon_spacing)

        # Tabs Parent
        self.tabs = QTabWidget()

        # Add tabs
        self.layout.addWidget(self.tabs)

    def build_tabs(self):
        # TODO implement building of tabs from nxs data
        # first clearing the layout
        qt_utils.delete_widgets_in_layout(self)
        self.tabs = QTabWidget()
        nxs_data = nxs.NexusMetaData().get_metadata()
        if len(nxs_data.keys()):
            for tab in nxs_data.keys():
                new_tab = MyTabWidget(self)
                self.tabs.addTab(new_tab, tab)
                qt_utils.delete_widgets_in_layout(new_tab)
                for group in nxs_data[tab].keys():
                    print("adding groups " + group)
                    new_group = MyGroupWidget(self, group_name=group,
                                              tab_name=tab)
                    new_tab.layout.addWidget(new_group)
                    entries = nxs_data[tab][group].keys()
                    new_group.add_entries(entries, tab_name=tab, group_name=group)
        self.layout.addWidget(self.tabs)

    def add_tab(self, new_name):
        new_tab = QWidget()
        self.tabs.addTab(new_tab, new_name)

    def remove_current_tab(self):
        # TODO implement removal of currently selected tab
        return

    def add_group(self, tab, group_name):
        #TODO implementing adding icons to group within tab
        #TODO consider abstracting goups as a new class
        self.group_widget = QWidget()
        self.group_widget.layout = QGridLayout()


class MyTabWidget(QWidget):
    def __init__(self, parent):
        super().__init__()
        # Tabs Layout
        self.parent = parent
        self.setMinimumWidth(self.parent.minimum_width + self.parent.icon_size)
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

        # Widgets container for scrollable area
        self.widget_container = QWidget()
        self.widget_container.layout = QVBoxLayout()
        self.widget_container.setLayout(self.widget_container.layout)

        # Defining Scroll Area for tab
        self.scroll_area = QScrollArea()

        # Setting scroll area to widget container and
        # Adding to scroll area to layout
        self.scroll_area.setWidget(self.widget_container)
        self.layout.addWidget(self.scroll_area)

    def add_group(self, group_name):
        print("adding group: " + group_name + " to layout")
        self.widget_container.layout.addWidget(MyGroupWidget(self.parent, group_name))


class MyGroupWidget(QWidget):
    def __init__(self, parent, tab_name, group_name):
        super().__init__()
        print("Initializing group: " + group_name)
        # Attributes
        self.parent = parent
        self.tab_name = tab_name
        self.group_name = group_name
        self.icon_size = parent.icon_size
        self.setAcceptDrops(True)

        # Layouts
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)
        self.setMinimumWidth(self.parent.minimum_width)

        # Header
        self.header = QLabel(self.group_name)
        self.header.setMaximumHeight(20)

        # Icons Widget
        self.frame = QFrame()
        self.frame.setFrameStyle(QFrame.Panel | QFrame.Raised)
        # self.frame.setLayout(self.layout)

        # Icons Group
        self.icons_widget = QWidget()
        self.icons_widget.layout = QGridLayout()
        self.icons_widget.setLayout(self.icons_widget.layout)

        # Aesthetics
        self.setStyleSheet("background-color: green;")

        # Adding Widgets
        self.layout.addWidget(self.header)
        self.layout.addWidget(self.icons_widget)
        # self.parent.layout.addWidget(self.frame)

    def add_entries(self, entries, tab_name, group_name):
        columns = self.parent.icon_horizontal_max
        if len(entries) != 0:
            if len(entries) % columns != 0:
                rows = int(len(entries) / self.parent.icon_horizontal_max) + 1
            else:
                rows = int(len(entries) / self.parent.icon_horizontal_max)
        else:
            return
        positions = [(i, j) for i in range(rows) for j in range(columns)]
        for position, name in zip(positions, entries):
            # TODO implement build from metadata
            browser_icon = MyIconWidget(self, tab_name=tab_name, group_name=group_name, entry_name=name)
            self.icons_widget.layout.addWidget(browser_icon, *position)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.RightButton:
            # right - click menu
            right_click_menu = QMenu('Add', self)

            # menu actions
            add_entry_menu = QMenu("Add New Entry...")
            add_entry_action = QAction("Open File Browser", self)
            add_entry_action.triggered.connect(lambda: self.right_click_add_entry(start_dir=path_utils.get_icon_path()))
            add_entry_menu.addAction(add_entry_action)

            right_click_menu.addMenu(add_entry_menu)

            right_click_menu.exec_(QCursor.pos())

            print('RightMousePressed')

    def right_click_add_entry(self, start_dir=""):
        filepath = QFileDialog.getOpenFileName(self, "Open File", path_utils.get_os_path(start_dir))[0]
        self.add_new_entry(filepath)

    def add_new_entry(self, filepath=""):
        pass



class MyIconWidget(QLabel):
    #TODO raise borders, make selectable, read meta, aff
    def __init__(self, parent, tab_name="", group_name="", entry_name=""):
        super().__init__()
        self.setAcceptDrops(True)
        self.parent = parent
        self.tab_name = tab_name
        self.group_name = group_name
        self.entry_name = entry_name
        self.icon_width = parent.icon_size
        self.icon_height = parent.icon_size

        # inits
        self.init_metadata()
        self.set_toolTip()
        self.init_aesthetics()
        self.init_icon()

    def init_metadata(self):
        nxs_data = nxs.NexusMetaData().get_metadata()
        if self.tab_name in nxs_data.keys() and self.group_name in nxs_data[self.tab_name].keys():
            entry_dict = nxs_data[self.tab_name][self.group_name][self.entry_name]
            print(self.entry_name, entry_dict)
            self.icon_name = entry_dict["icon_name"]
            self.icon_location = entry_dict["icon_location"]
            self.owner = entry_dict["owner"]
            self.local_source_file = entry_dict["local_source_file"]
            self.virtual_file_location = entry_dict["virtual_file_location"]
            self.metadata = entry_dict["metadata"]
            self.file_extension = entry_dict["file_extension"]
        else:
            # defaults
            pass

    def set_toolTip(self):
        toolTip = "<b>{0}<b>\n<b>Source Location:<b> {1}\n<b>Extension:<b> {2}".format(self.entry_name,
                                                                                       self.local_source_file,
                                                                                       self.file_extension)
        self.setToolTip(toolTip)

    def init_aesthetics(self):
        # Setting Size
        self.setMaximumWidth(self.icon_width)
        self.setMaximumHeight(self.icon_width)

        # Setting Style Frame
        self.setFrameStyle(QFrame.StyledPanel | QFrame.Sunken)

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
