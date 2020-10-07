from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QPoint
from PyQt5.QtWidgets import QDialog, QHBoxLayout, QVBoxLayout, QLabel, QSizeGrip, QWidget, QSizePolicy

import xu.compa.Parapluie.src.StickyWindow as Sticky
from xu.compa.Parapluie import Parapluie, PResource, PFunction, PMoveWidget


class PSticky(QDialog):
    closed = pyqtSignal()
    __title_bar_height__ = 32
    __bottom_grip__size__ = 16
    __window_margin__ = 1

    def __init__(self, parent: QWidget, inner: bool = False):
        if not inner:
            super().__init__()

        self.__parent__ = parent
        if self.__parent__ is not None:

            self.__central_widget__ = None
            self.__follow__ = False

            self.HAnchor = Parapluie.HCenter
            self.VAnchor = Parapluie.VCenter

            self.__update_distance__ = False
            self.__const_hDistance__ = False
            self.__const_vDistance__ = False

            self.leftDistance = 0
            self.rightDistance = 0
            self.topDistance = 0
            self.bottomDistance = 0

            PFunction.applyStyle(self, PResource.stylesheet())

            self.setWindowFlags(Qt.FramelessWindowHint)

            self.setObjectName(Parapluie.Object_StickyWindow)

            self.title = QLabel("Parapluie")
            self.title.setStyleSheet("font-size: 14px; font-weight: bold;")
            self.title.setContentsMargins(8, 0, 8, 0)
            self.title.setMinimumHeight(self.__title_bar_height__)

            self.bottom_sizeGrip = QSizeGrip(self)
            self.bottom_sizeGrip.setObjectName(Parapluie.Object_StickyWindow_ResizeBottom)
            self.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

            self.titleBar = QHBoxLayout()
            self.titleBar.setContentsMargins(0, 0, 0, 0)
            self.titleBar.addWidget(self.title, alignment=Qt.AlignLeft | Qt.AlignCenter)
            self.titleBar.addStretch()

            self.moveWidget = PMoveWidget(self)
            self.moveWidget.setObjectName(Parapluie.Object_StickyWindow_FunctionButton)
            self.moveWidget.setLayout(self.titleBar)
            self.moveWidget.setMaximumHeight(self.__title_bar_height__)

            self.mainLayout = QVBoxLayout()
            self.mainLayout.setContentsMargins(self.__window_margin__, self.__window_margin__, self.__window_margin__,
                                               self.__window_margin__)
            self.mainLayout.setSpacing(0)
            self.mainLayout.addWidget(self.moveWidget, alignment=Qt.AlignTop)
            self.mainLayout.addWidget(self.bottom_sizeGrip, alignment=Qt.AlignRight)

            self.setLayout(self.mainLayout)

            if isinstance(parent, Sticky.PWindow):
                self.updateDistance()
                parent.resized.connect(self.followParentRelative)
                parent.closed.connect(self.close)
                parent.minimized.connect(self.minimizedFollowParent)

    def updateDistance(self):
        if self.__parent__ is not None:
            if not self.__const_hDistance__:
                self.leftDistance = self.x() - self.__parent__.x()
                self.rightDistance = (self.x() + self.width()) - self.__parent__.x() - self.__parent__.width()
            if not self.__const_vDistance__:
                self.topDistance = self.y() - self.__parent__.y()
                self.bottomDistance = (self.y() + self.height()) - self.__parent__.y() - self.__parent__.height()

    def moveEvent(self, a0: QtGui.QMoveEvent):
        if self.__parent__ is not None:
            super(PSticky, self).moveEvent(a0)
            if self.__update_distance__:
                self.updateDistance()

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        if self.__parent__ is not None:
            super(PSticky, self).resizeEvent(a0)
            if self.__update_distance__:
                self.updateDistance()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        if self.__parent__ is not None:
            self.completeDestroy(0)
            self.closed.emit()

    def setWindowTitle(self, *args):
        if self.__parent__ is not None:
            super(PSticky, self).setWindowTitle(*args)
            self.title.setText(*args)

    def setCentralWidget(self, widget: QWidget):
        if self.__parent__ is not None:
            self.mainLayout.insertWidget(1, widget)
            self.__central_widget__ = widget
            self.__central_widget__.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

    def addWindowAction(self, button):
        if self.__parent__ is not None:
            self.titleBar.addWidget(button, alignment=Qt.AlignLeft | Qt.AlignTop)

    def setResizable(self, resize=False):
        if self.__parent__ is not None:
            self.bottom_sizeGrip.setVisible(resize and not (self.__const_vDistance__ or self.__const_hDistance__))

    def isResizable(self):
        return self.bottom_sizeGrip.isVisible()

    def setMovable(self, movable: bool):
        if self.__parent__ is not None:
            self.moveWidget.setMovable(movable and not (self.__const_vDistance__ or self.__const_hDistance__))

    def isMovable(self) -> bool:
        return self.moveWidget.isMovable()

    def completeDestroy(self, code: int = 0):
        self.done(code)
        self.__parent__ = None

    def setAnchor(self, hAnchor: int, vAnchor: int, hDistance: int = None, vDistance: int = None):
        if self.__parent__ is not None:
            self.HAnchor = hAnchor
            self.VAnchor = vAnchor
            if hDistance is not None:
                self.leftDistance = hDistance
                self.rightDistance = hDistance
                self.__const_hDistance__ = True
            else:
                self.__const_hDistance__ = False
            if vDistance is not None:
                self.topDistance = vDistance
                self.bottomDistance = vDistance
                self.__const_vDistance__ = True
            else:
                self.__const_vDistance__ = False

            self.setMovable(not (self.__const_vDistance__ or self.__const_hDistance__))
            self.setResizable(not (self.__const_vDistance__ or self.__const_hDistance__))

            self.followParentRelative()

    def enableFollowParentRelative(self) -> bool:
        if self.__parent__ is not None:
            self.__follow__ = isinstance(self.__parent__, Sticky.PWindow)
            if self.__follow__:
                self.setWindowFlags(self.windowFlags() | Qt.WindowStaysOnTopHint)
            return self.__follow__
        return False

    def minimizedFollowParent(self):
        if self.__parent__ is not None:
            minimize = self.__parent__.isMinimized()
            if minimize:
                self.hide()
            else:
                self.show()
                self.followParentRelative()

    def followParentRelative(self):
        if self.__follow__ and self.__parent__ is not None:
            # pPoint = self.__parent__.mapToGlobal(QPoint(self.__parent__.x(), self.__parent__.y()))
            pPoint = QPoint(0, 0)

            if self.HAnchor == Parapluie.HCenter:
                x = pPoint.x() + self.__parent__.width() / 2 - (self.width() / 2)
            elif self.HAnchor == Parapluie.Left:
                x = pPoint.x() + self.leftDistance
            elif self.HAnchor == Parapluie.Right:
                x = pPoint.x() + self.__parent__.width() + self.rightDistance - self.width()
            else:
                x = 0

            if self.VAnchor == Parapluie.VCenter:
                y = pPoint.y() + self.__parent__.height() / 2 - (self.height() / 2)
            elif self.VAnchor == Parapluie.Top:
                y = pPoint.y() + self.topDistance
            elif self.VAnchor == Parapluie.Bottom:
                y = pPoint.y() + self.__parent__.height() + self.bottomDistance - self.height()
            else:
                y = 0

            if x > self.__parent__.width():
                x = self.__parent__.width()
            elif x < 0:
                x = 0

            if y > self.__parent__.height():
                y = self.__parent__.height()
            elif y < 0:
                y = 0

            self.__update_distance__ = False
            self.move(x, y)
            self.__update_distance__ = True
