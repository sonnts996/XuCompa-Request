from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSplitter

from xu.compa.Parapluie import Parapluie
from xu.src.python.Request import RequestNavigation, RequestWorkspace


class RequestViewer(QSplitter):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self, window):
        super().__init__()

        self.workspace = RequestWorkspace(window)
        self.workspace.alert.connect(lambda a, b, c, d: self.alert.emit(a, b, c, d))

        self.leftWidget = RequestNavigation()

        self.leftWidget.currentChange.connect(self.fileSelected)
        self.leftWidget.categoriesChange = self.workspace.setCategories
        self.leftWidget.alert.connect(lambda a, b: self.alert.emit(a, b, None, None))

        self.workspace.onSaveFunc = self.leftWidget.saveData

        self.addWidget(self.leftWidget)
        self.addWidget(self.workspace)

        self.setChildrenCollapsible(False)
        self.setStretchFactor(0, 1)
        self.setStretchFactor(1, 5)
        self.setObjectName(Parapluie.Object_QSplitter)

        self.leftWidget.newFile()
        self.workspace.setCategories(self.leftWidget.categories)

    def fileSelected(self):
        current = self.leftWidget.currentFile
        if current is not None:
            self.workspace.setVisible(True)
            self.workspace.setCurrentFile(current)
        else:
            self.workspace.setVisible(False)
