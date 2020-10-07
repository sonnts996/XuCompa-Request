from PyQt5 import QtCore
from PyQt5.QtCore import QSize, QTimer, Qt
from PyQt5.QtWidgets import QWidget, QToolButton, QLabel, QSizePolicy, QDialog

from xu.compa.Parapluie import Parapluie, PResource
from xu.compa.Parapluie.src.StickyWindow.PSticky import PSticky


class PAlert(PSticky):

    def __init__(self, parent: QWidget, tpe: str = Parapluie.Alert_Information):
        super(QDialog, self).__init__(parent)
        super().__init__(parent, inner=True)

        self.setWindowFlags(Qt.FramelessWindowHint | Qt.SubWindow)

        self.setMaximumWidth(300)
        self.setMinimumWidth(300)
        self.setFixedWidth(300)
        self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.installEventFilter(self)

        self.alertType = tpe
        self.timer = None
        self.time = -1
        self._inHiddenMode__ = True

        if self.alertType == Parapluie.Alert_Error:
            self.setObjectName(Parapluie.Object_Alert_Error)
        elif self.alertType == Parapluie.Alert_Warning:
            self.setObjectName(Parapluie.Object_Alert_Warning)
        else:
            self.setObjectName(Parapluie.Object_Alert_Information)

        close = QToolButton()
        close.setObjectName(Parapluie.Object_StickyWindow_FunctionButton)
        close.setIconSize(QSize(12, 12))
        close.setIcon(PResource.defaultIcon(Parapluie.Icon_Cancel_Svg))
        close.pressed.connect(self.close)
        self.addWindowAction(close)

        self.message = QLabel()
        self.message.setWordWrap(True)
        self.message.setContentsMargins(8, 8, 8, 8)

        self.setCentralWidget(self.message)

    def setMessage(self, *msg, sep=" "):
        if len(msg) > 1:
            data = ""
            for s in msg:
                if isinstance(s, str):
                    data = data + s + sep
                else:
                    if msg.index(s) != len(msg) - 1:
                        data = data + str(s) + sep
                    else:
                        data = data + str(s)
        elif len(msg) == 1:
            data = str(msg[0])
        else:
            data = ""

        self.message.setText(data)

    def setInHideMode(self, hide: bool):
        self._inHiddenMode__ = hide

    def inHideMode(self):
        return self._inHiddenMode__

    def setAutoClose(self, time: int):
        self.time = time
        if self.timer is None and time > 0:
            self.timer = QTimer()
            self.timer.timeout.connect(self.closeAlert)
            self.timer.start(time)

    def closeAlert(self):
        if self.timer is not None and self.time > 0:
            self.close()
        elif self.timer is None and self.time > 0:
            self.setAutoClose(self.time)

    def eventFilter(self, a0: QtCore.QObject, a1: QtCore.QEvent):
        if a1.type() == QtCore.QEvent.MouseButtonRelease:
            self.timer = None

        return super(PAlert, self).eventFilter(a0, a1)

    def minimizedFollowParent(self):
        if not self.inHideMode():
            super(PAlert, self).minimizedFollowParent()
