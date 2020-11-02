from PyQt5 import QtGui
from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QWidget, QStyleOption, QStyle


class PMoveWidget(QWidget):
    _parent_ = None

    def __init__(self, parent: QWidget, **kwargs):
        super().__init__(**kwargs)
        self._parent_ = parent
        self._movable_ = True

    def mousePressEvent(self, event):
        if self._movable_:
            self._parent_.oldPos = event.globalPos()

    def mouseMoveEvent(self, event):
        if self._movable_:
            delta = QPoint(event.globalPos() - self._parent_.oldPos)
            self._parent_.move(self._parent_.x() + delta.x(), self._parent_.y() + delta.y())
            self._parent_.oldPos = event.globalPos()

    def setMovable(self, movable: bool):
        self._movable_ = movable

    def isMovable(self) -> bool:
        return self._movable_

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)