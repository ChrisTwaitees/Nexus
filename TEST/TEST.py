from utils.gui_utils import pyqt_utils

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
class TestWindow(pyqt_utils.SimpleWindow):
    def __init__(self):
        super(TestWindow, self).__init__("TEST", style="darkorange")
        self.testGroupBox = qw.QGroupBox()
        self.testButton = qw.QPushButton("TEST")
        self.testButton.setMinimumSize(500,500)
        self.scroll = qw.QScrollArea()
        self.group_layout = qw.QVBoxLayout()
        self.testGroupBox.setLayout(self.group_layout)
        self.group_layout.addWidget(self.testButton)
        self.scroll.setWidget(self.testGroupBox)
        self.scroll.setMaximumSize(500,500)
        self.scroll.setWidgetResizable(True)
        self.layout.addWidget(self.scroll)






def main():

    app = pyqt_utils.qw.QApplication(pyqt_utils.sys.argv)
    main_window = TestWindow()
    main_window.show()
    pyqt_utils.sys.exit(app.exec_())

main()

