from PyQt5.QtWidgets import QWidget, QSplitter, QVBoxLayout

import xu.compa.parapluie as Parapluie
import xu.src.python.Module as Module
from xu.src.python.Module.ListView import ListView


class JSONViewer(QSplitter):
    def __init__(self):
        super().__init__()

        listView = ListView()

        leftLayout = QVBoxLayout()
        leftLayout.addWidget(listView)

        leftWidget = QWidget()
        Parapluie.Style.applyShadow(leftWidget)
        leftWidget.setObjectName(Parapluie.Object_Raised)
        leftWidget.setFixedWidth(300)
        leftWidget.setLayout(leftLayout)
        self.addWidget(leftWidget)

        self.jsonEdit = Module.JSONEditor()
        self.addWidget(self.jsonEdit)

        self.paramEdit = Module.ParamEditor()
        self.paramEdit.syncSignal.connect(self.onSync)
        self.addWidget(self.paramEdit)

        self.setChildrenCollapsible(False)

    def onSync(self, data):
        self.jsonEdit.setText(str(data).replace("'", '"'))
