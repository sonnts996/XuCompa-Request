from PyQt5.QtCore import pyqtSignal, QUrl
from PyQt5.QtWebEngineWidgets import QWebEngineView
from PyQt5.QtWidgets import QSplitter

from xu.compa.Parapluie import Parapluie, PTabWidget, PFunction
from xu.src.python.Module.ParamEditor import TextEditWidget, EditorType, ParamType, ParamEditor, ParamEditorConnect
from xu.src.python.Request.Model import APIResponse, APIData, BodyType


class RequestResult(PTabWidget):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self):
        super().__init__()
        self.setObjectName(Parapluie.Object_Raised)
        self.setMinimumHeight(500)
        self.setFixedHeight(500)

        self.header = ParamEditor(ParamType.Param)

        self.analysis = ParamEditor(ParamType.JSON)

        self.result = ParamEditor(ParamType.JSON)

        self.editor = TextEditWidget(save=True)
        self.editor.setTitle('Result')
        self.editor.title.setVisible(False)
        self.editor.alert.connect(lambda a, b, c, d: self.alert.emit(a, b, c, d))

        self.paramConnect = ParamEditorConnect(self.result, self.editor)
        self.editor.setEditorType(EditorType.Text)

        self.webView = QWebEngineView()

        splitter = QSplitter()
        splitter.addWidget(self.editor)
        splitter.addWidget(self.result)
        splitter.setObjectName(Parapluie.Object_QSplitter)

        self.addTab(splitter, "Data")
        self.addTab(self.webView, "Preview")
        self.addTab(self.header, "Header")
        self.addTab(self.analysis, "Analysis")

        self.response: APIResponse = APIResponse()
        self.data: APIData = APIData()
        self.currentChanged.connect(self.tabChanged)

    def pushAlert(self, text, tpe=Parapluie.Alert_Error):
        self.alert.emit(text, tpe, None, None)

    def setResponse(self, apiData):
        if apiData is not None:
            self.response = apiData.parseResponse()
            self.data = apiData
        else:
            self.response = APIResponse()
            self.data = APIData()
        self.editor.setTitle(self.data.parseConfig().api())
        self.refresh()

    def refresh(self):
        if self.response is None:
            self.response: APIResponse = APIResponse()
            self.clearData()
        else:
            try:
                if "Content-Type" in self.response.header():
                    contentType, charset = BodyType.getContentType(self.response.header()['Content-Type'])
                    if contentType.startswith("image"):
                        self.editor.setData({})
                        url = QUrl(self.response.parseAnalysis().url())
                        self.webView.load(url)
                        self.editor.setEditorType(EditorType.Text)
                        self.editor.blockEditorType(True)
                        self.editor.setText(str(self.response.content()))
                    else:
                        self.editor.blockEditorType(False)
                        if isinstance(self.response.content(), bytes):
                            if charset is not None:
                                content = str(self.response.content().decode(charset))
                            else:
                                content = str(self.response.content())
                        else:
                            content = self.response.content()

                        if self.currentIndex() == 0:  # data
                            if "json" in contentType:
                                self.editor.setEditorType(EditorType.JSON)
                                self.editor.setText(content)
                            elif "xml" in contentType:
                                self.editor.setEditorType(EditorType.XML)
                                self.editor.setText(content)
                            elif "html" in contentType:
                                self.editor.setEditorType(EditorType.HTML)
                                self.editor.setText(content)
                            elif "javascript" in contentType:
                                self.editor.setEditorType(EditorType.Javascript)
                                self.editor.setText(content)
                            else:
                                self.editor.setEditorType(EditorType.Text)
                                self.editor.setText(content)
                        elif self.currentIndex() == 1:  # preview
                            url = QUrl(self.response.parseAnalysis().url())
                            if "html" in contentType:
                                self.webView.setHtml(content, url)
                            else:
                                html = "<div>" + content + "</div>"
                                self.webView.setHtml(html, url)
                    if self.currentIndex() == 2:  # header
                        self.header.setData(self.response.header())
                        self.header.refresh()
                    elif self.currentIndex() == 3:  # analysis
                        data = self.__analysis()
                        self.analysis.setData(data)
                        self.analysis.refresh()
                else:
                    if self.response.header() != {}:
                        self.pushAlert("Content-Type error, see Header")
                        self.header.setData(self.response.header())
                        data = self.__analysis()
                        self.analysis.setData(data)
                        self.analysis.refresh()
            except Exception as ex:
                print(RequestResult, ex, 104)
                self.pushAlert(str(ex))

    def clearData(self):
        self.editor.setData({})
        self.header.setData({})
        self.analysis.setData({})
        self.webView.setHtml("<html></html>")

    def tabChanged(self, index):
        self.refresh()

    def __analysis(self):
        header = self.data.parseConfig().header()
        data = self.response.parseAnalysis()
        data.setSendHeader(header)
        return data.analysis
