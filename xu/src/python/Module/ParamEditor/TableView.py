import copy

from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QMenu, QAction

import xu.src.python.Module.ParamEditor as ParamEditor
import xu.src.python.Module.ParamEditor.JSONObject as Jso
from xu.src.python import Utilities

"""
[
    {
        'key': 'id',
        'name': 'Id',
        'editable': False,
    },
    {
        'key': 'name',
        'name': 'Name',
        'editable': True,
    },
    {
        'key': 'url',
        'name': 'Link',
        'editable': True,
    }
]
"""


class TableView:
    def __init__(self, treeView, model):
        self.treeView: ParamEditor.ParamEditor = treeView
        self.model = model
        self.jsonData = Jso.fromObject([])
        self.headerData = []
        self.flow = ParamEditor.ActionFlow()

    def setData(self, header, param):
        self.headerData = header
        self.jsonData: Jso.JObject = param
        self.flow.add(copy.deepcopy(self.jsonData))

    def createUI(self):
        for i in self.jsonData.get('JSON'):
            self.createJsonUi(i, self.model.invisibleRootItem())

    def createJsonUi(self, obj, parent: QStandardItem):
        if isinstance(obj.value, Jso.JObject):
            items = []
            for h in self.headerData:
                if h['key'] in obj.value:
                    item = QStandardItem(obj.value.getItem(h['key']).getValueStr())
                    item.setEditable(h['editable'])
                    item.setData(self.getItemData(obj.value.getItem(h['key']), obj))
                else:
                    key = Jso.JKey(h['key'], "")
                    obj.value.addKey(key)
                    item = QStandardItem('')
                    item.setEditable(True)
                    item.setData(self.getItemData(key, obj))
                items.append(item)
            parent.appendRow(items)

    def dataChange(self, item: QStandardItem):
        data = item.data()
        if data is not None:
            jObj = data['item']
            if isinstance(jObj, Jso.JKey) or isinstance(jObj, Jso.JIndex):
                jObj.value = self.keyDecode(item.text())
            self.treeView.pushSignal()
            self.flow.add(copy.deepcopy(self.jsonData))

    def getItemData(self, item, par):
        return {"item": item, 'parent':par}

    def keyDecode(self, text: str):
        if text.isnumeric():
            return int(text)
        elif text.startswith("'"):
            return text[1:]
        else:
            return text

    def openMenu(self, position):
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
            ite = None
            par = None
        else:
            ite = data['item']
            par = data['parent']

        if ite is None:
            self.createMenu(position, 0, ite, par, item)
        else:
            self.createMenu(position, 1, ite, par, item)

    def createMenu(self, position, tpe, obj, par, item):
        # global
        undoAction = QAction('Undo', self.treeView)
        undoAction.setEnabled(not self.flow.isEnd())
        redoAction = QAction('Redo', self.treeView)
        redoAction.setEnabled(not self.flow.isFirst())
        copyAsJSON = QAction('Copy as JSON', self.treeView)
        clearAll = QAction('Clear table', self.treeView)

        # delete
        copyTextAction = QAction('Copy text', self.treeView)
        pasteTextAction = QAction("Paste text", self.treeView)
        deleteKeyAction = QAction('Delete line', self.treeView)

        # add new
        addNewAction = QAction('New line', self.treeView)

        menu = QMenu()
        Utilities.Style.applyStyle(menu)
        if self.treeView.editable:
            menu.addAction(undoAction)
            menu.addAction(redoAction)

        menu.addAction(copyAsJSON)
        if self.treeView.editable:
            menu.addAction(clearAll)
            menu.addSeparator()

        if self.treeView.editable:
            if tpe:  # line
                menu.addAction(copyTextAction)
                menu.addAction(pasteTextAction)
                menu.addAction(addNewAction)
                menu.addAction(deleteKeyAction)
            else:  # table
                menu.addAction(addNewAction)
        else:
            if  tpe == 1:
                menu.addAction(copyTextAction)
        action = menu.exec_(self.treeView.viewport().mapToGlobal(position))

        if action == undoAction:
            self.flowAction(1)
        elif action == redoAction:
            self.flowAction(0)
        elif action == copyAsJSON:
            self.actionCopyAsJSON()
        elif action == clearAll:
            self.actionClearAll()
        elif action == copyTextAction:
            self.actionCopyText(item)
        elif action == pasteTextAction:
            self.actionPasteText(item)
        elif action == deleteKeyAction:
            self.actionDelete(self.jsonData.get('JSON'), par)
        elif action == addNewAction:
            self.actionAddValue(self.jsonData.get('JSON'), par)

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
        text = Jso.toString(self.jsonData.get('JSON'))
        import clipboard
        clipboard.copy(text)

    def actionClearAll(self):
        self.jsonData = Jso.fromObject([])
        self.treeView.refresh()
        self.treeView.pushSignal()
        self.flow.add(copy.deepcopy(self.jsonData))

    def actionDelete(self, par, obj):
        par.remove(obj)
        self.treeView.refresh()
        self.treeView.pushSignal()
        self.flow.add(copy.deepcopy(self.jsonData))

    def actionAddValue(self, par, obj):
        if obj is not None:
            inx = par.index(obj) + 1
            new = Jso.JIndex(inx, Jso.copyObject(obj.value))
        else:
            inx = -1
            new = Jso.JIndex(par.count(), self.createLine())
        par.append(new, inx)
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.jsonData))

    def createLine(self):
        obj = Jso.JObject()
        for col in self.headerData:
            obj.addKey(Jso.JKey(col['key'], ""))
        return obj
