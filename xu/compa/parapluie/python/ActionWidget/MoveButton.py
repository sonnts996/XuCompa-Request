from PyQt5.QtCore import QPoint
from PyQt5.QtWidgets import QPushButton, QWidget


class MoveButton(QPushButton):
    _parent_ = None

    def __init__(self, parent: QWidget, **kwargs):
        super().__init__(**kwargs)
        self._parent_ = parent

    def mousePressEvent(self, event):
        self._parent_.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        delta = QPoint(event.globalPos() - self._parent_.oldPos)
        self._parent_.move(self._parent_.x() + delta.x(), self._parent_.y() + delta.y())
        self._parent_.oldPos = event.globalPos()
