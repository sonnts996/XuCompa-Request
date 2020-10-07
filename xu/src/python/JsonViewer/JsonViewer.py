from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSplitter

from xu.src.python.JsonViewer import JSONNavigation, JSONWidget, ParamEditor


class JSONViewer(QSplitter):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self):
        super().__init__()

        self.leftWidget = JSONNavigation()
        self.leftWidget.currentChange.connect(self.fileSelected)
        self.addWidget(self.leftWidget)

        self.jsonEdit = JSONWidget()
        self.jsonEdit.alert.connect(lambda txt, tpe, button1, button2: self.alert.emit(txt, tpe, button1, button2))
        self.jsonEdit.syncRequest.connect(self.editSignal)

        self.addWidget(self.jsonEdit)

        self.paramEdit = ParamEditor()
        self.paramEdit.syncRequest.connect(self.tableSignal)
        self.addWidget(self.paramEdit)

        self.setChildrenCollapsible(False)

        self.leftWidget.newFile()

    def tableSignal(self, data):
        self.jsonEdit.setData(data)

    def editSignal(self, data):
        self.paramEdit.setData(data)

    def fileSelected(self):
        if self.leftWidget.currentFile is not None:
            self.paramEdit.setVisible(True)
            self.jsonEdit.setVisible(True)
            self.jsonEdit.setFile(self.leftWidget.currentFile)
        else:
            self.paramEdit.setVisible(False)
            self.jsonEdit.setVisible(False)
            self.paramEdit.setData({})
            self.jsonEdit.setText("")
