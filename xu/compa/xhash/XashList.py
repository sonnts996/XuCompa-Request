import os

import xu.compa.xhash as xhash


class XashList:
    def __init__(self, listXash=None):
        if listXash is None:
            listXash = []

        self.list: list = listXash
        self.xdef = xhash.XashDef()

    def addXash(self, xha: xhash.Xash) -> int:
        if isinstance(xha, xhash.Xash):
            if xha not in self.list:
                self.list.append(xha)
                return self.list.index(xha)
            return self.list.index(xha)
        else:
            return -1

    def load(self, src_folder: str, filters: list = None):
        for root, dirs, files in os.walk(src_folder):
            for file in files:
                filename, file_extension = os.path.splitext(file)
                if file_extension == ".xdef":
                    self.xdef.addDef(os.path.join(root, file))
                else:
                    if filters is not None and file_extension in filters:
                        self.addXash(xhash.Xash(filename, file_extension, root))
                    elif filters is None:
                        self.addXash(xhash.Xash(filename, file_extension, root))

    # finding
    def findWithTags(self, *key: str, sensitive: bool = True) -> list:
        rs = []
        for x in self.list:
            if x.findWithTags(*key, sensitive=sensitive, xdef=self.xdef):
                rs.append(x)
        return rs

    def findWithName(self, name: str, sensitive: bool = True) -> list:
        rs = []
        for x in self.list:
            if x.findWithName(name, sensitive):
                rs.append(x)
        return rs

    def findEveryWhere(self, category: str, name: str, *tag: str, sensitive: bool = True) -> list:
        rs = []
        for x in self.list:
            c = False if category.isspace() or category == "" else x.findWithCategory(category, sensitive=sensitive)
            t = False if len(tag) <= 0 else x.findWithTags(*tag, sensitive=sensitive)
            n = False if name.isspace() or name == "" else x.findWithName(name, sensitive=sensitive)
            if c or n or t:
                rs.append(x)
        return rs

    def findMatchAll(self, category: str, name: str, *tag: str, sensitive: bool = True) -> list:
        rs = []
        for x in self.list:
            c = x.findWithCategory(category, sensitive=sensitive)
            t = x.findWithTags(*tag, sensitive=sensitive)
            n = x.findWithName(name, sensitive=sensitive)
            if c and n and t:
                rs.append(x)
        return rs

    def get(self, h: str):
        for x in self.list:
            if x == h:
                return x
        return None

    def findWithCategory(self, categories_name: str, file_id: str = None) -> list:
        rs = []
        for x in self.list:
            if x.findWithCategory(categories_name, file_id):
                rs.append(x)
        return rs

    def findWithId(self, categories: str) -> list:
        rs = []
        for x in self.list:
            if x.findWithId(categories):
                rs.append(x)
        return rs

    def extract(self, category_id: str, pro: str) -> list:
        x: xhash.Xash = self.xdef.get(category_id)
        if x is None:
            return []
        else:
            for i in x.tag:
                if i == pro:
                    return x.tag[i]

    def clear(self):
        self.list.clear()
        self.xdef.clear()
