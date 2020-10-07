from PyQt5 import QtGui
from PyQt5.QtCore import pyqtSignal, QEvent
from PyQt5.QtWidgets import QMainWindow

from xu.compa.Parapluie.src import Parapluie
from xu.compa.Parapluie.src.StickyWindow.PAlert import PAlert


class PWindow(QMainWindow):
    resized = pyqtSignal()
    closed = pyqtSignal()
    minimized = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.__listAlerts__ = []
        self.__numberAlert__ = 3

    def moveEvent(self, a0: QtGui.QMoveEvent):
        super(QMainWindow, self).moveEvent(a0)
        self.resized.emit()

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        super(QMainWindow, self).resizeEvent(a0)
        self.resized.emit()

    def closeEvent(self, a0: QtGui.QCloseEvent):
        self.closed.emit()
        super(PWindow, self).closeEvent(a0)

    def changeEvent(self, event):
        if event.type() == QEvent.ActivationChange or event.type() == QEvent.WindowStateChange:
            self.minimized.emit()

    # Parapluie Window will be manage alert list
    def addAlert(self, new: PAlert):
        new.closed.connect(lambda: self.onAlertClose(new))
        new.adjustSize()
        if new not in self.__listAlerts__:
            self.__listAlerts__.append(new)

        self.refreshAlert()

    def refreshAlert(self):
        destroyed = []
        showing = []
        # tach du lieu -> destroyed -> showing -> hidden
        for i1 in reversed(self.__listAlerts__):
            if i1.__parent__ is None:
                destroyed.append(i1)
            else:
                if len(showing) <= self.__numberAlert__:
                    showing.append(i1)
                else:
                    i1.setInHideMode(True)
                    i1.hide()

        # xu ly showing
        x = -10
        y = 10
        for i2 in range(len(showing)):
            a2: PAlert = showing[i2]
            if i2 == 0:
                a2.enableFollowParentRelative()
                a2.setAnchor(Parapluie.Right, Parapluie.Top, x, y)
            else:
                prev: PAlert = showing[i2 - 1]
                y = y + prev.height() + 10
                a2.enableFollowParentRelative()
                a2.setAnchor(Parapluie.Right, Parapluie.Top, x, y)
            a2.setInHideMode(False)
            a2.show()

        # xu ly destroy
        for a3 in destroyed:
            a3.hide()
            a3.setInHideMode(True)
            self.__listAlerts__.remove(a3)

    def onAlertClose(self, a: PAlert):
        # inner destroy
        if a in self.__listAlerts__:
            self.refreshAlert()

    def clearAllAlert(self):
        # outer destroy - clear all
        for a in self.__listAlerts__:
            a.completeDestroy()
            self.refreshAlert()
