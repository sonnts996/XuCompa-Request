from typing import TypeVar, Generic, Tuple

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListWidget, QListWidgetItem

from xu.compa.Parapluie.src.ActionWidget import PHolder


class PListAdapter:
    def __init__(self, layout: QListWidget):
        self.layout: QListWidget = layout
        self.layout.setSizeAdjustPolicy(QListWidget.AdjustToContents)
        self.dataList = []

    def count(self) -> int:
        return len(self.dataList)

    def item(self, index: int):
        if index < self.count():
            return self.dataList[index]
        else:
            return None

    def refresh(self):
        self.updateLayout()

    def updateLayout(self):
        numItem = self.layout.count()
        if self.count() >= numItem:
            for i in range(numItem):
                item = self.layout.item(i)
                self.layout.removeItemWidget(item)
                self.fixItem(item, i)

            for i in range(numItem, self.count()):
                item = QListWidgetItem()
                self.layout.addItem(item)
                self.fixItem(item, i)
        else:
            for i in reversed(range(numItem)):
                if i < self.count():
                    index = self.count() - i - 1
                    item = self.layout.item(index)
                    self.layout.removeItemWidget(item)
                    self.fixItem(item, index)
                else:
                    item = self.layout.item(i)
                    self.layout.removeItemWidget(item)
                    self.layout.takeItem(i)

    def fixItem(self, item: QListWidgetItem, index: int):
        new, selected, data = self.__getWidget__(index)
        item.setData(Qt.UserRole, data)
        item.setSizeHint(new.itemSize())
        if selected < 0:
            item.setFlags(item.flags() & ~ Qt.ItemIsSelectable)
        else:
            item.setFlags(item.flags() | Qt.ItemIsSelectable)
            item.setSelected(selected > 0)
        self.layout.setItemWidget(item, new)

    def __getWidget__(self, position, w=None) -> Tuple[PHolder, int, object]:
        w, selected, data = self.getWidget(position, w)
        # w.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        return w, selected, data

    def getWidget(self, position: int, w: PHolder = None) -> Tuple[PHolder, int, object]:
        if w is None:
            w = PHolder()
        return w, 0, None
