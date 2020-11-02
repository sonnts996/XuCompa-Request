from PyQt5.QtCore import Qt, QRect
from PyQt5.QtWidgets import QWidget, QPushButton, QHBoxLayout, QVBoxLayout, QToolButton

from xu.compa.Parapluie import PSticky, Parapluie, PResource
from xu.src.python import Utilities
from xu.src.python.Module.ParamEditor import ParamEditor, ParamType
from xu.src.res.app import appInformation


class About(PSticky):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        x = parent.x() + parent.width() / 2 - 200
        y = parent.y() + parent.height() / 2 - 100
        window_rect = QRect(x, y, 400, 245)
        self.setGeometry(window_rect)

        self.tableLink = ParamEditor(ParamType.Param)
        self.tableLink.setHeaderVisible(False)
        self.tableLink.setEditable(False)

        self.closeButton = QToolButton()
        self.closeButton.setObjectName(Parapluie.Object_StickyWindow_FunctionButton)
        self.closeButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Cancel_Svg))
        self.closeButton.pressed.connect(lambda: self.completeDestroy(0))

        self.addWindowAction(self.closeButton)

        self.setCentralWidget(self.tableLink)
        self.setWindowTitle("XuCompa - Request")
        Utilities.Style.applyWindowIcon(self)

        self.tableLink.setData(appInformation.app)
        self.tableLink.refresh()
