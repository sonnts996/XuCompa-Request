import copy
import json


class JIndex:
    def __init__(self, index: int, value=None):
        self.value = value
        self.index = index

    def __eq__(self, other):
        if isinstance(other, JIndex):
            return self.index == other.index
        elif isinstance(other, int):
            return other == self.index
        else:
            return False

    def __str__(self):
        if isinstance(self.value, JObject) or isinstance(self.value, JList):
            return self.value.__str__()
        else:
            if isinstance(self.value, (int, float, complex)):
                return str(self.value)
            else:
                return '"%s"' % str(self.value)

    def __inx__(self) -> int:
        return self.index

    def isEmpty(self):
        if self.isObject():
            return self.value.count() == 0
        return self.value == "" or self.value is None

    def isObject(self):
        return isinstance(self.value, JObject) or isinstance(self.value, JList)

    def getValueStr(self) -> str:
        return __valueStr__(self.value)


class JKey:
    def __init__(self, key: str, value=None):
        self.key = key
        self.value = value

    def __eq__(self, other):
        if isinstance(other, JKey):
            return other.key == self.key
        elif isinstance(other, str):
            return other == self.key
        else:
            return False

    def __str__(self):
        if isinstance(self.value, JObject) or isinstance(self.value, JList):
            return '"%s":%s' % (str(self.key), self.value.__str__())
        else:
            if isinstance(self.value, (int, float, complex)):
                return '"%s":%s' % (str(self.key), str(self.value))
            else:
                return '"%s":"%s"' % (str(self.key), str(self.value))

    def __inx__(self) -> str:
        return self.key

    def isEmpty(self):
        if self.isObject():
            return self.value.count() == 0
        return self.value == "" or self.value is None

    def isObject(self):
        return isinstance(self.value, JObject) or isinstance(self.value, JList)

    def getValueStr(self) -> str:
        return __valueStr__(self.value)


class JList:
    def __init__(self):
        self.__lst__ = []

    def count(self):
        return len(self.__lst__)

    def append(self, item: JIndex, index=-1):
        if index == -1:
            self.__lst__.append(item)
        else:
            self.__lst__.insert(index, item)

    def index(self, item):
        if item in self.__lst__:
            return self.__lst__.index(item)
        else:
            return -1

    def sort(self):
        self.__lst__.sort(key=JIndex.__inx__)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item < self.count():
                return self.__lst__[item]

    def __contains__(self, item):
        return self.__lst__.__contains__(item)

    def __iter__(self):
        self.__inx__ = 0
        return self

    def __next__(self):
        if self.__inx__ < len(self.__lst__):
            a = self.__lst__[self.__inx__]
            self.__inx__ += 1
            return a
        else:
            raise StopIteration

    def __str__(self):
        s = "["
        for data in self:
            if data is not None and isinstance(data, JObject):
                if self.index(data) != self.count() - 1:
                    s += data.__str__() + ","
                else:
                    s += data.__str__()
            else:
                if self.index(data) != self.count() - 1:
                    s += data.__str__() + ","
                else:
                    s += data.__str__()

        return s + "]"

    def remove(self, item: JIndex):
        self.__lst__.remove(item)


class JObject:
    def __init__(self):
        self.__root__ = []

    def addKey(self, key: JKey, index=-1):
        if key in self.__root__:
            i = self.__root__.index(key)
            self.__root__[i].value = key.value
        else:
            if index == -1:
                self.__root__.append(key)
            else:
                self.__root__.insert(index, key)

    def index(self, item):
        if item in self.__root__:
            return self.__root__.index(item)
        else:
            return -1

    def __contains__(self, item):
        return self.__root__.__contains__(item)

    def count(self):
        return len(self.__root__)

    def __iter__(self):
        self.__inx__ = 0
        return self

    def __next__(self):
        if self.__inx__ < len(self.__root__):
            a = self.__root__[self.__inx__]
            self.__inx__ += 1
            return a
        else:
            raise StopIteration

    def __str__(self):
        s = "{"
        for data in self:
            if data is not None:
                if data.key is not None:
                    if self.index(data) != self.count() - 1:
                        s += data.__str__() + ","
                    else:
                        s += data.__str__()
                else:
                    if self.index(data) == 0:
                        s += "["
                    if self.index(data) != self.count() - 1:
                        s += data.__str__() + ","
                    else:
                        s += data.__str__() + "]"
        return s + "}"

    def remove(self, item: JKey):
        self.__root__.remove(item)

    def __getitem__(self, item):
        if isinstance(item, int):
            if item < self.count():
                return self.__root__[item]

    def get(self, item):
        if item in self.__root__:
            return self.__root__[self.index(item)].value

    def getItem(self, item):
        if item in self.__root__:
            return self.__root__[self.index(item)]


def __valueStr__(value) -> str:
    if value is None:
        return '@null'
    elif isinstance(value, JObject) and value.count() == 0:
        return '@{}'
    elif isinstance(value, JList) and value.count() == 0:
        return '@[]'
    elif isinstance(value, str):
        if value == '@null' or value == "@[]" or value == '@{}' or value.isnumeric():
            return "'" + value
        else:
            return value
    else:
        return str(value)


def fromString(data):
    obj = json.loads(data)
    return fromObject(obj)


def fromObject(data):
    if isinstance(data, dict):
        root = JObject()
        __deep__(root, data)
    elif isinstance(data, list):
        root = JObject()
        key = JKey("JSON", JList())
        root.addKey(key)
        __deep__(key.value, data)
    else:
        root = JObject()
    return root


def toString(data: JObject):
    return data.__str__()


def toDict(data: JObject):
    if data.count() == 1 and data[0].key == 'JSON':
        dct = [] if isinstance(data[0].value, JList) else {}
        __deepDict__(dct, data[0].value)
    else:
        dct = {}
        __deepDict__(dct, data)
    return dct


def __deep__(parent, data):
    if isinstance(data, dict):  # obj
        for d in data:
            val = data[d]
            if isinstance(val, dict):  # key:obj -> obj
                child = JObject()
                key = JKey(d, child)
                __deep__(child, val)
                if isinstance(parent, JObject):
                    parent.addKey(key)
            elif isinstance(val, list):  # key:list -> obj
                child = JList()
                key = JKey(d, child)
                __deep__(child, val)
                if isinstance(parent, JObject):
                    parent.addKey(key)
            else:  # key:value -> obj
                if isinstance(parent, JObject):
                    key = JKey(d, val)
                    parent.addKey(key)
    elif isinstance(data, list):  # arr
        for val in data:
            if isinstance(val, dict):
                child = JObject()
                key = JIndex(data.index(val), child)
                __deep__(child, val)
                if isinstance(parent, JList):
                    parent.append(key)
            elif isinstance(val, list):
                child = JList()
                key = JIndex(data.index(val), child)
                __deep__(child, val)
                if isinstance(parent, JList):
                    parent.append(key)
            else:
                if isinstance(parent, JList):
                    key = JIndex(data.index(val), val)
                    parent.append(key)


def __deepDict__(parent, obj):
    if isinstance(obj, JObject) and isinstance(parent, dict):
        for data in obj:
            if isinstance(data.value, JObject):
                parent[data.key] = {}
                __deepDict__(parent[data.key], data.value)
            elif isinstance(data.value, JList):
                parent[data.key] = []
                __deepDict__(parent[data.key], data.value)
            else:
                parent[data.key] = data.value
    elif isinstance(obj, JList) and isinstance(parent, list):
        for data in obj:
            if isinstance(data.value, JObject):
                new = {}
                parent.append(new)
                __deepDict__(new, data.value)
            elif isinstance(data.value, JList):
                new = []
                parent.append(new)
                __deepDict__(new, data.value)
            else:
                parent.append(data.value)


def copyObject(obj):
    new = copy.deepcopy(obj)
    __deepCopy__(new)
    return new


def __deepCopy__(obj):
    if isinstance(obj, JObject) or isinstance(obj, JList):
        for data in obj:
            __deepCopy__(data)
    elif isinstance(obj, JKey) or isinstance(obj, JList):
        obj.value = ""


if __name__ == '__main__':
    test = {
        "firstName": "John",
        "lastName": "Smith",
        "gender": "man",
        "age": 32,
        "address": {
            "streetAddress": "21 2nd Street",
            "city": "New York",
            "state": "NY",
            "postalCode": "10021"
        },
        "phoneNumbers": [
            {"type": "home", "number": "212 555-1234"},
            {"type": "fax", "number": "646 555-4567"}
        ]
    }
    o = fromObject(test)
    n = toDict(o)
    print(o)
