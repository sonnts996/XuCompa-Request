import copy
import xml.etree.ElementTree as Et

from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItemModel
from PyQt5.QtWidgets import QTreeView

import xu.src.python.Module.ParamEditor.JSONObject as Jso
from xu.compa.Parapluie import Parapluie, PItemDelegate
from xu.src.python.Module.ParamEditor import JSONView, XMLView, ParamType, TableView


class ParamEditor(QTreeView):
    syncRequest = pyqtSignal()
    error = pyqtSignal(str)

    def __init__(self, paramType: ParamType = ParamType.Param):
        super().__init__()

        self.paramType = paramType
        if self.paramType == ParamType.JSON or self.paramType == ParamType.Param:
            self.headerData = {'key': 'KEY', 'value': 'VALUE'}
        elif self.paramType == ParamType.XML:
            self.headerData = {'key': 'TAG', 'value': 'DATA'}
        else:
            self.headerData = []
        self.xmlData = Et.Element("root")

        self.model = QStandardItemModel()
        self.setAlternatingRowColors(True)

        self.setModel(self.model)

        self.jsonView = JSONView(self, self.model)
        self.tableView = TableView(self, self.model)
        self.xmlView = XMLView(self, self.model)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.openMenu)
        self.model.itemChanged.connect(self.dataChange)

        self.delegate = PItemDelegate()
        self.setItemDelegate(self.delegate)

        if self.header():
            header = super(ParamEditor, self).header()
            header.setObjectName(Parapluie.Object_Header)
            header.setFixedHeight(36)
            header.setSectionResizeMode(0, QtWidgets.QHeaderView.Interactive)
            header.setCascadingSectionResizes(False)
        self.loadParam2Table()

        self.editable = True

    def setEditable(self, editable):
        self.editable = editable
        self.refresh()

    def setParamType(self, paramType: ParamType):
        if self.paramType != paramType:
            self.paramType = paramType
            if self.paramType == ParamType.JSON or self.paramType == ParamType.Param:
                self.headerData = {'key': 'KEY', 'value': 'VALUE'}
            elif self.paramType == ParamType.XML:
                self.headerData = {'key': 'TAG', 'value': 'DATA'}
            else:
                self.headerData = []
            self.model.setRowCount(0)
            self.header()

    def setData(self, param):
        if self.paramType == ParamType.Param or self.paramType == ParamType.JSON:
            if param is not None or isinstance(param, dict) or isinstance(param, list):
                param = Jso.fromObject(param)
            else:
                param = Jso.JObject()
            self.jsonView.setData(param)
        elif self.paramType == ParamType.XML:
            if param is not None:
                if isinstance(param, Et.Element):
                    self.xmlView.setData(param)
                else:
                    # xml = Et.Element('root')
                    self.xmlView.setData(None)
            else:
                # xml = Et.Element('root')
                self.xmlView.setData(None)
        elif self.paramType == ParamType.Table:
            if param is not None or isinstance(param, list):
                param = Jso.fromObject(param)
            else:
                param = Jso.fromObject([])
            self.tableView.setData(self.headerData, param)

    def setHeaderData(self, header: list):
        self.headerData = header
        self.header()

    def getData(self):
        if self.paramType == ParamType.Param or self.paramType == ParamType.JSON:
            return Jso.toDict(self.jsonView.jsonData)
        elif self.paramType == ParamType.XML:
            return copy.copy(self.xmlView.xmlData)
        elif self.paramType == ParamType.Table:
            return Jso.toDict(self.tableView.jsonData)

    def header(self):
        if self.headerData is not None and self.headerData != [] and self.headerData != {}:
            if isinstance(self.headerData, list):
                self.model.setHorizontalHeaderLabels(map(lambda a: a['name'], self.headerData))
            elif isinstance(self.headerData, dict):
                self.model.setHorizontalHeaderLabels(self.headerData.values())
            return True
        else:
            return False

    def refresh(self):
        self.loadParam2Table()

    def pushSignal(self):
        self.syncRequest.emit()

    def loadParam2Table(self):
        self.model.setRowCount(0)
        if self.paramType == ParamType.Param or self.paramType == ParamType.JSON:
            self.jsonView.createUI()
        elif self.paramType == ParamType.XML:
            self.xmlView.createUI()
        elif self.paramType == ParamType.Table:
            self.tableView.createUI()
        self.expandAll()

    def openMenu(self, position):
        if self.paramType == ParamType.Param or self.paramType == ParamType.JSON:
            self.jsonView.openMenu(position)
        elif self.paramType == ParamType.XML:
            self.xmlView.openMenu(position)
        elif self.paramType == ParamType.Table:
            self.tableView.openMenu(position)

    def dataChange(self, item):
        if self.paramType == ParamType.Param or self.paramType == ParamType.JSON:
            self.jsonView.dataChange(item)
        elif self.paramType == ParamType.XML:
            self.xmlView.dataChange(item)
        elif self.paramType == ParamType.Table:
            self.tableView.dataChange(item)
