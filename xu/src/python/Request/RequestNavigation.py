import os

from PyQt5 import QtGui
from PyQt5.QtCore import Qt, pyqtSignal, QPoint, QRect
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QHBoxLayout, QListWidget, QToolButton, QStackedWidget, QSizePolicy, \
    QFileDialog, QApplication

from xu.compa.Parapluie import Parapluie, PResource, PGridWidget, PWidget, PMessage
from xu.compa.xhash import XashList, Xash, XashHelp
from xu.src.python import Utilities
from xu.src.python.Model import XFile
from xu.src.python.Model.ItemModel import ItemModel
from xu.src.python.Module import GridAdapter
from xu.src.python.Module.ParamEditor import Formatter, EditorType
from xu.src.python.Request.Adapter import ItemAdapter
from xu.src.python.Utilities import Config


def inRequestFolder(path):
    return os.path.dirname(path) == Config.getRequestFolder()[0]


class RequestNavigation(PWidget):
    alert = pyqtSignal(str, str, object, object)
    currentChange = pyqtSignal()

    def __init__(self):
        super().__init__()
        self.setMaximumWidth(600)
        self.setObjectName(Parapluie.Object_Raised)

        self.backButton = QToolButton()
        self.backButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Left_Arrow_Svg))
        self.backButton.setFixedSize(36, 36)
        self.backButton.pressed.connect(self.onBackPressed)

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
        topBar.addWidget(self.backButton)
        topBar.addWidget(self.searchBar)
        topBar.addWidget(self.openButton)
        topBar.addWidget(self.addButton)

        self.listDataWidget = QListWidget()
        self.listDataWidget.setObjectName(Parapluie.Object_Raised)
        self.listDataWidget.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.listDataWidget.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
        self.listDataWidget.horizontalScrollBar().setEnabled(False)

        self.gridData = PGridWidget(2)
        self.gridData.setObjectName(Parapluie.Object_Raised)
        self.gridData.setContentsMargins(0, 0, 0, 0)
        self.gridData.setHorizontalSpacing(5)
        self.gridData.setVerticalSpacing(5)
        self.gridData.setFixColumn(True)
        self.gridData.setRowHeight(100)
        self.gridData.setAlignment(Qt.AlignTop | Qt.AlignLeft)

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.gridData)
        self.stacked.addWidget(self.listDataWidget)
        self.stacked.currentChanged.connect(self.tabChange)

        layout = QVBoxLayout()
        layout.addLayout(topBar)
        layout.addWidget(self.stacked)

        self.setLayout(layout)

        self.categoriesChange = None

        self.dataList = []  # combine
        self.categories = []  # string
        self.dataSource = XashList()
        self.dataTemp = []  # xfile
        self.listFile = []  # xfile

        self.currentFile = None
        self.newCount = -1
        self.lastSearch = {1: "", 0: ""}

        self.listAdapter = ItemAdapter(self,
                                       self.listDataWidget,
                                       self.dataList,
                                       self.dataSource,
                                       self.onItemSelected,
                                       self.onItemClosed)

        gridAdapter = GridAdapter(data=self.categories)
        gridAdapter.setOnItemClick(self.onCategoriesClicked)
        self.gridData.setAdapter(gridAdapter)

        self.stacked.setCurrentIndex(1)
        self.tabChange(1)
        self.loadFile()

    def loadFile(self):
        self.dataSource.clear()
        self.dataSource.load(Config.getRequestFolder()[0])
        self.updateCategories(self.dataSource.list)
        self.updateDataList(self.dataTemp, self.dataSource.list)
        self.listAdapter.refresh()
        self.gridData.refresh()

    def updateCategories(self, lstSrc):
        self.categories.clear()
        self.categories.append("all")
        self.categories.append('recent')
        for data in lstSrc:
            c = data.categories.category if data.categories is not None else ""
            if c != "" and c not in self.categories:
                self.categories.append(c)
        if self.categoriesChange is not None:
            self.categoriesChange(self.categories)

    def searchFile(self, a0: str):
        if self.stacked.currentIndex() == 1:
            self.lastSearch[1] = a0
            if a0 == "" or a0 == "categories:all":
                self.updateDataList(self.dataTemp, self.dataSource.list)
            elif a0 == 'categories:recent':
                self.updateDataList(self.dataTemp, [])
            else:
                if a0.startswith("categories:"):
                    self.updateDataList([], self.dataSource.findWithCategory(a0.replace("categories:", "")))
                elif a0.startswith("name:"):
                    self.updateDataList([], self.dataSource.findWithName(a0.replace("name:", "")))
                else:
                    self.updateDataList([], self.dataSource.findEveryWhere("", a0, "description#" + a0))
            self.listAdapter.refresh()
        else:
            self.lastSearch[0] = a0
            self.categories.clear()
            if a0 == "":
                self.categories.append("all")
                self.categories.append('recent')
                for data in self.dataSource.list:
                    d: Xash = data
                    c = d.categories.category if d.categories is not None else ""
                    if c != "" and c not in self.categories:
                        self.categories.append(c)
            else:
                for data in self.dataSource.list:
                    d: Xash = data
                    c = d.categories.category if d.categories is not None else ""
                    if c != "" and c not in self.categories and a0 in c:
                        self.categories.append(c)
            self.gridData.refresh()

    def tabChange(self, index):
        if index == 1:
            self.backButton.setVisible(True)
            self.searchBar.setText(self.lastSearch[1])
            self.searchBar.blockSignals(False)
        else:
            self.backButton.setVisible(False)
            self.searchBar.setText(self.lastSearch[0])

    def onCategoriesClicked(self, txt):
        self.stacked.setCurrentIndex(1)
        self.searchBar.setText("categories:" + txt)

    def onBackPressed(self):
        self.stacked.setCurrentIndex(0)

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        super(RequestNavigation, self).resizeEvent(a0)
        col = int(self.width() / 150) + 1
        self.gridData.setNumberColumn(col)

    def refresh(self):
        self.listAdapter.refresh()
        self.gridData.refresh()

    def newFile(self):
        self.newCount += 1
        file = XFile("Unsaved/Untitled-" + str(self.newCount))
        self.dataTemp.insert(0, file)
        self.onItemSelected(file)
        self.updateDataList(self.dataTemp, self.dataSource.list)
        self.refresh()

    def pushAlert(self, text, tpe=Parapluie.Alert_Error):
        self.alert.emit(text, tpe, None, None)

    def openFile(self):
        init_dir = Config.getRequestConfig_LastOpen()

        name = QFileDialog.getOpenFileName(self, 'Open file', init_dir,
                                           "XuCompa Request (*.xreq);; JSON files (*.json);; All files (*)")
        if name[0] != "":
            config = Config.getConfig()
            config["viewer"]["last_open"] = os.path.dirname(name[0])
            Config.updateConfig(config)

            file = XFile(name[0])
            self.dataTemp.insert(0, file)
            self.onItemSelected(file)
            self.updateDataList(self.dataTemp, self.dataSource.list)
            self.refresh()

    def updateDataList(self, lstNew, lstSrc):
        self.dataList.clear()
        if len(lstNew):
            # header item
            item = ItemModel()
            item.file = "Recent File"
            item.selected = -1
            self.dataList.append(item)
            for data in lstNew:  # XFile
                item = ItemModel()
                item.file = data
                item.selected = 1 if self.currentFile == data else 0
                self.dataList.append(item)

        if len(lstSrc) > 0:
            # header item
            item = ItemModel()
            item.file = "Request Folder"
            item.selected = -1
            self.dataList.append(item)
            for data in lstSrc:  # Xash
                item = ItemModel()
                if data.getPath() in self.listFile:
                    inx = self.listFile.index(data.getPath())
                    file = self.listFile[inx]
                else:
                    file = XFile(data.getPath())
                    self.listFile.append(file)
                item.file = file
                item.selected = 1 if self.currentFile == file else 0
                self.dataList.append(item)

    def onItemSelected(self, data):
        if isinstance(data, XFile):

            self.currentFile = data
            self.currentChange.emit()

            for item in self.dataList:
                if item.file == data:
                    item.selected = 1
                else:
                    item.selected = 0
                self.refresh()

    def onItemClosed(self, data):
        if self.currentFile == data:
            self.currentFile = None
            self.currentChange.emit()

        if isinstance(data, XFile):
            if inRequestFolder(data.getPath()):
                message = PMessage(self, QRect(QPoint(0, 0), QApplication.focusWindow().screen().size()))
                Utilities.Style.applyWindowIcon(message)
                message.initWarning("Are you want delete this item!", negative="Delete")
                code = message.exec_()
                if code == 1:
                    # remove description
                    xash = XashHelp.path2Xash(data.getPath())
                    xashId = xash.getId()
                    self.saveDescription("", xashId, True)

                    # remove file
                    os.remove(data.getPath())

        if data in self.dataList:
            self.dataList.remove(data)
        if data in self.dataTemp:
            self.dataTemp.remove(data)
        self.loadFile()

    def saveData(self, file: XFile, newData):
        if file.unsavedData is not None:  # has data unsaved
            if inRequestFolder(file.getPath()):
                self.saveExistedInRequest(file, newData)
            else:
                self.saveNewFile(file, newData)

    def getSavePath(self, name, category, description) -> str:
        # create new xashID
        xashId = XashHelp.newXashId(category, self.dataSource)
        # write description
        descId = self.saveDescription(description, xashId)
        # gotta new xash string
        x = XashHelp.createXash(name, xashId, {'description': descId}, '.xreq')
        # join with folder
        path = os.path.join(Config.getRequestFolder()[0], x)
        return path

    def saveDescription(self, desc, descId=None, isRemove=False):
        # read descriptions
        xDef = Config. getRequestFolder()[1]
        if os.path.isfile(xDef):
            file = open(xDef, "r", encoding='utf-8')
            data = file.read()
            file.close()
        else:
            data = ''

        # edit
        listDesc = data.split("\n")
        if descId is None and not isRemove:
            newId = '[desc#%s]' % str(len(listDesc))
            lines = newId + 'xreq_description--description#' + desc
            listDesc.append(lines)
        else:
            newId = descId
            exist = False
            for d in listDesc:
                if d.startswith(newId):
                    inx = listDesc.index(d)
                    if not isRemove:
                        listDesc[inx] = newId + 'xreq_description--description#' + desc
                        exist = True
                    else:
                        listDesc.remove(d)
                    break
            if not exist:
                lines = newId + 'xreq_description--description#' + desc
                listDesc.append(lines)

        # save
        file = open(xDef, "w", encoding='utf-8')
        data = "\n".join(listDesc)
        file.write(data)
        file.close()
        return newId

    def saveNewFile(self, file: XFile, newData):
        temp = self.dataSource.findMatchAll(newData[1], newData[0], "", sensitive=False)
        if len(temp) > 0:
            self.pushAlert("File was existed!!!")
        else:
            # data
            text = Formatter.dumps(file.unsavedData.data, EditorType.JSON, self.pushAlert)
            path = self.getSavePath(newData[0], newData[1], newData[2])
            if self.save(file, path, text):
                if file in self.dataTemp:
                    self.dataTemp.remove(file)
                self.loadFile()

    def saveExistedInRequest(self, file: XFile, newData: tuple):
        # data
        text = Formatter.dumps(file.unsavedData.data, EditorType.JSON, self.pushAlert)
        xash = XashHelp.path2Xash(file.getPath())

        if xash.getCategory() == newData[1] and xash.getName() == newData[0]:
            # replace existed description
            xashId = xash.getId()
            self.saveDescription(newData[2], xashId)

            if self.save(file, file.getPath(), text):
                self.loadFile()
        else:
            temp = self.dataSource.findMatchAll(newData[1], newData[0], "", sensitive=False)
            if len(temp) > 0:
                self.pushAlert("File was existed!!!")
            else:
                message = PMessage(self, QRect(QPoint(0, 0), QApplication.focusWindow().screen().size()))
                message.initQuestion("File is saved, do you want to rename or create new file?",
                                     [{"text": "Rename", 'type': Parapluie.Button_Negative},
                                      {"text": "New File", 'type': Parapluie.Button_Positive},
                                      {"text": "Close", 'type': Parapluie.Button_Neutral}],
                                     'Save request')
                code = message.exec_()
                if code == 0:
                    # remove old description
                    xashId = xash.getId()
                    self.saveDescription(newData[2], xashId, True)

                    path = self.getSavePath(newData[0], newData[1], newData[2])

                    os.rename(file.getPath(), path)

                    if self.save(file, path, text):
                        self.loadFile()
                elif code == 1:
                    path = self.getSavePath(newData[0], newData[1], newData[2])
                    if self.save(file, path, text):
                        self.loadFile()

    def save(self, file: XFile, path, text) -> bool:
        try:
            f = open(path, 'w', encoding='utf-8')
            f.write(text)
            f.close()

            file.unsavedData = None
            file.setPath(path)
            file.data = XashHelp.path2Xash(path)

            self.pushAlert("Saved!!!", Parapluie.Alert_Success)
            return True
        except Exception as ex:
            print(RequestNavigation, ex, 401)
            self.pushAlert(str(ex))
            return False
