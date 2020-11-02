import os

from PyQt5.QtWidgets import QListWidget

from xu.compa.Parapluie.src.ActionWidget import PWidget
from xu.compa.Parapluie.src.Adapter import PListAdapter
from xu.compa.xhash import XashList, XashHelp
from xu.src.python.Model import XFile
from xu.src.python.Model.ItemModel import ItemModel
from xu.src.python.Module import ItemHolder, ItemHeader
from xu.src.python.Utilities import Config


def inRequestFolder(path):
    return os.path.dirname(path) == Config.getRequestFolder()[0]


class ItemAdapter(PListAdapter):
    def __init__(self, parent: PWidget, layout: QListWidget, data, xashSrc, itemSelected, itemClose):
        super().__init__(layout)
        self.dataList = data
        self.itemSelected = itemSelected
        self.itemClose = itemClose
        self.parent = parent
        self.xashSrc: XashList = xashSrc

    def count(self) -> int:
        return len(self.dataList)

    def item(self, index: int):
        return self.dataList[index]

    def getWidget(self, position: int, w: ItemHolder = None):
        i: ItemModel = self.item(position)
        if isinstance(i.file, XFile):
            xash = XashHelp.path2Xash(i.file.getPath())

            w = ItemHolder(self.parent)
            w.setData(i.file)

            if inRequestFolder(i.file.getPath()):
                cate = xash.getCategory() if xash.getCategory() != "" else "<uncategorized>"
                descArr = xash.getTag("description")
                desc = ''
                for d in descArr:
                    if xash.isImportTag(d):
                        desc = d
                        break

                arr = self.xashSrc.extract(desc, "description")
                if arr is not None and len(arr) > 0:
                    desc = arr[0]
                else:
                    desc = ""
            else:
                cate = i.file.parent()
                desc = i.file.dir()

            w.setOnSelected(onSelected=self.itemSelected)
            w.setOnClose(onClose=self.itemClose)
            w.setText(xash.getName(), cate, desc, i.selected > 0)
        elif isinstance(i.file, str):
            w = ItemHeader()
            x: str = i.file
            w.setLabel(x)
        return w, i.selected, i.file
