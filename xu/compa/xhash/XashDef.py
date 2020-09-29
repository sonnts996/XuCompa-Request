import os

import xu.compa.xhash as xhash


class XashDef:
    def __init__(self):
        self.defFile = []
        self.listDef = {}

    def addDef(self, file: str):
        filename, file_extension = os.path.splitext(file)
        if file_extension == ".xdef":
            self.defFile.append(file)
            self.listDef[file] = []
            lst = self.readDef(file)
            for d in lst:
                self.listDef[file].append(d)
            return 0
        else:
            return -1

    def readDef(self, file: str):
        rs = []
        file1 = open(os.path.join(file), 'r', encoding='utf-8', errors='ignore')
        Lines = file1.readlines()
        for line in Lines:
            rs.append(xhash.Xash(line))
        return rs

    def get(self, categories_id):
        for x in self.listDef:
            for a in self.listDef[x]:
                if a.findWithId(categories_id):
                    return a
        return None

    def find(self, categories_id: str, pro: str, value: str, sensity: bool = True) -> bool:
        x: xhash.Xash = self.get(categories_id)
        if x is None:
            return False

        rs = False
        for t in x.tag:
            if sensity:
                if t.lower() == pro.lower():
                    rs = rs or value.lower() in map(str.lower, x.tag[t])
            else:
                if t == pro:
                    rs = rs or value in x.tag
        return rs
