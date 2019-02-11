from utils.gui_utils import pyqt_utils

from PyQt5 import QtWidgets as qw
from PyQt5 import QtGui as qg
from PyQt5 import QtCore as qc
class TestWindow(pyqt_utils.SimpleWindow):
    def __init__(self):
        super(TestWindow, self).__init__("TEST", style="darkorange")
        self.test = pyqt_utils.RaisedVBoxWidget()
        header = pyqt_utils.qw.QPushButton("Name")
        header
        self.test.addWidget(header)
        self.grpBox = pyqt_utils.SimpleCollapsibleWidget("Named GroupBox")
        self.grpBox.layout = qw.QVBoxLayout()
        self.grpBox.setLayout(self.grpBox.layout)
        self.testButton = qw.QPushButton("Test")
        self.grpBox.layout.addWidget(self.testButton)





        self.layout.addWidget(self.test)
        self.test.addWidget(self.grpBox)




def main():

    app = pyqt_utils.qw.QApplication(pyqt_utils.sys.argv)
    main_window = TestWindow()
    main_window.show()
    pyqt_utils.sys.exit(app.exec_())

main()

