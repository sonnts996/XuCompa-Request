from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QListView, QLabel, QSizePolicy

from xu.compa.Parapluie import Parapluie


def listView():
    return QListView()


def formLabel(label: str, center=True):
    name = QLabel(label)
    name.setFixedWidth(100)
    if center:
        name.setObjectName(Parapluie.Object_FormLabel)
        name.setAlignment(Qt.AlignLeft | Qt.AlignVCenter)
    else:
        name.setObjectName(Parapluie.Object_FormLabel)
        name.setAlignment(Qt.AlignLeft | Qt.AlignTop)
    name.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)
    return name
