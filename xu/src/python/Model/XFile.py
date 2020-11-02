import os


class XFile:
    def __init__(self, path):
        self.path = path
        self.unsavedData = ""

    def getPath(self):
        return self.path

    def setPath(self, path):
        self.path = path

    def name(self):
        return os.path.splitext(os.path.basename(self.path))

    def parent(self):
        return os.path.basename(os.path.dirname(self.path))

    def dir(self):
        return os.path.dirname(self.path)

    def __eq__(self, other):
        if isinstance(other, XFile):
            return other.path == self.path
        elif isinstance(other, str):
            return other == self.path
        return False
