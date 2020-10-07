from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QVBoxLayout, QLineEdit, QHBoxLayout, QListWidget, QStyleOption, QStyle, \
    QToolButton, QStackedWidget

from xu.compa.Parapluie import Parapluie, PFunction, PResource, PGridWidget, PWidget
from xu.compa.xhash import XashList, Xash
from xu.src.python.Model.ItemModel import ItemModel
from xu.src.python.Module import ItemAdapter, GridAdapter


class RequestNavigation(PWidget):
    def __init__(self):
        super().__init__()

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

        topBar = QHBoxLayout()
        topBar.addWidget(self.backButton)
        topBar.addWidget(self.searchBar)
        topBar.addWidget(self.addButton)

        listData = QListWidget()

        self.gridData = PGridWidget(2)
        self.gridData.setContentsMargins(0, 0, 0, 0)
        self.gridData.setHorizontalSpacing(5)
        self.gridData.setVerticalSpacing(5)
        self.gridData.setFixColumn(True)
        self.gridData.setRowHeight(100)
        self.gridData.setAlignment(Qt.AlignTop | Qt.AlignHCenter)

        self.stacked = QStackedWidget()
        self.stacked.addWidget(self.gridData)
        self.stacked.addWidget(listData)
        self.stacked.currentChanged.connect(self.tabChange)

        layout = QVBoxLayout()
        layout.addLayout(topBar)
        layout.addWidget(self.stacked)

        self.setObjectName(Parapluie.Object_Raised)
        self.setStyleSheet("QWidget{background:white}")
        self.setFixedWidth(299)
        self.setContentsMargins(0, 0, 0, 0)
        self.setLayout(layout)
        PFunction.applyShadow(self)

        self.dataList = []
        self.categories = []
        self.lastSearch = {1: "", 0: ""}
        self.dataXash = XashList()
        self.listAdapter = ItemAdapter(listData, self.dataList)
        gridAdapter = GridAdapter(data=self.categories)
        gridAdapter.setOnItemClick(self.onCategoriesClicked)
        self.gridData.setAdapter(gridAdapter)

        self.stacked.setCurrentIndex(0)
        self.tabChange(0)
        self.loadFile()

    def loadFile(self):
        self.dataXash.clear()
        self.dataXash.load("C:\\Users\\DEV-C2-2\\PythonProject\\XuCompa-Request\\xu\\compa\\xhash\\example")
        self.dataList.clear()
        self.categories.clear()
        for data in self.dataXash.list:
            d: Xash = data
            item = ItemModel()
            item.file = data
            c = d.categories.category if d.categories is not None else ""
            if c != "" and c not in self.categories:
                self.categories.append(c)
            self.dataList.append(item)
        self.listAdapter.refresh()
        self.gridData.refresh()

    def updateDataList(self, lst):
        self.dataList.clear()
        for data in lst:
            item = ItemModel()
            item.file = data
            self.dataList.append(item)

    def searchFile(self, a0: str):
        if self.stacked.currentIndex() == 1:
            self.lastSearch[1] = a0
            if a0 == "":
                self.updateDataList(self.dataXash.list)
            else:
                if a0.startswith("categories:"):
                    self.updateDataList(self.dataXash.findWithCategory(a0.replace("categories:", "")))
                elif a0.startswith("name:"):
                    self.updateDataList(self.dataXash.findWithName(a0.replace("name:", "")))
                else:
                    self.updateDataList(self.dataXash.findEveryWhere("", a0, "description#" + a0))
            self.listAdapter.refresh()
        else:
            self.lastSearch[0] = a0
            self.categories.clear()
            if a0 == "":
                for data in self.dataXash.list:
                    d: Xash = data
                    c = d.categories.category if d.categories is not None else ""
                    if c != "" and c not in self.categories:
                        self.categories.append(c)
            else:
                for data in self.dataXash.list:
                    d: Xash = data
                    c = d.categories.category if d.categories is not None else ""
                    if c != "" and c not in self.categories and a0 in c:
                        self.categories.append(c)
            self.gridData.refresh()

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)

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
