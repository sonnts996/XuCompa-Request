from typing import TypeVar, Generic

from PyQt5.QtWidgets import QGridLayout

T = TypeVar('T')


class PGridAdapter(Generic[T]):
    def __init__(self, layout: QGridLayout = None, numCol: int = 1):
        self.layout: QGridLayout = layout
        self.dataList = []
        self.numCol = numCol
        self.colWidth = -1
        self.rowHeight = -1
        self.itemList = []

    def setNumCol(self, numCol: int):
        self.numCol = numCol

    def setColumnWidth(self, colWidth):
        self.colWidth = colWidth

    def setRowHeight(self, rowHeight):
        self.rowHeight = rowHeight

    def setLayout(self, layout: QGridLayout):
        self.layout = layout

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
        if self.layout is not None:
            self.clear()

            numRow = int(self.count() / self.numCol)
            numRow = numRow + 1 if self.count() % self.numCol != 0 else numRow
            for c in range(self.numCol):
                for r in range(numRow):
                    index = r * self.numCol + c
                    if index >= self.count():
                        break
                    else:
                        w, selected = self.__getWidget__(index)
                        self.itemList.append(w)
                        self.layout.addWidget(w, r + 1, c + 1)

    def clear(self):
        if self.layout is not None:
            while self.layout.count() > 0:
                item = self.layout.takeAt(0)
                if item.widget() is not None:
                    item.widget().hide()
                    self.layout.removeWidget(item.widget())
                    self.layout.removeItem(item)

    def __getWidget__(self, position, w=None) -> T:
        w, selected = self.getWidget(position, w)
        if self.colWidth > 0:
            w.setFixedWidth(self.colWidth)
            w.setMaximumWidth(self.colWidth)
        if self.rowHeight > 0:
            w.setFixedHeight(self.rowHeight)

        return w, selected

    def getWidget(self, position: int, w: T = None) -> T:
        if w is None:
            w = T()
        return w, False
