"""
Nexus
DCC Independent Content Browser

Author: Chris Thwaites
Github: https://github.com/ChrisTwaitees
"""
import sys
import os
import webbrowser
from utils import path_utils
from utils.gui_utils import pyqt_utils
from data.nexus_metadata import nexus_metadata as nxs
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class NXS_UI(QMainWindow):
    def __init__(self):
        super(NXS_UI, self).__init__()

        # GLOBALS
        self.version = "v0.1"
        self.docs = "https://github.com/ChrisTwaitees/Nexus/blob/master/README.md"
        self.width = 750.0
        self.height = 500.0
        self.icon_size = 100

        # BUILD
        self.create_UI()
        self.create_menu_bar()
        self.create_widgets()
        pyqt_utils.set_stylesheet(self, "darkorange")

        # LOAD DATA
        self.load_nxs_data()

        # SHOW
        self.show()

    def create_UI(self):
        # Construction
        self.setWindowTitle('NXS Content Browser')
        self.setWindowFlags(
            Qt.WindowStaysOnTopHint
        )

        self.setMinimumSize(self.width, self.height)
        self.center()

    def create_menu_bar(self):
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

        # INFO MENU
        info_menu = menubar.addMenu('&Info')

        # Help Action
        help_icon = self.fetch_icon("Help")
        help_act = QAction(help_icon, '&Open Support Page', self)
        help_act.setShortcut('Ctrl+H')
        help_act.setStatusTip("Open Tool's Support Page")
        help_act.triggered.connect(lambda: self.open_webbrowser(self.docs))
        info_menu.addAction(help_act)


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

        # Refresh TABS and Tree
        refresh_icon = self.fetch_icon("Refresh")
        refresh_action = QAction(refresh_icon, "Refresh Nexus", self)
        refresh_action.setStatusTip("Refreshes Nexus")
        refresh_action.triggered.connect(lambda: self.refresh())
        toolbar.addAction(refresh_action)

    def create_widgets(self):
        # WIDGETS
        # widgets container
        self.widgets_container = QWidget()
        self.widgets_container.layout = QHBoxLayout()
        self.widgets_container.setLayout(self.widgets_container.layout)

        # tree browser widget
        self.tree_browser = NXSTreeBrowserWidget()

        # tabs widget
        self.tabs_widget = NXSTabsWidget(self)

        # adding widgets to widgets container
        self.widgets_container.layout.addWidget(self.tree_browser)
        self.widgets_container.layout.addWidget(self.tabs_widget)

        # initializing tabs
        self.setCentralWidget(self.widgets_container)

    def load_nxs_data(self):
        # Load NXS Metadata
        nxs_data = nxs.NexusMetaData().get_metadata()
        # Clear Tabs Layout
        pyqt_utils.delete_widgets_in_layout(self.tabs_widget)
        self.tabs_widget.tabs = QTabWidget()
        # Building Tabs from Data
        if len(nxs_data.keys()):
            for tab in nxs_data.keys():
                new_tab = NXSTabWidget(parent=self.tabs_widget, name=tab)
                self.tabs_widget.tabs.addTab(new_tab, tab)
                for group in nxs_data[tab].keys():
                    new_group = NXSGroupWidget(self.tabs_widget, group_name=group,
                                               tab_name=tab)
                    new_tab.widget_container.layout.addWidget(new_group)
                    entries = nxs_data[tab][group].keys()
                    new_group.add_entries(entries, tab_name=tab, group_name=group)
        self.tabs_widget.layout.addWidget(self.tabs_widget.tabs)

    def refresh(self):
        self.load_nxs_data()
        self.tree_browser.refresh()

    def center(self):
        qr = self.frameGeometry()
        cp = QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def display_version_info(self):
        QMessageBox.information(self, "ContentBrowser Version Info", "DCC Content Browser {0}".format(self.version))

    def open_file_browser(self, start_dir):
        QFileDialog.getOpenFileName(self, "Open File", path_utils.get_os_path(start_dir))
        self.statusBar().showMessage("Adding : {0}".format("TestProp"))

    def fetch_icon(self, icon_name):
        icon_type = pyqt_utils.icons_dict(icon_name)
        return self.style().standardIcon(getattr(QStyle, icon_type))

    def open_webbrowser(self, url):
        webbrowser.open(url, new=0, autoraise=1)


class NXSTreeBrowserWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.title = "NEXUS BROWSER: "
        self.width = 300
        self.icon_size = 20
        self.collapsed = False
        self.create_layout()

    def create_layout(self):

        # layout
        self.layout = QVBoxLayout()
        self.layout.setContentsMargins(5,5,5,5)
        self.setLayout(self.layout)
        self.setMaximumWidth(self.width)

        # Header and Collapsible
        self.create_arrowed_header()

        # NEXUS
        self.nxs_tree = QTreeView()
        self.nxs_tree.model = QStandardItemModel()
        self.nxs_tree.model.setHorizontalHeaderLabels([self.tr("Nexus Items")])

        self.add_items(self.nxs_tree.model)
        self.nxs_tree.setModel(self.nxs_tree.model)
        self.layout.addWidget(self.nxs_tree)

    def create_arrowed_header(self):
        # collapse icons
        self.leftArrow = pyqt_utils.get_icon(self, "ArrowLeft")
        self.rightArrow = pyqt_utils.get_icon(self, "ArrowRight")

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
        if self.nxs_tree.model.hasChildren():
            self.nxs_tree.model.removeRows(0, self.nxs_tree.model.rowCount())
        self.add_items(self.nxs_tree.model)


class NXSTabsWidget(QWidget):
    def __init__(self, parent):
        super(QWidget, self).__init__(parent)
        self.parent = parent

        # Tabs layout
        self.layout = QVBoxLayout(self)
        self.setLayout(self.layout)

        # Icons
        self.icon_horizontal_max = 4
        self.icon_size = parent.icon_size
        self.icon_spacing = 10

        # Dimensions
        self.minimum_width = (self.icon_horizontal_max * self.icon_size) + (
                    self.icon_horizontal_max * self.icon_spacing)

        # Tabs Parent
        self.tabs = QTabWidget()

        # Add tabs
        self.layout.addWidget(self.tabs)

        self.tab_index = None

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.RightButton:
            # right - click menu
            right_click_menu = QMenu('Add', self)

            # menu actions
            add_tab_action = QAction("Add new Tab...", self)
            add_tab_action.triggered.connect(lambda: self.add_tab(user=True))
            right_click_menu.addAction(add_tab_action)

            remove_tab_action = QAction("Remove Tab...", self)
            remove_tab_action.triggered.connect(lambda: self.remove_tab(user=True))
            right_click_menu.addAction(remove_tab_action)

            rename_tab_action = QAction("Rename Tab...", self)
            rename_tab_action.triggered.connect(lambda: self.rename_tab(user=True))
            right_click_menu.addAction(rename_tab_action)

            # Returning widget at click position
            try:
                tab_bar_widget = QApplication.widgetAt(QCursor.pos())  # fetch tab widget from clickpos
                self.tab_index = tab_bar_widget.tabAt(e.pos())
                # execute right click menu
                right_click_menu.exec_(QCursor.pos())
            except:
                pass

    def add_tab(self, tab_name="", user=False):
        # TODO: Update the nxs data with new tab
        nxs_data = nxs.NexusMetaData()
        if user:
            tab_name = pyqt_utils.get_user_text(self.parent, header="New Tab",
                                                label="Enter New Tab Name:")
            if tab_name[1] and len(tab_name[0]):
                tab_name = tab_name[0]
                nxs_data.add_new_tab(tab_name)
                self.tabs.addTab(NXSTabWidget(self, tab_name), tab_name)
                self.parent.tree_browser.refresh()
            else:
                return
        else:
            nxs_data.add_new_tab(tab_name)
            self.tabs.addTab(NXSTabWidget(self, tab_name))

    def remove_tab(self, tab_name="", user=False):
        nxs_data = nxs.NexusMetaData()
        if user:
            tab_widget = self.tabs.widget(self.tab_index)
            tab_name = tab_widget.tab_name
            # ask user if they are sure
            msg = QMessageBox()
            msg.setIcon(QMessageBox.Warning)

            msg.setWindowFlags(Qt.WindowStaysOnTopHint)
            msg.setWindowTitle("Delete Tab Confirmation")
            msg.setText("Are you sure you want to delete: %s?" % tab_name)
            msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

            if msg.exec_() == QMessageBox.Yes:
                tab_widget = self.tabs.widget(self.tab_index)
                tab_name = tab_widget.tab_name
                pyqt_utils.delete_widgets_in_layout(tab_widget)
                nxs_data.remove_tab(tab_name)
                self.tabs.removeTab(self.tab_index)
                self.parent.refresh()
            else:
                return
        else:
            # TODO: implement delete of tab through referencing
            self.tabs.addTab(NXSTabWidget(self.parent, tab_name))

    def rename_tab(self, tab_name="", user=False):
        # TODO: implement renaming tab function
        pass


class NXSTabWidget(QWidget):
    def __init__(self, parent, name):
        super().__init__()
        # Tabs Layout
        self.tab_name = name

        # Inherited
        self.parent = parent
        self.icon_size = parent.icon_size
        self.minimum_width = parent.minimum_width
        self.icon_horizontal_max = parent.icon_horizontal_max

        # Dimensions
        self.setMinimumWidth(self.minimum_width + self.icon_size)

        # Layout
        self.layout = QVBoxLayout()
        self.layout.setAlignment(Qt.AlignTop)
        self.setLayout(self.layout)

        # Widgets container for scrollable area
        self.widget_container = QWidget()
        self.widget_container.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        # Widget Container Layout
        self.widget_container.layout = QVBoxLayout()
        self.widget_container.layout.setAlignment(Qt.AlignTop)
        self.widget_container.setLayout(self.widget_container.layout)

        # Defining Scroll Area for tab
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)

        # Setting scroll area to widget container and
        # Adding to scroll area to layout
        self.scroll_area.setWidget(self.widget_container)

        self.layout.addWidget(self.scroll_area)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.RightButton:
            # right - click menu
            right_click_menu = QMenu('Add', self)

            # menu actions
            add_entry_action = QAction("Add new Group...", self)
            add_entry_action.triggered.connect(lambda: self.add_group())
            right_click_menu.addAction(add_entry_action)
            right_click_menu.exec_(QCursor.pos())

    def add_group(self):
        nxs_data = nxs.NexusMetaData()
        group_name = pyqt_utils.get_user_text(self, header="New Group", label="Enter New Group Name:")
        if group_name[1] and len(group_name[0]):  # checking if user OK and entered a name
            nxs_data.add_new_group(tab_name=self.tab_name, group_name=group_name[0])
            print("adding group: " + group_name[0] + " to tab: " + self.tab_name)
            self.widget_container.layout.addWidget(NXSGroupWidget(self, self.tab_name, group_name[0]))
            self.parent.parent.tree_browser.refresh()
        else:
            return


class NXSGroupWidget(pyqt_utils.SimpleCollapsibleWidget):
    def __init__(self, parent, tab_name, group_name):
        super(NXSGroupWidget, self).__init__(group_name)
        print("Initializing group: " + group_name)
        # Attributes
        self.parent = parent
        self.tab_name = tab_name
        self.group_name = group_name
        self.icon_size = parent.icon_size
        self.minimum_width = parent.minimum_width

        # Build
        self.construction()
        self.create_layout()
        self.create_widgets()

    def construction(self):
        self.setMinimumHeight(self.icon_size + self.icon_size * 0.5)
        self.original_height = self.icon_size + self.icon_size * 0.5
        self.setMinimumWidth(self.minimum_width)
        self.setSizePolicy(QSizePolicy.Minimum, QSizePolicy.Minimum)
        self.setSizePolicy(QSizePolicy.MinimumExpanding, QSizePolicy.MinimumExpanding)
        self.setAcceptDrops(True)

    def create_layout(self):
        # Layout
        self.layout = QVBoxLayout()
        self.setLayout(self.layout)

    def create_widgets(self):
        # Icons Widget
        self.icons_widget = QWidget()
        self.icons_widget.setAcceptDrops(True)
        self.icons_widget.setSizePolicy(QSizePolicy.Maximum, QSizePolicy.Maximum)
        self.icons_widget.layout = QGridLayout()
        self.icons_widget.setLayout(self.icons_widget.layout)

        # Scroll Area
        self.scroll_area = QScrollArea()
        self.scroll_area.setWidgetResizable(True)
        self.scroll_area.setWidget(self.icons_widget)

        # Adding Widgets
        self.layout.addWidget(self.scroll_area)

        # Highlight Widget
        self.highlight = pyqt_utils.HighlightWidget(self, alpha=125)

    # MOUSE CLICK HANDLERS

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.RightButton:
            # right - click menu
            right_click_menu = QMenu('Add', self)

            # menu actions
            # add new entry action
            add_entry_action = QAction("Add New Entry...", self)
            add_entry_action.triggered.connect(lambda: self.right_click_add_entry(start_dir=path_utils.get_icon_path()))
            right_click_menu.addAction(add_entry_action)

            # remove group action
            remove_group_action = QAction("Remove Group", self)
            remove_group_action.triggered.connect(lambda: self.right_click_remove_group())
            right_click_menu.addAction(remove_group_action)

            right_click_menu.exec_(QCursor.pos())

    # DRAG AND DROP
    def dragEnterEvent(self, e):
        if e.mimeData().hasUrls:
            e.accept()
            self.highlight.show()
            print("EnterEvent")
        else:
            print("EnterEvent")
            e.ignore()

    def dragLeaveEvent(self, e):
        e.accept()
        self.highlight.hide()

    def dropEvent(self, e):
        if e.mimeData().hasUrls:
            e.setDropAction(Qt.CopyAction)
            e.accept()
            for url in e.mimeData().urls():
                path = str(url.toLocalFile())
                print("Adding %s" % path)
            self.highlight.hide()
        else:
            e.ignore()

    def resizeEvent(self, e):
        self.highlight.resize(e.size())
        e.accept()

    # FUNCTIONS

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
            browser_icon = NXSIconWidget(self, tab_name=tab_name, group_name=group_name, entry_name=name)
            self.icons_widget.layout.addWidget(browser_icon, *position)

    def add_new_entry(self, file_path=""):
        entry_name = path_utils.get_file_name(file_path)
        nxs_data = nxs.NexusMetaData()
        nxs_data.add_new_entry(self.tab_name, self.group_name, file_path)
        # new_icon = NXSIconWidget(self, tab_name=self.tab_name, group_name=self.group_name,
        #                           entry_name=entry_name)
        # self.icons_widget.addWidget(new_icon)
        # TODO: implement layout correcting function
        pass

    def right_click_add_entry(self, start_dir=""):
        filepath = QFileDialog.getOpenFileName(self, "Open File", path_utils.get_os_path(start_dir))[0]
        self.add_new_entry(filepath)

    def right_click_remove_group(self):
        # Ask user if they are sure
        msg = QMessageBox()
        msg.setIcon(QMessageBox.Warning)
        msg.setWindowFlags(Qt.WindowStaysOnTopHint)
        msg.setWindowTitle("Delete Group Confirmation")
        msg.setText("Are you sure you want to delete: %s?" % self.group_name)
        msg.setStandardButtons(QMessageBox.Yes | QMessageBox.Cancel)

        if msg.exec_() == QMessageBox.Yes:

            nxs_data = nxs.NexusMetaData()

            nxs_data.remove_group(self.tab_name, self.group_name)
            print("Removed group %s" % self.group_name)
            pyqt_utils.delete_widgets_in_layout(self.icons_widget)
            self.setParent(None)
            self.deleteLater()
        else:
            return

    def update_layout(self):
        # TODO: Implement updating of row column layout according to icon size and screenspace
        pass


class NXSIconWidget(QLabel):
    #TODO raise borders, make selectable, read meta, aff
    def __init__(self, parent, tab_name="", group_name="",
                 entry_name=""):
        super().__init__()
        self.setAcceptDrops(True)
        self.parent = parent
        self.tab_name = tab_name
        self.group_name = group_name
        self.entry_name = entry_name
        self.icon_width = parent.icon_size
        self.icon_height = parent.icon_size

        # inits
        self.last = None
        self.set_metadata()
        self.set_toolTip()
        self.set_aesthetics()
        self.create_icon()

    def set_metadata(self):
        entry_dict = nxs.NexusMetaData().get_entry(self.tab_name, self.group_name, self.entry_name)
        print("adding new entry: %s" % self.entry_name)
        self.icon = entry_dict["icon"]
        self.source_file = entry_dict["source_file"]
        self.metadata = entry_dict["metadata"]
        self.file_extension = entry_dict["file_extension"]

    def set_toolTip(self):
        toolTip = "<b>{0}<b>\n<b>Source Location:<b> {1}\n<b>Extension:<b> {2}".format(self.entry_name,
                                                                                       self.source_file,
                                                                                       self.file_extension)
        self.setToolTip(toolTip)

    def set_aesthetics(self):
        # Setting Size
        self.setFixedSize(self.icon_width, self.icon_height)

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

    def create_icon(self):
        # Setting default icon pixmap
        self.default_icon_pixmap = self.get_icon(self.icon, pixmap=True, w=self.icon_width, h=self.icon_height)
        #TODO establish better method for protecting original icon, QPainter seems to override
        self.protected_default_icon_pixmap = self.get_icon(self.icon, pixmap=True, w=self.icon_width, h=self.icon_height)

        self.setPixmap(self.default_icon_pixmap)

        # Creating Highlight Overlay
        self.highlight_pixmap = QPixmap(self.default_icon_pixmap.width(), self.default_icon_pixmap.height())
        self.highlight_pixmap.fill(self.highlight_colour)

        # Using QPainter in Color Dodge to create overlayed highlight of icon
        self.highlight_painter = QPainter()
        self.highlight_painter.begin(self.default_icon_pixmap)
        self.highlight_painter.setCompositionMode(QPainter.CompositionMode_ColorDodge)
        self.highlight_painter.setOpacity(self.highlight_opacity )
        self.highlight_painter.drawPixmap(0,0,self.highlight_pixmap)
        self.highlight_painter.end()

    # MOUSE CLICK HANDLING

    def mousePressEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.last = "Left Click"
            self.drag_start_position = e.pos()
        if e.button() == Qt.RightButton:
            self.last = "Right Click"
            self.drag_start_position = e.pos()

    def mouseReleaseEvent(self, e):
        if self.last == "Left Click":
            QTimer.singleShot(QApplication.instance().doubleClickInterval(),
                                 self.single_left_click_action)
        elif self.last == "Right Click":
            self.single_right_click_action()
        else:
            pass

    def mouseDoubleClickEvent(self, e):
        if e.button() == Qt.LeftButton:
            self.last = "Double Left Click"
            print(self.last)

    def single_left_click_action(self):
        if self.last == "Left Click":
            print(self.last)

    def single_right_click_action(self):
        if self.last == "Right Click":
            # right - click menu
            right_click_menu = QMenu('Add', self)

            # menu actions
            # Change Icon
            change_icon_menu = QMenu("Change Icon...")
            change_icon_screengrab = QAction("Use the snipping tool", self)
            change_icon_screengrab.triggered.connect(lambda: self.take_screenshot())
            change_icon_file = QAction("Choose file from directory...")
            change_icon_file.triggered.connect(lambda: self.open_file_browser(start_dir=self.icon_location))
            change_icon_menu.addAction(change_icon_screengrab)
            change_icon_menu.addAction(change_icon_file)
            right_click_menu.addMenu(change_icon_menu)

            # Delete Entry
            delete_entry_action = QAction("Delete Entry...", self)
            delete_entry_action.triggered.connect(lambda: self.delete_entry())
            right_click_menu.addAction(delete_entry_action)

            # Go to Local File Location
            open_file_browser = QAction('Open Local File Directory', self)
            open_file_browser.triggered.connect(lambda: self.open_file_browser(start_dir=self.source_file))
            right_click_menu.addAction(open_file_browser)

            right_click_menu.exec_(QCursor.pos())

    # MOUSE HOVERS
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

        # TODO: MimeData handler depending on icon's metadata
        mimedata = QMimeData()
        mimedata.setText(self.source_file)

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
    def dragEnterEvent(self, e):
        self.setStyleSheet(self.highlighted_style_sheet)
        self.setPixmap(self.default_icon_pixmap)
        print("dragEnterEvent")

    def dragLeaveEvent(self, e):
        print("drag leave event")
        self.setStyleSheet(self.default_style_sheet)
        self.setPixmap(self.protected_default_icon_pixmap)

    # DRAG AND DROP - DROP
    def dropEvent(self, e):
        print("dropEventTriggered" * 40)

    # UTILITIES

    def take_screenshot(self):
        # TODO implement legitimate screenshot method
        img = QApplication.primaryScreen().grabWindow(0)
        img.scaled(100,100, Qt.KeepAspectRatio)
        self.setPixmap(img)

    def get_icon(self, icon_name, pixmap=True, icon=False, w=100, h=100):
        if icon:
            icon_type = pyqt_utils.icons_dict(icon_name)
            return self.style().standardIcon(getattr(QStyle, icon_type))
        elif pixmap:
            icon_pixmap = QPixmap(path_utils.get_icon_path(icon_name))
            return icon_pixmap.scaled(w, h, Qt.KeepAspectRatio)

    def open_file_browser(self, start_dir):
        if os.path.exists(start_dir):
            QFileDialog.getOpenFileName(self, "Open File", path_utils.get_os_path(start_dir))
        else:
            print("path to: %s , does not exist please look at nxs data" % start_dir)

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
    ex = NXS_UI()
    sys.exit(app.exec_())
