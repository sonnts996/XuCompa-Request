import copy
import json
import logging
import os

from PyQt5.QtCore import Qt, pyqtSignal
from PyQt5.QtGui import QCursor
from PyQt5.QtWidgets import QToolButton, QHBoxLayout, QVBoxLayout, QWidget, QApplication, QScrollArea, QCompleter, \
    QStyledItemDelegate

import xu.src.python.Request.HTTP.HTTPRequest as Request
from xu.compa.Parapluie import PResource, Parapluie, PLabelEdit, PFunction, PWidget, PCorner
from xu.compa.xhash import XashHelp
from xu.src.python import Utilities
from xu.src.python.Model.XFile import XFile
from xu.src.python.Request import RequestParam, RequestResult
from xu.src.python.Request.Model import APIData, APIResponse


class RequestWorkspace(PWidget):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self, window):
        super().__init__()

        self.param = RequestParam()
        self.param.alert.connect(lambda a, b, c, d: self.alert.emit(a, b, c, d))

        self.result = RequestResult()
        self.result.alert.connect(lambda a, b, c, d: self.alert.emit(a, b, c, d))

        clearButton = QToolButton()
        clearButton.setText("Clear")
        clearButton.setToolTip("Clear (Ctrl+D)")
        clearButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Clear_All_Svg))
        clearButton.setFixedSize(36, 36)
        clearButton.pressed.connect(self.clearAll)

        saveButton = QToolButton()
        saveButton.setText("Save")
        saveButton.setToolTip("Save (Ctrl+S)")
        saveButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Save_Svg))
        saveButton.setFixedSize(36, 36)
        saveButton.pressed.connect(self.saveData)

        runButton = QToolButton()
        runButton.setText("Run")
        runButton.setToolTip("Run (Ctrl+R)")
        runButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Play_Button_Svg))
        runButton.setFixedSize(36, 36)
        runButton.pressed.connect(self.run)

        self.category = self.param.categories

        self.title = PLabelEdit()
        self.title.setFixedHeight(36)
        self.title.setMaximumHeight(36)
        self.title.setStyleSheet("QLabel{color:#424242; font-size:16px}")
        self.title.setText("Untitled")

        tool = QHBoxLayout()
        tool.addSpacing(10)
        tool.addWidget(self.title)
        tool.addStretch()
        tool.addWidget(clearButton)
        tool.addWidget(runButton)
        tool.addWidget(saveButton)

        widget = QWidget()
        widget.setLayout(tool)
        widget.layout().setContentsMargins(8, 4, 8, 4)
        widget.setObjectName(Parapluie.Object_TopHeader)
        widget.setMaximumHeight(44)
        PFunction.applyShadow(widget)

        workLayout = QVBoxLayout()
        workLayout.addWidget(self.param)
        workLayout.addSpacing(20)
        workLayout.addWidget(self.result)
        workLayout.setContentsMargins(8, 8, 8, 8)

        workspace = PWidget()
        workspace.setLayout(workLayout)
        workspace.setObjectName(Parapluie.Object_Raised)

        scroll = QScrollArea()
        scroll.setWidget(workspace)
        scroll.setWidgetResizable(True)
        scroll.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        layout = QVBoxLayout()
        layout.setSpacing(10)
        layout.setAlignment(Qt.AlignTop)
        layout.addWidget(widget)
        layout.addWidget(scroll)
        layout.setContentsMargins(0, 0, 0, 10)

        outer = PWidget()
        outer.setObjectName(Parapluie.Object_TopHeader)
        outer.setLayout(layout)

        outerLayout = QHBoxLayout()
        outerLayout.addWidget(outer)

        self.setLayout(outerLayout)
        self.layout().setContentsMargins(0, 5, 5, 10)

        self.currentFile: XFile = None
        self.win = window
        self.onSaveFunc = None

    def pushAlert(self, text, tpe=Parapluie.Alert_Error):
        self.alert.emit(text, tpe, None, None)

    def run(self):
        config = self.param.getData()
        if config is None:
            return

        if self.currentFile is None:
            self.currentFile = XFile("Unknown")
        if self.currentFile.unsavedData is None or not isinstance(self.currentFile.unsavedData, APIData):
            self.currentFile.unsavedData = APIData()

        self.currentFile.unsavedData.setConfig(config)

        QApplication.setOverrideCursor(QCursor(Qt.WaitCursor))
        res = Request.call(config)
        if res is None:
            self.pushAlert("API call failed")
            self.currentFile.unsavedData.setResponse(APIResponse())
            self.result.setResponse(self.currentFile.unsavedData)
        else:
            if res.status() < 400:
                self.pushAlert(Request.print_response(res.status()), Parapluie.Alert_Success)
            else:
                self.pushAlert(Request.print_response(res.status()), Parapluie.Alert_Error)

            self.currentFile.unsavedData.setResponse(copy.copy(res))
            self.result.setResponse(self.currentFile.unsavedData)
        QApplication.restoreOverrideCursor()

    def setCurrentFile(self, file: XFile):
        if self.currentFile is None:
            self.currentFile = file
        elif self.currentFile != file:
            if isinstance(self.currentFile.unsavedData, APIData):
                data = self.currentFile.unsavedData
            else:
                data = APIData()
            param = copy.deepcopy(self.param.getData(True))
            if param is not None:
                data.setConfig(param)
            self.currentFile.unsavedData = data

            self.currentFile = file

        data2 = APIData()
        if self.currentFile.unsavedData is None \
                or self.currentFile.unsavedData == "" \
                or self.currentFile.unsavedData == {}:
            try:
                if os.path.isfile(file.getPath()):
                    f = open(file.getPath(), "r", encoding="utf-8").read()
                    js = json.loads(f)
                    data2.construct(js)
            except Exception as ex:
                logging.exception(ex)
                self.alert.emit("Can not open file:\n" + str(ex), Parapluie.Alert_Error, None, None)
        else:
            data2.construct(self.currentFile.unsavedData.data)

        self.param.setConfig(data2.parseConfig())
        self.result.clearData()
        self.result.setResponse(data2)

        xash = XashHelp.path2Xash(self.currentFile.getPath())
        self.title.setText(xash.getName())
        if xash.getCategory() != "":
            self.category.setText(xash.getCategory())
        else:
            self.category.setText("")

    def clearAll(self):
        self.result.setResponse(None)
        self.param.setConfig()

    def setCategories(self, categories):
        completer = QCompleter(categories)
        mCompleterItemDelegate = QStyledItemDelegate(self)
        completer.popup().setItemDelegate(mCompleterItemDelegate)
        Utilities.Style.applyStyle(completer.popup())
        self.category.setCompleter(completer)

    def saveData(self):
        if self.currentFile is not None:
            data = APIData()
            param = copy.deepcopy(self.param.getData(True))
            if param is not None:
                data.setConfig(param)
            self.currentFile.unsavedData = data

            name = self.title.text()
            category = self.category.text()
            description = self.currentFile.unsavedData.parseConfig().description()
            description = " ".join(description.split())

            if self.onSaveFunc is not None:
                self.onSaveFunc(self.currentFile, (name, category, description))
