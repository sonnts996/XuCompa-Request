from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle


class PWidget(QWidget):
    resized = pyqtSignal()

    def __init__(self):
        super().__init__()

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        super(PWidget, self).resizeEvent(a0)
        self.resized.emit()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
