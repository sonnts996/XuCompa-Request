from PyQt5.QtWidgets import QLabel, QVBoxLayout

from xu.compa.Parapluie import Parapluie
from xu.compa.Parapluie.src.ActionWidget import PHolder


class ItemHeader(PHolder):
    def __init__(self, objName= Parapluie.Object_ItemHeader):
        super().__init__()
        self.label = QLabel()
        self.setObjectName(objName)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

    def setLabel(self, text: str):
        self.label.setText(text.upper())
