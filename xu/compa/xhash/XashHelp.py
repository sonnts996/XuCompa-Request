import os

from xu.compa.xhash import Xash, XashList


def path2Xash(path):
    folder = os.path.dirname(path)
    data = os.path.basename(path)
    name, ext = os.path.splitext(data)
    return Xash(name, ext, folder)


def createXash(name: str, categoryId: str, tagList: dict, ext=""):
    text = categoryId + name

    tags = []
    for t in tagList:
        if isinstance(tagList[t], list):
            tag = t + "#".join(tagList[t])
        else:
            tag = t + "#" + tagList[t]
        tags.append(tag)

    tagg = "--".join(tags)
    if ext != "":
        return text + "--" + tagg + ext
    else:
        return text + "--" + tagg


def newXashId(category: str, xashList: XashList = None):
    if xashList is None:
        text = '[' + category + '#1]'
    else:
        lst = xashList.findWithCategory(category)
        if len(lst) > 0:
            text = "[%s#%s]" % (category, str(len(lst)))
        else:
            text = "[%s#%s]" % (category, '1')
    return text
