import copy
import logging
import xml.etree.ElementTree as Et

from PyQt5.QtGui import QStandardItem
from PyQt5.QtWidgets import QAction, QMenu

import xu.src.python.Module.ParamEditor as ParamEditor
from xu.src.python import Utilities



class XMLView:
    def __init__(self, treeView, model):
        self.treeView: ParamEditor.ParamEditor = treeView
        self.model = model
        self.xmlData = None
        self.flow = ParamEditor.ActionFlow()

    def setData(self, param):
        self.xmlData: Et.Element = param
        self.flow.add(copy.deepcopy(self.xmlData))

    def createUI(self):
        if self.xmlData is not None:
            self.createXmlUi(self.xmlData, self.model.invisibleRootItem(), None)

    def createXmlUi(self, obj: Et.Element, parent: QStandardItem, xmlParent):
        item = QStandardItem(obj.tag)
        item.setEditable(True and self.treeView.editable)
        item.setData(self.getItemData(obj, "tag", parent=xmlParent))
        if obj.text is not None and not obj.text.isspace():
            value = QStandardItem(obj.text.strip())
        else:
            value = QStandardItem("")
        value.setEditable(True and self.treeView.editable)
        value.setData(self.getItemData(obj, "value", parent=xmlParent))
        if obj.attrib != {}:
            for att in obj.attrib:
                self.createAttr(obj, att, obj.attrib[att], item)
        parent.appendRow([item, value])
        for elem in obj:
            self.createXmlUi(elem, item, obj)

    def createAttr(self, elem, key, value, parent: QStandardItem):
        item = QStandardItem('@' + key)
        item.setEditable(True and self.treeView.editable)
        item.setData(self.getItemData(elem, "property", key))
        val = QStandardItem(value)
        val.setEditable(True and self.treeView.editable)
        val.setData(self.getItemData(elem, "property-value", item))
        parent.appendRow([item, val])

    def dataChange(self, item: QStandardItem):
        data = item.data()
        if data is not None:
            elem: Et.Element = data['item']
            if data['type'] == 'value':
                elem.text = item.text()
            elif data['type'] == 'property-value':
                if data['key'] is not None:
                    elem.set(data['key'].text().replace('@', ''), item.text())
            elif data['type'] == 'tag':
                elem.tag = item.text()
            elif data['type'] == 'property':
                key = data['key']
                text: str = item.text()
                if text.startswith('@'):
                    text = text[1:]
                else:
                    item.setText('@' + text)
                if text != key:
                    if key in elem.attrib:
                        elem.attrib[text] = elem.attrib[key]
                        del elem.attrib[key]
                        self.treeView.refresh()
            self.treeView.pushSignal()
            self.flow.add(copy.deepcopy(self.xmlData))

    def keyDecode(self, value):
        pass

    def getItemData(self, item, tpe, key=None, parent=None):
        return {"item": item, 'type': tpe, 'key': key, 'parent': parent}

    def openMenu(self, position):
        indexes = self.treeView.selectedIndexes()

        isItem = len(indexes) > 0
        data = None
        if isItem:
            index = indexes[0]
            item = self.model.itemFromIndex(index)
            data = item.data()

        if data is not None:
            elem = data['item']
            tpe = data['type']
            prop = data['key']
            par = data['parent']
        else:
            elem = self.xmlData
            tpe = None
            prop = None
            par = None

        if tpe is not None and tpe.startswith('property'):
            self.createMenu(position, 1, elem, prop, par)
        else:
            if par is None:
                self.createMenu(position, 2, elem, prop, par)
            else:
                self.createMenu(position, 0, elem, prop, par)

    def createMenu(self, position, tpe, elem, prop, par):
        # global
        undoAction = QAction('Undo', self.treeView)
        undoAction.setEnabled(not self.flow.isEnd())
        redoAction = QAction('Redo', self.treeView)
        redoAction.setEnabled(not self.flow.isFirst())
        copyAsXML = QAction('Copy as XML', self.treeView)
        pasteAsXML = QAction('Paste as XML', self.treeView)
        clearAll = QAction('Clear table', self.treeView)

        # delete
        deleteTagAction = QAction('Delete tag', self.treeView)
        deletePropertyAction = QAction('Delete property', self.treeView)

        # duplicate
        duplicateAction = QAction('Duplicate', self.treeView)

        # add
        addMenu = QMenu("Add..")
        Utilities.Style.applyStyle(addMenu)

        # add child
        addChildAction = QAction('Add Child', self.treeView)

        # add property
        addPropertyAction = QAction('Add Property', self.treeView)

        # new
        newDocument = QAction('New document', self.treeView)

        addMenu.addAction(addChildAction)
        addMenu.addAction(addPropertyAction)

        menu = QMenu()
        Utilities.Style.applyStyle(menu)
        if self.treeView.editable:
            menu.addAction(undoAction)
            menu.addAction(redoAction)
            menu.addSeparator()
        menu.addAction(copyAsXML)
        if self.treeView.editable:
            menu.addAction(pasteAsXML)
            menu.addAction(clearAll)
            menu.addSeparator()

        if self.treeView.editable:
            if tpe == 0:  # tag
                menu.addAction(duplicateAction)
                menu.addMenu(addMenu)
                menu.addAction(deleteTagAction)
            elif tpe == 1:  # property
                menu.addAction(addPropertyAction)
                if prop is not None:
                    menu.addAction(deletePropertyAction)
            else:  # root
                if self.xmlData is None:
                    menu.addAction(newDocument)
                else:
                    menu.addAction(addChildAction)
                    menu.addAction(addPropertyAction)

        action = menu.exec_(self.treeView.viewport().mapToGlobal(position))

        if action == undoAction:
            self.flowAction(1)
        elif action == redoAction:
            self.flowAction(0)
        elif action == copyAsXML:
            self.actionCopyAsXML()
        elif action == pasteAsXML:
            self.actionPasteAsXML()
        elif action == clearAll:
            self.actionClearAll()
        elif action == duplicateAction:
            self.actionDuplicate(elem, par)
        elif action == deleteTagAction:
            self.actionDeleteTag(elem, par)
        elif action == deletePropertyAction:
            self.actionDeleteProperty(elem, prop)
        elif action == addChildAction:
            self.actionAddChild(elem)
        elif action == addPropertyAction:
            self.actionAddProperty(elem)
        elif action == newDocument:
            self.actionNewDocument()

    def flowAction(self, flow):
        if flow == 1:
            self.xmlData = self.flow.previous()
            self.treeView.refresh()
            self.treeView.pushSignal()
        else:
            self.xmlData = self.flow.next()
            self.treeView.refresh()
            self.treeView.pushSignal()

    def actionCopyAsXML(self):
        try:
            text: bytes = Et.tostring(self.xmlData, encoding='utf8')
            from xml.dom import minidom
            repaired = minidom.parseString(text.decode('utf-8'))
            newText = '\n'.join([line for line in repaired.toprettyxml(indent='\t').split('\n') if line.strip()])
            import clipboard
            clipboard.copy(newText)
        except Exception as ex:
            logging.exception(ex)
            self.treeView.error.emit(str(ex))

    def actionPasteAsXML(self):
        import clipboard
        text = clipboard.paste()
        try:
            self.xmlData = Et.fromstring(text)
            self.treeView.pushSignal()
            self.treeView.refresh()
            self.flow.add(copy.deepcopy(self.xmlData))
        except Exception as ex:
            logging.exception(ex)
            self.treeView.error.emit(str(ex))

    def actionClearAll(self):
        self.xmlData = None
        self.treeView.pushSignal()
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.xmlData))

    def actionNewDocument(self):
        self.xmlData = Et.Element('Document')
        self.treeView.pushSignal()
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.xmlData))

    def actionDuplicate(self, elem, par: Et.Element):
        if par is not None:
            new = copy.deepcopy(elem)
            inx = list(par).index(elem)
            par.insert(inx, new)
            self.treeView.pushSignal()
            self.treeView.refresh()
            self.flow.add(copy.deepcopy(self.xmlData))

    def actionDeleteTag(self, elem: Et.Element, par):
        if par is not None:
            par.remove(elem)
            self.treeView.pushSignal()
            self.treeView.refresh()
            self.flow.add(copy.deepcopy(self.xmlData))

    def actionDeleteProperty(self, elem: Et.Element, prop):
        if prop in elem.attrib:
            del elem.attrib[prop]
            self.treeView.pushSignal()
            self.treeView.refresh()
            self.flow.add(copy.deepcopy(self.xmlData))

    def actionAddChild(self, elem):
        Et.SubElement(elem, 'NewChild')
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.xmlData))

    def actionAddProperty(self, elem: Et.Element):
        elem.set("NewProperty", "")
        self.treeView.refresh()
        self.flow.add(copy.deepcopy(self.xmlData))
