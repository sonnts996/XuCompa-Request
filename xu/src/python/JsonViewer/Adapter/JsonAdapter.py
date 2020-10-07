from PyQt5.QtWidgets import QVBoxLayout

from xu.compa.Parapluie.src.Adapter import PListAdapter
from xu.src.python.JsonViewer.Model import JSONFile
from xu.src.python.Model.ItemModel import ItemModel
from xu.src.python.Module import ItemHolder, ItemHeader


class JsonAdapter(PListAdapter):
    def __init__(self, layout: QVBoxLayout, data, itemSelected, itemClose):
        super().__init__(layout)
        self.dataList = data
        self.itemSelected = itemSelected
        self.itemClose = itemClose

    def count(self) -> int:
        return len(self.dataList)

    def item(self, index: int):
        return self.dataList[index]

    def getWidget(self, position: int, w: ItemHolder = None):
        i: ItemModel = self.item(position)
        if isinstance(i.file, JSONFile):
            w = ItemHolder()
            x: JSONFile = i.file
            w.setData(x)
            w.setText(x.name()[0], x.parent(), x.path, i.selected > 0)
            w.setOnSelected(onSelected=self.itemSelected)
            w.setOnClose(onClose=self.itemClose)
        elif isinstance(i.file, str):
            w = ItemHeader()
            x: str = i.file
            w.setLabel(x)
        return w, i.selected, i.file
