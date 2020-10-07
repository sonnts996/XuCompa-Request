from PyQt5 import QtWidgets
from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtGui import QStandardItemModel, QStandardItem
from PyQt5.QtWidgets import QTreeView, QMenu, QAction

import xu.src.python.Utilities as Util
from xu.compa.Parapluie import Parapluie


class ParamEditor(QTreeView):
    jsonData = {}
    syncRequest = pyqtSignal(object)

    def __init__(self):
        super().__init__()
        self.setObjectName(Parapluie.Object_Raised)

        self.model = QStandardItemModel()
        self.setAlternatingRowColors(True)

        self.setModel(self.model)

        self.setContextMenuPolicy(Qt.CustomContextMenu)
        self.customContextMenuRequested.connect(self.open_menu)
        self.model.itemChanged.connect(self.dataChange)

        self.loadParam2Table({})

    def setData(self, param):
        self.jsonData = param
        self.loadParam2Table(self.jsonData)

    def header(self):
        self.model.setHorizontalHeaderLabels(['KEY', 'VALUE'])
        header = super(ParamEditor, self).header()
        header.setObjectName(Parapluie.Object_Header)
        header.setFixedHeight(36)
        header.setSectionResizeMode(0, QtWidgets.QHeaderView.ResizeToContents)

    def update(self):
        self.loadParam2Table(self.jsonData)

    def loadParam2Table(self, param):
        self.model.clear()
        self.header()
        self.createUI(self.model.invisibleRootItem(), param, 0, "", [])
        self.expandAll()

    def pushSignal(self, data=None):
        if data is None:
            self.syncRequest.emit(self.jsonData)
        else:
            self.syncRequest.emit(data)

    # INNER FUNCTION

    # create ui
    def createUI(self, parent, obj, level, parent_name="", item_link=None):
        if item_link is None:
            item_link = []
        if isinstance(obj, list):
            for i in range(len(obj)):
                if isinstance(obj[i], dict) or isinstance(obj[i], list):
                    item = QStandardItem(str(i) + ": ")
                    item.setEditable(False)
                    item.setData(self.itemData(":" + str(i), parent_name, level, item_link, True))
                    parent.appendRow([item])
                    link = item_link.copy()
                    link.append(":" + str(i))
                    self.createUI(item, obj[i], level, parent_name, link)
                else:
                    item = QStandardItem(str(i) + ": ")
                    item.setEditable(False)
                    value = QStandardItem(str(obj[i]))
                    value.setEditable(True)
                    link = item_link.copy()
                    link.append(":" + str(i))
                    item.setData(self.itemData(":" + str(i), parent_name, level, link, True))
                    value.setData(self.itemData(":" + str(i), parent_name, level, link, False))
                    parent.appendRow([item, value])
        elif isinstance(obj, dict):
            for key, value in obj.items():
                if isinstance(value, dict) or isinstance(value, list):
                    item = QStandardItem(key)
                    item.setEditable(True)
                    item.setData(self.itemData(key, parent_name, level, item_link, True))
                    parent.appendRow([item])
                    link = item_link.copy()
                    link.append(key)
                    self.createUI(item, value, level + 1, key, link)
                else:
                    self.addObject(parent, obj[key], level, key, item_link)
        else:
            self.addObject(parent, obj, level, parent_name, item_link)

    def addObject(self, parent, obj, level, parent_name="", item_link=None):
        if item_link is None:
            item_link = []
        item = QStandardItem(parent_name)
        item.setEditable(True)
        value = QStandardItem(str(obj))
        value.setEditable(True)
        item.setData(self.itemData(parent_name, "", level, item_link, True))
        value.setData(self.itemData(parent_name, "", level, item_link, False))
        parent.appendRow([item, value])

    def itemData(self, key, parent, level, link, isKey):
        return {"key": key, "parent": parent, 'level': level, 'link': link, "isKey": isKey}

    # data manage function
    def dataChange(self, item: QStandardItem):
        data = item.data()
        if data is not None and "link" in data:
            if not data["isKey"]:
                item_link = data['link']
                link = item_link.copy()
                link.append(data['key'])
                self.update_data(self.jsonData, link, item.text(), 0, len(link))
                self.pushSignal()
            else:
                item_link = data['link']
                link = item_link.copy()
                link.append(data['key'])
                if item.text() != "":
                    self.update_key(self.jsonData, link, item.text(), 0, len(link))
                    self.pushSignal()
                else:
                    self.remove_data(self.jsonData, link, 0, len(link))
                    self.update()
                    self.pushSignal()

    def update_data(self, obj, link, new, index, end):
        i = link[index]
        if i.startswith(":"):
            i = int(i.replace(":", ""))
        if index == end - 1:
            obj[i] = new
        else:
            self.update_data(obj[i], link, new, index + 1, end)

    def update_key(self, obj, link, new, index, end):
        i = link[index]
        if i.startswith(":"):
            i = int(i.replace(":", ""))
        if index == end - 1:
            obj[new] = obj[i]
            del obj[i]
        else:
            self.update_key(obj[i], link, new, index + 1, end)

    def open_menu(self, position):
        indexes = self.selectedIndexes()
        level = 0
        data_link = []
        link = []
        item = None
        if len(indexes) > 0:
            index = indexes[0]
            item = self.model.itemFromIndex(index)
            data = item.data()
            if data is not None:
                link = data['link']
                data_link = link.copy()
                data_link.append(data['key'])
                level = 1

        menu = QMenu()
        Util.Style.applyStyle(menu)

        delete_action = QAction('&Delete key', self)
        new_action = QAction('&Add key', self)

        menu.addAction(new_action)
        if level == 1:
            menu.addAction(delete_action)

        action = menu.exec_(self.viewport().mapToGlobal(position))

        if action == delete_action:
            if data_link is not None and data_link != []:
                self.remove_data(self.jsonData, data_link, 0, len(data_link))
                self.update()
        elif action == new_action:
            if self.is_list(self.jsonData, link, 0, len(link)):
                data_new = self.get_data(self.jsonData, data_link, 0, len(data_link))
                self.duplicate_data(self.jsonData, link, data_new.copy(), 0, len(link))
                self.update()
                self.pushSignal()
            elif self.is_list(self.jsonData, data_link, 0, len(data_link)):
                data_new = self.get_data(self.jsonData, data_link, 0, len(data_link))
                self.add_data(self.jsonData, data_link, data_new.copy(), 0, len(data_link))
                self.update()
                self.pushSignal()
            else:
                if data_link:
                    self.add_data(self.jsonData, data_link, "<key>", 0, len(data_link))
                else:
                    self.jsonData["<key>"] = ""
                self.update()
                self.pushSignal()

    def remove_data(self, obj, link, index, end):
        if index <= end - 1:
            i = link[index]
            if i.startswith(":"):
                i = int(i.replace(":", ""))
            if index == end - 1:
                del obj[i]
            else:
                self.remove_data(obj[i], link, index + 1, end)

    def is_list(self, obj, link, index, end):
        if index <= end - 1:
            i = link[index]
            if i.startswith(":"):
                i = int(i.replace(":", ""))
            if index == end - 1:
                return isinstance(obj[i], list)
            else:
                return self.is_list(obj[i], link, index + 1, end)
        else:
            return False

    def get_data(self, obj, link, index, end):
        if index <= end - 1:
            i = link[index]
            if i.startswith(":"):
                i = int(i.replace(":", ""))
            if index == end - 1:
                return obj[i]
            else:
                return self.get_data(obj[i], link, index + 1, end)
        else:
            return ""

    def add_data(self, obj, link, new, index, end):
        if index <= end - 1:
            i = link[index]
            if i.startswith(":"):
                i = int(i.replace(":", ""))
            if index == end - 1:
                if isinstance(obj[i], list):
                    if len(obj[i]) > 1:
                        obj[i].append(obj[i][0])
                    else:
                        obj[new] = ""
                elif isinstance(obj[i], dict) or str(obj[i]) == "":
                    obj[i] = {}
                    obj[i][new] = ""
                else:
                    obj[new] = ""
            else:
                self.add_data(obj[i], link, new, index + 1, end)

    def duplicate_data(self, obj, link, new, index, end):
        if index <= end - 1:
            i = link[index]
            if i.startswith(":"):
                i = int(i.replace(":", ""))
            if index == end - 1:
                if isinstance(obj[i], list):
                    obj[i].append(new)
            else:
                self.duplicate_data(obj[i], link, new, index + 1, end)
