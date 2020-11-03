from PyQt5.QtCore import pyqtSignal, Qt, QSize, QRect, QPoint
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QHBoxLayout, QFormLayout, QTextEdit, QSizePolicy, QToolButton, \
    QApplication

from xu.compa.Parapluie import PWidget, Parapluie, PTabWidget, PComboBox, PResource
from xu.src.python.Module.ParamEditor import ParamEditor, ParamType
from xu.src.python.Request import RequestBody, RequestLink
from xu.src.python.Request.Model import APIConfig, APILink
from xu.src.python.Utilities import listView, formLabel


class RequestParam(PWidget):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self):
        super().__init__()

        # line 1
        self.apiType = PComboBox()
        self.apiType.setFixedWidth(100)
        self.apiType.setView(listView())
        self.apiType.addItem("GET")
        self.apiType.addItem("POST")
        self.apiType.addItem("PUT")
        self.apiType.addItem("HEAD")
        self.apiType.addItem("DELETE")
        self.apiType.addItem("PATCH")
        self.apiType.addItem("OPTIONS")

        self.apiURL = QLineEdit()
        self.apiURL.setPlaceholderText("API..")

        l1 = QHBoxLayout()
        l1.setSpacing(10)
        l1.addWidget(self.apiType)
        l1.addWidget(self.apiURL)

        # line 2
        addLink = QToolButton()
        addLink.setIcon(PResource.defaultIcon(Parapluie.Icon_Plus_Svg))
        addLink.setIconSize(QSize(12, 12))
        addLink.setFixedSize(32, 32)
        addLink.pressed.connect(self.openApiLinkEdit)

        self.apiLink = PComboBox()
        self.apiLink.setView(listView())

        apiBar = QHBoxLayout()
        apiBar.setSpacing(6)
        apiBar.setContentsMargins(0, 0, 0, 0)
        apiBar.addWidget(self.apiLink, stretch=1)
        apiBar.addWidget(addLink)

        self.description = QTextEdit()
        self.description.setMinimumHeight(100)
        self.description.setMaximumHeight(100)

        l2 = QFormLayout()
        l2.setVerticalSpacing(6)
        l2.setHorizontalSpacing(10)

        l2.addRow(formLabel("API Link:"), apiBar)
        l2.addRow(formLabel("Description:", False), self.description)

        # line 3
        self.bodyWidget = RequestBody()
        self.bodyWidget.editor.alert.connect(lambda a, b, c, d: self.alert.emit(a, b, c, d))

        self.paramWidget = ParamEditor(ParamType.Param)

        self.headerWidget = ParamEditor(ParamType.Param)

        self.tab = PTabWidget()
        self.tab.resizable(True)
        self.tab.setSizeBox(300, 1000, 200)
        self.tab.sizeBox.setValue(400)
        self.tab.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.tab.addTab(self.headerWidget, "Header")
        self.tab.addTab(self.paramWidget, "Param")
        self.tab.addTab(self.bodyWidget, "Body")

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addLayout(l1)
        layout.addLayout(l2)
        layout.addWidget(self.tab)
        self.setLayout(layout)

        self.setObjectName(Parapluie.Object_Raised)

        self.dialog = RequestLink(self, QRect(QPoint(0, 0), QApplication.primaryScreen().size()))
        self.dialog.getData()
        self.updateAPILink()

    def openApiLinkEdit(self):
        self.dialog.loadData()
        rs = self.dialog.exec_()
        if rs == 1:
            self.updateAPILink()

    def pushAlert(self, text, tpe=Parapluie.Alert_Error):
        self.alert.emit(text, tpe, None, None)

    def getData(self, save=False) -> APIConfig:
        config = APIConfig()
        api = self.getURL()
        link = self.getLink()
        protocol = self.getProtocol()
        param = self.paramWidget.getData()
        header = self.headerWidget.getData()
        body, tpe = self.bodyWidget.getData()

        description = self.description.toPlainText()

        config.setAPI(api)
        config.setLink(link)
        config.setProtocol(protocol)
        config.setBody(body, tpe)
        config.setParam(param)
        config.setHeader(header)
        config.setDescription(description)

        if not save:
            if api == "" or api.isspace():
                self.pushAlert("API URL can not empty!", Parapluie.Alert_Error)
            else:
                if protocol is None:
                    self.pushAlert("Protocol error!")
                else:
                    return config
        else:
            return config

    # get
    def getProtocol(self) -> str:
        return self.apiType.currentText().title().upper()

    def getURL(self) -> str:
        return self.apiURL.text()

    def getLink(self) -> APILink:
        linkInx = self.apiLink.currentIndex()
        if len(self.dialog.listLink) + 1 > linkInx > 0:
            data = self.dialog.listLink[linkInx - 1]
            link = APILink()
            link.construct(data)
            return link
        else:
            defaultLink = APILink()
            defaultLink.setURL("")
            defaultLink.setName("..")
            return defaultLink

    # set
    def setConfig(self, config: APIConfig = None):
        if config is None:
            config = APIConfig()
            self.setURL(config.api())
            self.setAPILink(config.parseLink().url())
            self.apiType.setCurrentIndex(0)
        else:
            self.setURL(config.api())
            self.setAPIType(config.protocol())
            self.setAPILink(config.parseLink().url())
        self.setDescription(config.description())
        self.setBody(config.body(), config.bodyType())
        self.setParam(config.param())
        if config.param() is None or config.param() == {} or config.param() == []:
            if config.body() is not None and config.body() != {} and config.body() != [] and config.body() != "":
                self.tab.setCurrentIndex(2)
        else:
            self.tab.setCurrentIndex(1)

    def setURL(self, url):
        self.apiURL.setText(url)

    def setAPIType(self, tpe):
        if tpe == "GET":
            self.apiType.setCurrentIndex(0)
        elif tpe == "POST":
            self.apiType.setCurrentIndex(1)
        elif tpe == "PUT":
            self.apiType.setCurrentIndex(2)
        elif tpe == "HEAD":
            self.apiType.setCurrentIndex(3)
        elif tpe == "DELETE":
            self.apiType.setCurrentIndex(4)
        elif tpe == "PATCH":
            self.apiType.setCurrentIndex(5)
        elif tpe == "OPTIONS":
            self.apiType.setCurrentIndex(6)
        else:
            self.apiType.setCurrentIndex(0)

    def updateAPILink(self):
        self.apiLink.clear()
        self.apiLink.addItem("..")
        for item in self.dialog.listLink:
            i = APILink()
            i.construct(item)
            self.apiLink.addItem(i.name() + " (" + i.url() + ").")

    def setAPILink(self, link: str) -> bool:
        for i in range(len(self.dialog.listLink)):
            item = APILink()
            item.construct(self.dialog.listLink[i])
            if item.url() == link:
                self.apiLink.setCurrentIndex(i + 1)
                return True
        self.apiLink.setCurrentIndex(0)
        return False

    def setDescription(self, des):
        self.description.setText(des)

    def setParam(self, para):
        self.paramWidget.setData(para)
        self.paramWidget.refresh()

    def setBody(self, js, tpe):
        self.bodyWidget.setData(str(js), tpe)
