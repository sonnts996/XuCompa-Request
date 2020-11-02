from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabBar


class PTabBar(QTabBar):
    def __init__(self):
        super().__init__()
        self.setFocusPolicy(Qt.StrongFocus)
        self.setStyleSheet("background:transparent")

    def wheelEvent(self, event: QtGui.QWheelEvent):
        pass

    # def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
    #     opt = QStyleOption()
    #     opt.initFrom(self)
    #     painter = QPainter(self)
    #     self.style().drawPrimitive(QStyle.PE_FrameTabBarBase, opt, painter, self)
