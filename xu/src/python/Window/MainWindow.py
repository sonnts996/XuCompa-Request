from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QToolBar, QWidget, QSizePolicy, QStackedWidget, QAction

import xu.src.python.Utilities as Util
from xu.compa.Parapluie import PResource, Parapluie, PWindow, PAlert
from xu.src.python.JsonViewer import JSONViewer
from xu.src.python.Request.RequestViewer import RequestViewer


class MainWindow(PWindow):

    def __init__(self):
        super().__init__()

        Util.Style.applyStyle(self)
        Util.Style.applyWindowTitle(self)
        Util.Style.applyWindowIcon(self)

        self.stack = QStackedWidget()
        self.stackList = {}
        self.jsonView = None
        self.requestView = None

        mainToolbar = QToolBar()
        mainToolbar.setMovable(False)
        topWidget = QWidget()
        topWidget.setFixedHeight(8)
        mainToolbar.addWidget(topWidget)
        self.requestAction = mainToolbar.addAction(PResource.invertIcon(Parapluie.Icon_Link_Svg),
                                                   "Request",
                                                   self.showRequest)
        self.requestAction.setCheckable(True)
        self.jsonAction = mainToolbar.addAction(PResource.invertIcon(Parapluie.Icon_Document_Json_Svg),
                                                "JSON Viewer",
                                                self.showJSONViewer)
        self.jsonAction.setCheckable(True)

        stretchWidget = QWidget()
        stretchWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        mainToolbar.addWidget(stretchWidget)
        mainToolbar.addAction(PResource.invertIcon(Parapluie.Icon_Information_Svg), "Information")

        mainToolbar.addAction(PResource.invertIcon(Parapluie.Icon_Levels_Svg), "Settings")
        self.addToolBar(Qt.LeftToolBarArea, mainToolbar)

        bottomWidget = QWidget()
        bottomWidget.setFixedHeight(8)
        mainToolbar.addWidget(bottomWidget)

        self.stack.currentChanged.connect(self.stackChange)

        self.setCentralWidget(self.stack)
        self.setContentsMargins(0, 0, 0, 0)

        self.showRequest()

    def stackChange(self, index: int):
        for i in self.stackList:
            w: QAction = self.stackList[i]
            w.setChecked(i == str(index))

    def showJSONViewer(self):
        if self.jsonView is None:
            self.jsonView = JSONViewer()
            self.jsonView.alert.connect(self.showAlert)
            self.stackList[str(self.stack.count())] = self.jsonAction
            self.stack.addWidget(self.jsonView)

        self.stack.setCurrentWidget(self.jsonView)

    def showRequest(self):
        if self.requestView is None:
            self.requestView = RequestViewer(self)
            self.requestView.alert.connect(self.showAlert)
            self.stackList[str(self.stack.count())] = self.requestAction
            self.stack.addWidget(self.requestView)

        self.stack.setCurrentWidget(self.requestView)

    def showAlert(self, text, type, button1=None, button2=None):
        alert = PAlert(self, type)
        alert.setMessage(text)
        if button1 is None and button2 is None:
            alert.setAutoClose(3000)
        self.addAlert(alert)


