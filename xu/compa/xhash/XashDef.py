import os
import re

import xu.compa.xhash as xhash


def isDef(key: str) -> bool:
    import_pattern = "#\[.*?\]"
    return re.search(import_pattern, key) is not None


class XashDef:
    def __init__(self):
        self.defFile = []
        self.listDef = {}

    def addDef(self, file: str):
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".xdef":
            lst = self.readDef(file)
            if lst is not None:
                self.defFile.append(file)
                self.listDef[file] = []
                for d in lst:
                    self.listDef[file].append(d)
                return 0
            return -2
        else:
            return -1

    def readDef(self, file: str):
        try:
            rs = []
            file1 = open(os.path.join(file), 'r', encoding='utf-8', errors='ignore')
            Lines = file1.readlines()
            for line in Lines:
                rs.append(xhash.Xash(line))
            return rs
        except:
            return None

    def get(self, categories_id):
        for x in self.listDef:
            for a in self.listDef[x]:
                if a.findWithId(categories_id):
                    return a
        return None

    def find(self, categories_id: str, pro: str, value: str, sensitive: bool = True) -> bool:
        x: xhash.Xash = self.get(categories_id)
        if x is None:
            return False

        rs = False
        for t in x.tag:
            if sensitive:
                if t.lower() == pro.lower():
                    for i in x.tag[t]:
                        rs = rs or value.lower() in i.lower()
            else:
                if t.lower() == pro.lower():
                    rs = rs or value.lower() in map(str.lower, x.tag[t])
        return rs

    @classmethod
    def isDef(cls, a) -> bool:
        return isDef(a)

    def clear(self):
        self.defFile.clear()
        self.listDef.clear()
