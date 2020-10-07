import os


class JSONFile:
    def __init__(self, path: str = ""):
        self.path = path
        self.unsavedData = ""

    def setPath(self, path):
        self.path = path

    def name(self):
        return os.path.splitext(os.path.basename(self.path))

    def parent(self):
        return os.path.basename(os.path.dirname(self.path))

    def dir(self):
        return os.path.dirname(self.path)

    def __eq__(self, other):
        if isinstance(other, JSONFile):
            return other.path == self.path
        return False
