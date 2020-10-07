from PyQt5.QtWidgets import QVBoxLayout

from xu.compa.Parapluie.src.Adapter import PListAdapter
from xu.compa.xhash import Xash
from xu.src.python.Model.ItemModel import ItemModel
from xu.src.python.Module import ItemHolder


class ItemAdapter:
    def __init__(self, layout: QVBoxLayout, data):
        super().__init__(layout)
        self.dataList = data

    def count(self) -> int:
        return len(self.dataList)

    def item(self, index: int):
        return self.dataList[index]

    def getWidget(self, position: int, w: ItemHolder = None):
        if w is None:
            w = ItemHolder()

        i: ItemModel = self.item(position)
        x: Xash = i.file
        w.setTitle(x.name)
        w.setCategory(x.categories.category if x.categories is not None else "<empty>")
        if "description" in x.tag:
            arr = x.tag["description"]
            if len(arr) > 0:
                w.setDescription(arr[0])

        return w, i.selected, i.file
