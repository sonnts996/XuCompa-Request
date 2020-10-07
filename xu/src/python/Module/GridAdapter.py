from xu.compa.Parapluie.src.Adapter import PGridAdapter
from xu.src.python.Module import ItemGridHolder


class GridAdapter(PGridAdapter[ItemGridHolder]):

    def __init__(self, data):
        super().__init__()
        self.dataList = data
        self.itemClicked = None

    def count(self) -> int:
        return len(self.dataList)

    def item(self, index: int):
        return self.dataList[index]

    def getWidget(self, position: int, w: ItemGridHolder = None):
        if w is None:
            w = ItemGridHolder()

        s = self.item(position)
        w.setTitle(s)
        w.setOnItemClick(self.onItemClicked)

        return w, False

    def onItemClicked(self, txt):
        if self.itemClicked is not None:
            self.itemClicked(txt)

    def setOnItemClick(self, onItemClickedFunc):
        self.itemClicked = onItemClickedFunc
