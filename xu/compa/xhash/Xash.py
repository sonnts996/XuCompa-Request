import json
import os
import re

import xu.compa.xhash as xhash


class Xash:
    category_pattern = "\[.*?\]"
    import_pattern = "#\[.*?\]"

    def __init__(self, data: str = None, ext: str = None, folder: str = None):
        if data is not None:
            self.data: str = data
            if data.endswith("\n"):
                self.data = self.data[:len(data) - 1]
        else:
            self.data: str = ""

        self.folder = folder  # for matching when return
        self.ext = ext
        self.categories: XashCategory = None
        self.name = None
        self.tag = {}

        if not self.data.isspace():
            elem = self.data.split("--")
            if len(elem) > 1:
                name = elem[0]
                for i in range(1, len(elem)):
                    self._tag__(elem[i])
            elif len(elem) == 1:
                name = elem[0]
            else:
                name = ""
            self._name__(name)

    def _name__(self, name: str):
        brackets = re.findall(self.category_pattern, name)
        if len(brackets) >= 1:
            c = brackets[0]
            if name.startswith(c) or name.index(c) == 1:
                self.categories = XashCategory(c, True)
                self.name = name.replace("[" + self.categories.data + "]", "")
            else:
                self.categories = XashCategory("", True)
                self.name = name
        else:
            self.name = name

    def _tag__(self, pro: str):
        imp = re.findall(self.import_pattern, pro)
        temp = pro
        for i in imp:
            temp = temp.replace(i, "")
        lst = temp.split("#")
        for i in imp:
            lst.append(i)
        if len(lst) > 0:
            self.tag[lst[0]] = []
            if len(lst) > 1:
                for i in range(1, len(lst)):
                    self.tag[lst[0]].append(lst[i])

    def getPath(self):
        return os.path.join(self.folder, self.data + self.ext)

    def __str__(self):
        data = self.getObject()
        return json.dumps(data, ensure_ascii=False)

    def getObject(self):
        return {
            "data": {
                "name": self.data,
                "ext": self.ext,
                "folder": self.folder
            },
            "analysis": {
                "name": self.name,
                "category": self.categories.getObject() if self.categories is not None else None,
                "property": self.tag
            }
        }

    def findWithTag(self, pro: str, value, sensitive: bool = True, xdef: xhash.XashDef = None) -> bool:
        if pro == "" or value == "":
            return True

        rs = False
        if sensitive:
            for t in self.tag:
                if t.lower() == pro.lower():
                    for s in self.tag[t]:
                        if xdef is not None and re.search(self.category_pattern, s) is not None:
                            rs = rs or xdef.find(s, pro, value, True)
                        else:
                            rs = rs or value.lower() in s.lower()
        else:
            for t in self.tag:
                if t.lower() == pro.lower():
                    for s in self.tag[t]:
                        if xdef is not None and re.search(self.category_pattern, s) is not None:
                            rs = rs or xdef.find(s, pro, value, False)
                        else:
                            rs = rs or value.lower() == s.lower()
        return rs

    def findWithTags(self, *tags: str, sensitive: bool = True, xdef: xhash.XashDef = None):
        if len(tags) == 0 or "" in tags:
            return True

        rs = True
        for key in tags:
            k, v = key.split(XashCategory.sep)
            rs = rs and k is not None and v is not None and self.findWithTag(k, v, sensitive, xdef=xdef)
            if not rs:
                break
        return rs

    def findWithName(self, name: str, sensitive: bool = True) -> bool:
        if name == "":
            return True

        if sensitive:
            return name.lower() in self.name.lower()
        else:
            return name.lower() == self.name.lower()

    def __eq__(self, other):
        if isinstance(other, Xash):
            return other.getPath() == self.getPath()
        elif isinstance(other, str):
            return self.getPath() == other

    def findWithCategory(self, categories_name: str, file_id: str = None, sensitive: bool = True) -> bool:
        if categories_name == "":
            return True

        if sensitive:
            if file_id is None:
                return categories_name in self.categories.category if self.categories is not None else False
            else:
                return XashCategory.sep.join(
                    [categories_name, file_id]) == self.categories.data if self.categories is not None else False
        else:
            if file_id is None:
                return categories_name == self.categories.category if self.categories is not None else False
            else:
                return XashCategory.sep.join(
                    [categories_name, file_id]) == self.categories.data if self.categories is not None else False

    def findWithId(self, categories: str) -> bool:
        if categories == "":
            return True

        c = xhash.XashCategory(categories, False)
        return self.categories.data == c.data if self.categories is not None else False


class XashCategory:
    sep = "#"

    def __init__(self, category: str, owner: bool):
        self.data = category
        self.isOwner = owner

        if self.data.startswith("["):
            self.data = self.data[1:]
        elif self.data.startswith("#["):
            self.data = self.data[2:]
            self.isOwner = False
        if self.data.endswith("]"):
            self.data = self.data[:len(self.data) - 1]

        arr = self.data.split(self.sep)
        if len(arr) > 1:
            self.category = arr[0]
            self.id = "".join(arr[1:])
        elif len(arr) == 1:
            self.category = arr[0]
            self.id = ""
        else:
            self.category = ""
            self.id = ""

    def __str__(self):
        data = self.getObject()
        return json.dumps(data, ensure_ascii=False)

    def getObject(self):
        return {
            "category": self.category,
            "id": self.id,
            "owner": self.isOwner
        }
