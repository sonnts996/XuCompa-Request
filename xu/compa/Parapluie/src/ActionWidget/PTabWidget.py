from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QTabWidget, QSpinBox

from xu.compa.Parapluie.src.ActionWidget.PTabBar import PTabBar


class PTabWidget(QTabWidget):
    def __init__(self, *args, **kwargs):
        super(PTabWidget, self).__init__(*args, **kwargs)
        self.setFocusPolicy(Qt.StrongFocus)
        self.tabB = PTabBar()
        self.tabB.setExpanding(False)
        self.setTabBar(self.tabB)

        self.sizeBox = QSpinBox()
        self.sizeBox.setVisible(False)
        self.sizeBox.valueChanged.connect(self.sizeChanged)
        self.setCornerWidget(self.sizeBox, Qt.TopRightCorner)

    def wheelEvent(self, *args, **kwargs):
        pass

    def setSizeBox(self, min, max, step):
        self.sizeBox.setRange(min, max)
        self.sizeBox.setSingleStep(step)

    def resizable(self, boolean):
        self.sizeBox.setVisible(boolean)

    def sizeChanged(self, value):
        self.setFixedHeight(value)
