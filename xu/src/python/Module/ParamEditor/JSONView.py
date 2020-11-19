import copy
import logging

from PyQt5.QtCore import QPoint
from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMenu, QAction

import xu.src.python.Module.ParamEditor as ParamEditor
import xu.src.python.Module.ParamEditor.JSONObject as  Jso
from xu.src.python import Utilities


class JSONView:
    def __init__(self, treeView, model):
        self.treeView: ParamEditor.ParamEditor = treeView
        self.model = model
        self.jsonData = Jso.JObject()
        self.flow = ParamEditor.ActionFlow()

    def setData(self, param):
        self.jsonData: Jso.JObject = param
        self.flow.add(copy.deepcopy(self.jsonData))

    def createUI(self):
        for elem in self.jsonData:
            self.createJsonUi(elem, self.model.invisibleRootItem(), self.jsonData)

    def createJsonUi(self, obj, parent: QStandardItem, itemParent):
        if isinstance(obj, Jso.JKey):
            item = QStandardItem(obj.key)
            item.setEditable(obj.key != 'JSON' and self.treeView.editable)
            item.setData(self.getItemData(obj, "key", itemParent))
            if obj.isObject():
                self.createJsonUi(obj.value, item, obj)
                if isinstance(obj.value, Jso.JList):
                    value = QStandardItem(str(obj.value.count()))
                    value.setEditable(False)
                    parent.appendRow([item, value])
                else:
                    parent.appendRow(item)
            else:
                value = QStandardItem(obj.getValueStr())
                value.setEditable(not (obj.isObject() and obj.isEmpty()) and self.treeView.editable)
                value.setData(self.getItemData(obj, "value", itemParent))
                parent.appendRow([item, value])
        elif isinstance(obj, Jso.JList):
            for i in range(obj.count()):
                item = QStandardItem(str(i) + ":")
                item.setEditable(False)
                data: Jso.JIndex = obj[i]
                item.setData(self.getItemData(data, "index", obj))
                if data.isObject():
                    self.createJsonUi(data.value, item, data)
                    parent.appendRow(item)
                else:
                    value = QStandardItem(data.getValueStr())
                    value.setEditable(not (data.isObject() and data.isEmpty()) and self.treeView.editable)
                    value.setData(self.getItemData(data, "value", obj))
                    parent.appendRow([item, value])
        elif isinstance(obj, Jso.JObject):
            for data in obj:
                self.createJsonUi(data, parent, obj)

    def dataChange(self, item: QStandardItem):
        data = item.data()
        if data is None:
            item.setText("")
        else:
            jObj = data['item']
            tpe = data['type']
            parent: Jso.JObject = data['parent']
            if tpe == 'value':
                if isinstance(jObj, Jso.JKey) or isinstance(jObj, Jso.JIndex):
                    jObj.value = self.keyDecode(item.text())
            elif tpe == 'key':
                if isinstance(jObj, Jso.JKey):
                    if parent is not None and item.text() not in parent:
                        jObj.key = item.text()
                    else:
                        self.treeView.error.emit("Duplicate Key error!")
                        item.setText(jObj.key)
                else:
                    self.treeView.error.emit("Cell is not a key!")
            self.treeView.pushSignal()
            self.flow.add(copy.deepcopy(self.jsonData))

    def getItemData(self, item, tpe, key=None):
        return {"item": item, 'type': tpe, 'parent': key}

    def keyDecode(self, text: str):
        if text == '@null':
            return None
        elif text == '@{}':
            return Jso.JObject()
        elif text == '@[]':
            return Jso.JList()
        elif text.isnumeric():
            return int(text)
        elif text.startswith("'"):
            return text[1:]
        else:
            return text

    def openMenu(self, position: QPoint):
        indexes = self.treeView.selectedIndexes()

        isItem = len(indexes) > 0
        data = None
        item = None
        if isItem:
            index = indexes[0]
            x = position.x()
            for i in indexes:
                point = self.treeView.visualRect(i)
                iw = point.width()
                ix = point.x()

                if ix < x < (ix + iw):
                    index = i
                    break
            item = self.model.itemFromIndex(index)
            data = item.data()

        if data is None:
            tpe = None
            par = self.jsonData
            ite = None
        else:
            tpe = data['type']
            par = data['parent']
            ite = data['item']

        if tpe == 'index':
            if ite.isObject():
                self.createMenu(position, 0, par, ite, item)
            else:
                self.createMenu(position, 1, par, ite, item)
        else:
            if isinstance(ite, Jso.JKey) or isinstance(ite, Jso.JIndex):
                if ite.isObject():
                    self.createMenu(position, 2, par, ite, item)
                else:
                    self.createMenu(position, 1, par, ite, item)
            else:
                self.createMenu(position, 3, par, ite, item)

    def createMenu(self, position, tpe, par, obj, item):
        # global
        undoAction = QAction('Undo', self.treeView)
        undoAction.setEnabled(not self.flow.isEnd())
        redoAction = QAction('Redo', self.treeView)
        redoAction.setEnabled(not self.flow.isFirst())
        copyAsJSON = QAction('Copy as JSON', self.treeView)

        pasteAsJSON = QAction('Paste as JSON', self.treeView)
        clearAll = QAction('Clear table', self.treeView)

        # delete
        copyTextAction = QAction('Copy text', self.treeView)
        pasteTextAction = QAction("Paste text", self.treeView)

        deleteKeyAction = QAction('Delete key', self.treeView)

        # duplicate
        duplicateAction = QAction('Duplicate', self.treeView)

        # add
        addKeyMenu = QMenu("Add..")
        Utilities.Style.applyStyle(addKeyMenu)

        # add value
        addValueAction = QAction('Add Value', self.treeView)

        # add object
        addObjectAction = QAction('Add Object', self.treeView)

        # add list
        addListAction = QAction('Add List', self.treeView)

        addKeyMenu.addAction(addValueAction)
        if self.treeView.paramType != ParamEditor.ParamType.Param:
            addKeyMenu.addAction(addObjectAction)
            addKeyMenu.addAction(addListAction)

        # insert
        insertKeyMenu = QMenu("Insert..")
        Utilities.Style.applyStyle(insertKeyMenu)

        # insert value
        insertValueAction = QAction('Insert Value', self.treeView)

        # insert object
        insertObjectAction = QAction('Insert Object', self.treeView)

        # insert list
        insertListAction = QAction('Insert List', self.treeView)

        insertKeyMenu.addAction(insertValueAction)
        insertKeyMenu.addAction(insertObjectAction)
        insertKeyMenu.addAction(insertListAction)

        menu = QMenu()
        Utilities.Style.applyStyle(menu)
        menu.addAction(copyAsJSON)
        if self.treeView.editable:
            menu.addAction(undoAction)
            menu.addAction(redoAction)
            menu.addAction(pasteAsJSON)
            menu.addAction(clearAll)
            menu.addSeparator()

        if self.treeView.editable:
            if tpe == 0:  # index
                menu.addAction(copyTextAction)
                menu.addAction(pasteTextAction)
                menu.addAction(duplicateAction)
                if self.treeView.paramType != ParamEditor.ParamType.Param:
                    menu.addMenu(insertKeyMenu)
                menu.addMenu(addKeyMenu)
                menu.addAction(deleteKeyAction)
            elif tpe == 1:  # key
                menu.addAction(copyTextAction)
                menu.addAction(pasteTextAction)
                if obj.isEmpty() and self.treeView.paramType != ParamEditor.ParamType.Param:
                    menu.addMenu(insertKeyMenu)
                menu.addMenu(addKeyMenu)
                menu.addAction(deleteKeyAction)
            elif tpe == 2:  # obj
                menu.addAction(copyTextAction)
                menu.addAction(pasteTextAction)
                if self.treeView.paramType != ParamEditor.ParamType.Param:
                    menu.addMenu(insertKeyMenu)
                menu.addMenu(addKeyMenu)
                menu.addAction(deleteKeyAction)
            else:  # table
                menu.addMenu(addKeyMenu)
        else:
            if tpe == 0 or tpe == 1 or tpe == 2:
                menu.addAction(copyTextAction)
        action = menu.exec_(self.treeView.viewport().mapToGlobal(position))

        if action == undoAction:
            self.flowAction(1)
        elif action == redoAction:
            self.flowAction(0)
        elif action == copyAsJSON:
            self.actionCopyAsJSON()
        elif action == pasteAsJSON:
            self.actionPasteAsJSON()
        elif action == clearAll:
            self.actionClearAll()
        elif action == copyTextAction:
            self.actionCopyText(item)
        elif action == pasteTextAction:
            self.actionPasteText(item)
        elif action == deleteKeyAction:
            self.actionDelete(par, obj)
        elif action == duplicateAction:
            self.actionDuplicate(par, obj)
        elif action == addValueAction:
            self.actionAddValue(par, obj)
        elif action == addObjectAction:
            self.actionAddObject(par, obj)
        elif action == addListAction:
            self.actionAddList(par, obj)
        elif action == insertValueAction:
            if obj.isEmpty():
                obj.value = Jso.JObject()
            self.actionAddValue(obj.value, None)
        elif action == insertObjectAction:
            if obj.isEmpty():
                obj.value = Jso.JObject()
            self.actionAddObject(obj.value, None)
        elif action == insertListAction:
            if obj.isEmpty():
                obj.value = Jso.JList()
            self.actionAddList(obj.value, None)

    # Menu action
    def flowAction(self, flow):
        if flow == 1:
            self.jsonData = self.flow.previous()
            self.treeView.refresh()
            self.treeView.pushSignal()
        else:
            self.jsonData = self.flow.next()
            self.treeView.refresh()
            self.treeView.pushSignal()

    def actionCopyText(self, item: QStandardItem):
        if item is not None:
            text = item.text()
            import clipboard
            clipboard.copy(text)

    def actionPasteText(self, item: QStandardItem):
        import clipboard
        text = clipboard.paste()
        if item is not None:
            if item.isEditable():
                item.setText(text)

    def actionCopyAsJSON(self):
        text = Jso.toString(self.jsonData)
        import clipboard
        clipboard.copy(text)

    def actionPasteAsJSON(self):
        import clipboard
        text = clipboard.paste()
        try:
            obj = Jso.fromString(text)
            self.jsonData = obj
            self.treeView.pushSignal()
            self.treeView.refresh()
            self.flow.add(copy.deepcopy(self.jsonData))
        except Exception as ex:
            logging.exception(ex)
            self.treeView.error.emit(str(ex))

    def actionClearAll(self):
        self.jsonData = Jso.JObject()
        self.treeView.refresh()
        self.treeView.pushSignal()
        self.flow.add(copy.deepcopy(self.jsonData))

    def actionDuplicate(self, par, obj):
        if obj is not None:
            inx = par.index(obj) + 1
            new = Jso.JIndex(inx, Jso.copyObject(obj.value))
            par.append(new, inx)
            self.treeView.refresh()
            self.flow.add(copy.deepcopy(self.jsonData))

    def actionDelete(self, par, obj):
        if isinstance(par, Jso.JObject) or isinstance(par, Jso.JList):
            par.remove(obj)
        self.treeView.refresh()
        self.treeView.pushSignal()
        self.flow.add(copy.deepcopy(self.jsonData))

    def actionAddValue(self, par, obj):
        if isinstance(par, Jso.JObject):
            new = Jso.JKey("<new key>", "")
            if obj is not None:
                inx = par.index(obj) + 1
            else:
                inx = -1
            par.addKey(new, inx)
        elif isinstance(par, Jso.JList):
            if obj is not None:
                inx = par.index(obj) + 1
                new = Jso.JIndex(inx, "")
            else:
                inx = -1
                new = Jso.JIndex(par.count(), "")
            par.append(new, inx)
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.jsonData))

    def actionAddObject(self, par, obj):
        if isinstance(par, Jso.JObject):
            child = Jso.JObject()
            new_item = Jso.JKey("<new key>", "")
            child.addKey(new_item)
            new = Jso.JKey("<new key>", child)
            if obj is not None:
                inx = par.index(obj) + 1
            else:
                inx = -1
            par.addKey(new, inx)
        elif isinstance(par, Jso.JList):
            child = Jso.JObject()
            new_item = Jso.JKey("<new key>", "")
            child.addKey(new_item)
            if obj is not None:
                inx = par.index(obj) + 1
                new = Jso.JIndex(inx, child)
            else:
                inx = -1
                new = Jso.JIndex(par.count(), child)
            par.append(new, inx)
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.jsonData))

    def actionAddList(self, par, obj):
        if isinstance(par, Jso.JObject):
            child = Jso.JList()
            new_item = Jso.JIndex(0, "")
            child.append(new_item)
            new = Jso.JKey("<new key>", child)
            if obj is not None:
                inx = par.index(obj) + 1
            else:
                inx = -1
            par.addKey(new, inx)
        elif isinstance(par, Jso.JList):
            child = Jso.JList()
            new_item = Jso.JIndex(0, "")
            child.append(new_item)
            if obj is not None:
                inx = par.index(obj) + 1
                new = Jso.JIndex(inx, child)
            else:
                inx = -1
                new = Jso.JIndex(par.count(), child)
            par.append(new, inx)
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.jsonData))
