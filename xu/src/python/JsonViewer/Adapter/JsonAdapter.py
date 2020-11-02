from PyQt5.QtWidgets import QListWidget

from xu.compa.Parapluie.src.ActionWidget import PWidget
from xu.compa.Parapluie.src.Adapter import PListAdapter
from xu.src.python.Model import ItemModel, XFile
from xu.src.python.Module import ItemHolder, ItemHeader


class JsonAdapter(PListAdapter):
    def __init__(self, parent: PWidget, layout: QListWidget, data, itemSelected, itemClose):
        super().__init__(layout)
        self.dataList = data
        self.itemSelected = itemSelected
        self.itemClose = itemClose
        self.parent = parent

    def count(self) -> int:
        return len(self.dataList)

    def item(self, index: int):
        return self.dataList[index]

    def getWidget(self, position: int, w: ItemHolder = None):
        i: ItemModel = self.item(position)
        if isinstance(i.file, XFile):
            w = ItemHolder(self.parent)
            x: XFile = i.file
            w.setData(x)
            w.setText(x.name()[0], x.parent(), x.getPath(), i.selected > 0)
            w.setOnSelected(onSelected=self.itemSelected)
            w.setOnClose(onClose=self.itemClose)
        elif isinstance(i.file, str):
            w = ItemHeader()
            x: str = i.file
            w.setLabel(x)
        return w, i.selected, i.file
