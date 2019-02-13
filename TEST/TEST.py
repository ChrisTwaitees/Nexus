# !/usr/bin/env python
# -*- coding:utf-8 -*-

from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


class overlay(QWidget):
    def __init__(self, parent=None):
        super(overlay, self).__init__(parent)

        palette = QPalette(self.palette())
        palette.setColor(palette.Background, Qt.transparent)

        self.setPalette(palette)

    def paintEvent(self, event):
        painter = QPainter()
        painter.begin(self)
        painter.setRenderHint(QPainter.Antialiasing)
        painter.fillRect(event.rect(), QBrush(QColor(255, 255, 255, 127)))
        painter.drawLine(self.width() / 8, self.height() / 8, 7 * self.width() / 8, 7 * self.height() / 8)
        painter.drawLine(self.width() / 8, 7 * self.height() / 8, 7 * self.width() / 8, self.height() / 8)
        painter.setPen(QPen(Qt.NoPen))


class windowOverlay(QWidget):
    def __init__(self, parent=None):
        super(windowOverlay, self).__init__(parent)

        self.editor = QTextEdit()
        self.editor.setPlainText("OVERLAY" * 100)

        self.button = QPushButton("Toggle Overlay")

        self.verticalLayout = QVBoxLayout(self)
        self.verticalLayout.addWidget(self.editor)
        self.verticalLayout.addWidget(self.button)

        self.overlay = overlay(self.editor)
        self.overlay.hide()

        self.button.clicked.connect(
            lambda: self.overlay.setVisible(False) if self.overlay.isVisible() else self.overlay.setVisible(True))

    def resizeEvent(self, event):
        self.overlay.resize(event.size())
        event.accept()


if __name__ == "__main__":
    import sys

    app = QApplication(sys.argv)
    main = windowOverlay()
    main.show()
    sys.exit(app.exec_())