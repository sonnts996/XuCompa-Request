import os

from xu.compa.xhash.XashList import XashList


def getListFile(src_folder: str, filters: list = None):
    lst = XashList()
    lst.load(src_folder, filters)
    a = lst.findWithTags("tag#apple")


if __name__ == '__main__':
    getListFile(os.path.join("..", "example"))
