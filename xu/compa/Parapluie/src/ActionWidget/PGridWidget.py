from PyQt5 import QtGui
from PyQt5.QtWidgets import QGridLayout

from xu.compa.Parapluie.src.ActionWidget import PWidget
from xu.compa.Parapluie.src.Adapter import PGridAdapter


class PGridWidget(PWidget):
    def __init__(self, numCol=1):
        super().__init__()
        self.layout = QGridLayout()
        self.numCol = numCol
        self.rowHeight: int = -1
        self.colWidth: int = -1
        self.fixColumn: bool = False
        self.adapter: PGridAdapter = None
        self.vSpacing = 0

        self.setLayout(self.layout)

    def setHorizontalSpacing(self, space):
        if space >= 0:
            self.vSpacing = space
        else:
            self.vSpacing = 0
        self.layout.setHorizontalSpacing(self.vSpacing)

    def setVerticalSpacing(self, space):
        self.layout.setVerticalSpacing(space)

    def setAlignment(self, alignment):
        self.layout.setAlignment(alignment)

    def setNumberColumn(self, numCol: int):
        if numCol >= 1:
            self.numCol = numCol
        else:
            self.numCol = 1

    def setFixColumn(self, fixColumn: bool):
        self.fixColumn = fixColumn
        self.refresh()

    def setRowHeight(self, rowHeight: int):
        self.rowHeight = rowHeight
        self.refresh()

    def setAdapter(self, adapter: PGridAdapter):
        self.adapter = adapter
        self.adapter.setLayout(self.layout)
        self.refresh()

    def getColumnWidth(self) -> int:
        if self.fixColumn:
            if self.adapter is not None:
                mr1, _, mr2, _ = self.getContentsMargins()
                return int(((self.width() - mr1 - mr2) - ((self.numCol + 3) * self.vSpacing)) / self.numCol)
            else:
                return -1
        else:
            return -1

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.refresh()
        super(PGridWidget, self).resizeEvent(a0)

    def refresh(self):
        if self.adapter is not None:
            self.adapter.setNumCol(self.numCol)
            self.adapter.setRowHeight(self.rowHeight)
            self.adapter.setColumnWidth(self.getColumnWidth())
            self.adapter.refresh()
