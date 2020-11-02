from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtWidgets import QTabWidget

from xu.compa.Parapluie.src.ActionWidget.PTabBar import PTabBar


class PTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(PTabWidget, self).__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)
        self.tabB = PTabBar()
        self.tabB.setExpanding(False)
        self.setTabBar(self.tabB)

    def wheelEvent(self, *args, **kwargs):
        pass
