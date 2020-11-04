import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QHBoxLayout, QListWidget, QToolButton, QFileDialog

from xu.compa.Parapluie import PResource, PWidget
from xu.src.python.JsonViewer.Adapter import JsonAdapter
from xu.src.python.Model import XFile
from xu.src.python.Model.ItemModel import ItemModel
from xu.src.python.Utilities import *


class JSONNavigation(PWidget):
    currentChange = pyqtSignal()

    def __init__(self):
        super().__init__()

        self.searchBar = QLineEdit()
        self.searchBar.setPlaceholderText("Search..")
        self.searchBar.textChanged.connect(self.searchFile)
        self.searchBar.setFixedHeight(36)

        self.addButton = QToolButton()
        self.addButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Plus_Svg))
        self.addButton.setFixedSize(36, 36)
        self.addButton.pressed.connect(self.newFile)

        self.openButton = QToolButton()
        self.openButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Folder_Svg))
        self.openButton.setFixedSize(36, 36)
        self.openButton.pressed.connect(self.openFile)

        topBar = QHBoxLayout()
        topBar.addWidget(self.searchBar)
        topBar.addWidget(self.openButton)
        topBar.addWidget(self.addButton)

        self.listDataWidget = QListWidget()
        self.listDataWidget.setObjectName(Parapluie.Object_Raised)
        self.listDataWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listDataWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.listDataWidget.horizontalScrollBar().setEnabled(False)

        layout = QVBoxLayout()
        layout.addLayout(topBar)
        layout.addWidget(self.listDataWidget)

        self.setObjectName(Parapluie.Object_Raised)
        self.setFixedWidth(300)
        self.setLayout(layout)
        # PFunction.applyShadow(self)

        self.dataList = []
        self.dataSource = []
        self.dataTemp = []
        self.currentFile = None
        self.newCount = -1

        self.listAdapter = JsonAdapter(self, self.listDataWidget, self.dataList, self.onItemSelected, self.onItemClosed)

        self.loadFile()

    def loadFile(self):
        if os.path.isfile(Config.getViewerRecentFile()):
            file = open(Config.getViewerRecentFile(), 'r', encoding='utf-8')
            data = file.read().splitlines()
            for d in data:
                if d not in self.dataSource:
                    self.dataSource.insert(0, XFile(d))
            self.updateDataList(self.dataTemp, self.dataSource)
            file.close()
        else:
            file = open(Config.getViewerRecentFile(), 'w', encoding='utf-8')
            file.close()

    def addRecentFile(self, f: XFile):
        if os.path.isfile(Config.getViewerRecentFile()):
            file = open(Config.getViewerRecentFile(), 'r', encoding='utf-8')
            data = file.read().splitlines()
            file.close()
            if f.getPath() not in data:
                data.append(f.getPath())
            else:
                data.remove(f.getPath())
                data.append(f.getPath())
            file = open(Config.getViewerRecentFile(), 'w', encoding='utf-8')
            file.write("\n".join(data))
            file.close()
        else:
            file = open(Config.getViewerRecentFile(), 'a+', encoding='utf-8')
            file.write(f.getPath() + "\n")
            file.close()

    def removeFile(self, f: XFile):
        if os.path.isfile(Config.getViewerRecentFile()):
            file = open(Config.getViewerRecentFile(), 'r', encoding='utf-8')
            data = file.read().splitlines()
            file.close()
            if f.getPath() in data:
                data.remove(f.getPath())
                file = open(Config.getViewerRecentFile(), 'w', encoding='utf-8')
                file.write("\n".join(data))
                file.close()
        else:
            file = open(Config.getViewerRecentFile(), 'a+', encoding='utf-8')
            file.close()

    def updateDataList(self, lstNew, lstSrc):
        self.dataList.clear()
        # unsaved item
        for data in lstNew:
            item = ItemModel()
            item.file = data
            if data == self.currentFile:
                item.selected = 1
            else:
                item.selected = 0
            self.dataList.append(item)
        if len(lstSrc) > 0:
            # header item
            item = ItemModel()
            item.file = "Recent File"
            item.selected = -1
            self.dataList.append(item)
            # recent item
            for data in lstSrc:
                item = ItemModel()
                item.file = data
                if data == self.currentFile:
                    item.selected = 1
                else:
                    item.selected = 0
                self.dataList.append(item)

    def searchFile(self, a0: str):
        if a0 == "":
            self.updateDataList(self.dataTemp, self.dataSource)
        else:
            lst = []
            for i in self.dataSource:
                if a0.lower() in i.name()[0].lower():
                    lst.append(i)
            self.updateDataList([], lst)
        self.listAdapter.refresh()

    def newFile(self):
        self.newCount += 1
        json = XFile("Unsaved\\Untitled-" + str(self.newCount))
        self.currentFile = json
        self.dataTemp.insert(0, json)
        self.updateDataList(self.dataTemp, self.dataSource)
        self.listAdapter.refresh()
        self.currentChange.emit()

    def onItemSelected(self, data):
        if self.currentFile != data:
            self.currentFile = data
            self.currentChange.emit()

        if isinstance(data, XFile):
            for item in self.dataList:
                if item.file == data:
                    item.selected = 1
                else:
                    item.selected = 0
        self.listAdapter.refresh()

    def onItemClosed(self, data):
        if self.currentFile == data:
            self.currentFile = None
            self.currentChange.emit()

        for i in self.dataList:
            if i.file == data:
                self.dataList.remove(i)
                break
        if data in self.dataSource:
            self.dataSource.remove(data)
        if data in self.dataTemp:
            self.dataTemp.remove(data)

        self.removeFile(data)

        self.searchFile(self.searchBar.text())

    def openFile(self):
        init_dir = Config.getViewerConfig_LastOpen()
        file_ext = """All files (*);;
                        JSON files (*.json);;
                        XML files (*.xml);;
                        HTML files (*.html);;
                        Javascript files (*.js)"""
        name = QFileDialog.getOpenFileName(self, 'Open file', init_dir, file_ext)
        if name[0] != "":
            config = Config.getConfig()
            config["viewer"]["last_open"] = os.path.dirname(name[0])
            Config.updateConfig(config)

            self.fileChanged(name[0])

    def fileChanged(self, path: str):
        file = XFile(path)
        self.currentFile = file
        if path in self.dataTemp:
            self.dataTemp.remove(path)
        if path in self.dataSource:
            self.dataSource.remove(file)
        self.addRecentFile(file)
        self.loadFile()
        self.updateDataList(self.dataTemp, self.dataSource)
        self.listAdapter.refresh()
        self.currentChange.emit()
