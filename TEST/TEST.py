import sys
from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc

from utils import path_utils
from utils import qt_utils

from PyQt5.QtCore import (Qt, QMimeData, QRect)
from PyQt5.QtGui import (QFont, QIcon, QDrag, QPixmap)
from PyQt5.QtWidgets import (QToolTip,
                             QPushButton, QApplication, QDesktopWidget, QMainWindow, QWidget,
                             qApp, QAction, QMessageBox, QMenu, QFileDialog, QStyle, QTabWidget, QVBoxLayout,
                             QInputDialog,  QLineEdit, QGridLayout, QScrollArea, QLabel, QFrame)

class TestUI(qw.QMainWindow):
    def __init__(self):
        super().__init__()
        self.initUI()
        self.setCentralWidget(self.widget_container)
        self.center()
        self.show()

    def initUI(self):
        # construction
        self.setWindowTitle("TestWindow")
        self.setGeometry(500, 500, 500, 500)

        # parent widget container
        self.widget_container = qw.QWidget()
        self.widget_container.layout = qw.QVBoxLayout()
        self.widget_container.setLayout(self.widget_container.layout)

        self.label = MyCustomLabelWidget("voronoi.png")
        self.label = QLabel()
        self.icon_pixmap = QPixmap(path_utils.return_icon_path("voronoi.png"))
        self.label.setPixmap(self.icon_pixmap)


        self.widget_container.layout.addWidget(self.label)


    def center(self):
        qr = self.frameGeometry()
        cp = qw.QDesktopWidget().availableGeometry().center()
        qr.moveCenter(cp)
        self.move(qr.topLeft())

    def printMessage(self, message):
        print(message)


class MyCustomLabelWidget(QLabel):
    def __init__(self,  icon_name):
        super().__init__()
        icon_pixmap = QPixmap(path_utils.return_icon_path(icon_name))
        self.setPixmap(icon_pixmap)


    # provides signal as dragging action enters it
    def dragEnterEvent(self, e):
        if e.mimeData().hasFormat("text/plain"):
            add_icon = self.fetch_icon("Add")
            self.setIcon(add_icon)
            e.accept()
        else:
            e.ignore()

    # triggers on drop
    def dropEvent(self, e):
        self.setText(e.mimeData().text())

    # provides signal as dragging action enters it
    def dragMoveEvent(self, e):
        pass

    # triggers when drag object leaves screenspace of widget
    def dragLeaveEvent(self, e):
        self.setIcon(self.defaultIcon)

    def mousePressEvent(self, e):
        super().mousePressEvent(e)
        if e.button() == Qt.LeftButton:
            print('press')

    def fetch_icon(self, icon_name):
        icon_type = qt_utils.icons_dict(icon_name)
        return self.style().standardIcon(getattr(QStyle, icon_type))




if __name__ == "__main__":
    app = qw.QApplication(sys.argv)
    ex = TestUI()
    sys.exit(app.exec())
