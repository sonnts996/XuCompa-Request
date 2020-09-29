from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy, QStackedWidget

import xu.compa.parapluie as Parapluie
import xu.src.python.Utilities as Util
import xu.src.python.Window as XWin
from xu.compa.parapluie.python import StickyWindow


class MainWindow(StickyWindow.ParapluieWindow):

    def __init__(self):
        super().__init__()

        Util.Style.applyStyle(self)
        Util.Style.applyWindowTitle(self)
        Util.Style.applyWindowIcon(self)

        self.stack = QStackedWidget()
        self.jsonView = None

        mainToolbar = QToolBar()
        mainToolbar.setMovable(False)
        mainToolbar.addAction(Parapluie.Resource.invertIcon(Parapluie.Icon_Link_Svg), "Request", self.test)
        mainToolbar.addAction(Parapluie.Resource.invertIcon(Parapluie.Icon_Document_Json_Svg), "JSON Viewer",
                              self.showJSONViewer)

        stretchWidget = QWidget()
        stretchWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainToolbar.addWidget(stretchWidget)
        mainToolbar.addAction(Parapluie.Resource.invertIcon(Parapluie.Icon_Information_Svg), "Information", self.test2)

        mainToolbar.addAction(Parapluie.Resource.invertIcon(Parapluie.Icon_Levels_Svg), "Settings")
        self.addToolBar(Qt.LeftToolBarArea, mainToolbar)

        self.setCentralWidget(self.stack)

    def showJSONViewer(self):
        if self.jsonView is None:
            self.jsonView = XWin.JSONViewer()
            self.stack.addWidget(self.jsonView)

        self.stack.setCurrentWidget(self.jsonView)

    count = 0

    def test(self):
        self.count = self.count + 1
        if self.count % 3 == 0:
            tpe = Parapluie.Alert_Warning
        elif self.count % 3 == 1:
            tpe = Parapluie.Alert_Information
        else:
            tpe = Parapluie.Alert_Error

        a1 = StickyWindow.Alert(self, tpe)
        a1.setWindowTitle(str(self.count))
        a1.setMessage("Hello, this is the", self.count, "mesage test.", sep=" ")
        if self.count != 3:
            a1.setAutoClose(5000)
        self.addAlert(a1)

    def test2(self):
        self.count = self.count + 1
        a1 = StickyWindow.MessageBox(self)
        a1.initInformation("Hello")
        a1.show()
