from xu.src.python.Module.ParamEditor.ParamEditor import ParamEditor, ParamType
from xu.src.python.Module.ParamEditor.TextEditWidget import TextEditWidget, EditorType


class ParamEditorConnect:
    def __init__(self, table: ParamEditor, editors: TextEditWidget):
        self.table = table
        self.editors = editors
        self.table.syncRequest.connect(self.tableSignal)
        self.editors.syncRequest.connect(self.editorSignal)
        self.editors.editorTypeChanged.connect(self.editorTypeSignal)

    def tableSignal(self):
        self.editors.setData(self.table.getData())

    def editorSignal(self, data):
        tpe = self.editors.editType
        if tpe == EditorType.JSON:
            if self.table.paramType != ParamType.JSON or self.table.paramType != ParamType.Param:
                self.table.setParamType(ParamType.JSON)
            self.table.setData(data)
            self.table.refresh()
        elif tpe == EditorType.XML:
            if self.table.paramType != ParamType.XML:
                self.table.setParamType(ParamType.XML)
            self.table.setData(data)
            self.table.refresh()

    def editorTypeSignal(self):
        tpe = self.editors.editType
        if tpe == EditorType.JSON:
            if self.table.paramType != ParamType.JSON or self.table.paramType != ParamType.Param:
                self.table.setParamType(ParamType.JSON)
                self.table.refresh()
            self.table.setData(self.editors.getData())
            self.table.refresh()
            self.table.setVisible(True)
        elif tpe == EditorType.XML:
            if self.table.paramType != ParamType.XML:
                self.table.setParamType(ParamType.XML)
                self.table.refresh()
            self.table.setData(self.editors.getData())
            self.table.refresh()
            self.table.setVisible(True)
        else:
            self.table.setVisible(False)
