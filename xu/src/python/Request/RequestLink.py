import json
import logging

from PyQt5.QtCore import Qt, QRect, pyqtSignal
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout

from xu.compa.Parapluie import PSticky, Parapluie
from xu.src.python import Utilities
from xu.src.python.Module.ParamEditor import ParamEditor, ParamType, Formatter, EditorType
from xu.src.python.Utilities import Config


class RequestLink(PSticky):
    alert = pyqtSignal(str, str, object, object)

    def __init__(self, parent: QWidget, rect: QRect = None):
        super().__init__(parent)

        if rect is None:
            x = parent.x() + parent.width() / 2 - 200
            y = parent.y() + parent.height() / 2 - 150
            window_rect = QRect(x, y, 400, 300)
        else:
            x = rect.x() + rect.width() / 2 - 200
            y = rect.y() + rect.height() / 2 - 150
            window_rect = QRect(x, y, 400, 300)
        self.setGeometry(window_rect)

        self.tableLink = ParamEditor(ParamType.Table)
        self.tableLink.setHeaderData([
            {
                'key': 'name',
                'name': 'NAME',
                'editable': True,
                'data-type': str.__class__
            },
            {
                'key': 'url',
                'name': 'LINK',
                'editable': True,
                'data-type': str.__class__
            }
        ])

        self.closeButton = QPushButton("Close")
        self.closeButton.pressed.connect(lambda: self.completeDestroy(0))
        self.saveButton = QPushButton("Save")
        self.saveButton.setObjectName(Parapluie.Object_OptimizeButton)
        self.saveButton.pressed.connect(self.save)

        bottomLayout = QHBoxLayout()
        bottomLayout.setContentsMargins(0, 4, 0, 0)
        bottomLayout.setAlignment(Qt.AlignRight)
        bottomLayout.addWidget(self.closeButton)
        bottomLayout.addWidget(self.saveButton)

        layout = QVBoxLayout()
        layout.setContentsMargins(10, 10, 10, 0)
        layout.addWidget(self.tableLink)
        layout.addLayout(bottomLayout)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setObjectName(Parapluie.Object_Raised_Off)
        self.setCentralWidget(widget)
        self.setWindowTitle("API Link define")
        Utilities.Style.applyWindowIcon(self)

        self.listLink = []
        self.loadData()

    def loadData(self):
        self.getData()
        self.tableLink.setData(self.listLink)
        self.tableLink.refresh()

    def getData(self):
        try:
            path = Config.getAPILinkFile()
            file = open(path, 'r', encoding='utf-8')
            data = file.read()
            file.close()
            self.listLink = json.loads(data)
        except Exception as ex:
            logging.exception(ex)
            self.alert.emit(str(ex))

    def save(self):
        self.listLink = self.tableLink.getData()
        try:
            path = Config.getAPILinkFile()
            file = open(path, 'w', encoding='utf-8')
            file.write(Formatter.dumps(self.listLink, EditorType.JSON, None))
            file.close()
            self.completeDestroy(1)
        except Exception as ex:
            logging.exception(ex)
            self.alert.emit(str(ex))
