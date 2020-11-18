from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QLineEdit


class PEditor(QLineEdit):
    focusSignal = pyqtSignal(bool)

    def __init__(self):
        super().__init__()

    def focusInEvent(self, a0: QtGui.QFocusEvent) -> None:
        super(PEditor, self).focusInEvent(a0)
        self.focusSignal.emit(True)

    def focusOutEvent(self, a0: QtGui.QFocusEvent) -> None:
        super(PEditor, self).focusOutEvent(a0)
        self.focusSignal.emit(False)
