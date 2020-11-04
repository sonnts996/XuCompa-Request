from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QSplitter, QWidget

from xu.compa.Parapluie import Parapluie
from xu.src.python.JsonViewer import JSONNavigation
from xu.src.python.Module.ParamEditor import EditorType
from xu.src.python.Module.ParamEditor.ParamEditor import ParamEditor
from xu.src.python.Module.ParamEditor.ParamEditorConnect import ParamEditorConnect
from xu.src.python.Module.ParamEditor.TextEditWidget import TextEditWidget


class JSONViewer(QSplitter):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self):
        super().__init__()

        self.leftWidget = JSONNavigation()
        self.leftWidget.currentChange.connect(self.fileSelected)
        self.leftWidget.alert.connect(lambda txt: self.alert.emit(txt, Parapluie.Alert_Error, None, None))
        self.addWidget(self.leftWidget)

        self.jsonEdit = TextEditWidget()
        self.jsonEdit.setObjectName(Parapluie.Object_Editor_Flat)
        self.jsonEdit.alert.connect(lambda txt, tpe, button1, button2: self.alert.emit(txt, tpe, button1, button2))
        self.jsonEdit.saveDataDone.connect(self.leftWidget.fileChanged)

        self.addWidget(self.jsonEdit)

        self.paramEdit = ParamEditor()
        self.paramEdit.setObjectName(Parapluie.Object_Table)
        self.paramEdit.error.connect(lambda s: self.alert.emit(s, Parapluie.Alert_Error, None, None))

        self.addWidget(self.paramEdit)

        self.paramConnect = ParamEditorConnect(self.paramEdit, self.jsonEdit)

        widget = QWidget()
        widget.setMaximumWidth(2)
        widget.setMinimumWidth(2)
        self.addWidget(widget)

        self.setChildrenCollapsible(False)

        self.leftWidget.newFile()
        self.jsonEdit.setEditorType(EditorType.JSON)

    def fileSelected(self):
        if self.leftWidget.currentFile is not None:
            self.paramEdit.setVisible(True)
            self.jsonEdit.setVisible(True)
            self.jsonEdit.setFile(self.leftWidget.currentFile)
        else:
            self.paramEdit.setVisible(False)
            self.jsonEdit.setVisible(False)
            self.paramEdit.setData(None)
            self.jsonEdit.setText("")
