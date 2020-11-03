from PyQt5 import QtCore
from PyQt5.QtCore import QSize
from PyQt5.QtWidgets import QToolButton

from xu.compa.Parapluie import Parapluie, PResource


class PClose(QToolButton):
    def __init__(self):
        super().__init__()
        self.setIconSize(QSize(12, 12))
        self.setObjectName(Parapluie.Object_CloseButton)
        self.setIcon(PResource.defaultIcon(Parapluie.Icon_Cancel_Svg))

    def enterEvent(self, a0: QtCore.QEvent):
        self.setIcon(PResource.invertIcon(Parapluie.Icon_Cancel_Svg))

    def leaveEvent(self, a0: QtCore.QEvent):
        self.setIcon(PResource.defaultIcon(Parapluie.Icon_Cancel_Svg))
