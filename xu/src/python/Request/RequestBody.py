from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QVBoxLayout, QSplitter

from xu.compa.Parapluie import PWidget, Parapluie
from xu.src.python.Module.ParamEditor import TextEditWidget, EditorType, ParamEditor, ParamEditorConnect
from xu.src.python.Request.Model import BodyType


class RequestBody(PWidget):

    def __init__(self):
        super().__init__()
        self.setObjectName(Parapluie.Object_Raised)

        self.editor = TextEditWidget(save=False)

        self.paramEditor = ParamEditor()
        self.paramConnect = ParamEditorConnect(self.paramEditor, self.editor)
        self.editor.setEditorType(EditorType.Text)

        l3 = QSplitter()
        l3.setObjectName(Parapluie.Object_QSplitter)
        l3.setOrientation(Qt.Horizontal)
        l3.addWidget(self.editor)
        l3.addWidget(self.paramEditor)

        layout = QVBoxLayout()
        layout.addWidget(l3)
        self.setLayout(layout)
        self.layout().setContentsMargins(0, 8, 0, 0)

    def getData(self):
        self.editor.syncJson()
        if self.editor.editType == EditorType.JSON:
            return self.editor.text(), BodyType.JSON
        elif self.editor.editType == EditorType.XML:
            return self.jsonEditor.text(), BodyType.XML
        elif self.editor.editType == EditorType.HTML:
            return self.xmlText.text(), BodyType.HTML
        elif self.editor.editType == EditorType.Javascript:
            return self.xmlText.text(), BodyType.Javascript
        else:
            return self.editor.text(), BodyType.Text if self.editor.text() != "" or self.editor.text().isspace() else ""

    def setData(self, body, tpe):
        self.editor.setText(body)
        if tpe == BodyType.JSON:
            self.editor.setEditorType(EditorType.JSON)
        elif tpe == BodyType.XML:
            self.editor.setEditorType(EditorType.XML)
        elif tpe == BodyType.HTML:
            self.editor.setEditorType(EditorType.HTML)
        elif tpe == BodyType.Javascript:
            self.editor.setEditorType(EditorType.Javascript)
        else:
            self.editor.setEditorType(EditorType.JSON)
