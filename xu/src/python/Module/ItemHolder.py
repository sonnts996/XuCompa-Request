from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QToolButton, QHBoxLayout, QSizePolicy

from xu.compa.Parapluie import PResource, Parapluie, PHolder


class ItemHolder(PHolder):

    def __init__(self):
        super().__init__()
        self.setObjectName(Parapluie.Object_Item)

        self.title = QLabel()
        self.category = QLabel()
        self.description = QLabel()

        close = QToolButton()
        close.setIconSize(QSize(12, 12))
        close.setFixedSize(24, 24)
        close.setIcon(PResource.defaultIcon(Parapluie.Icon_Cancel_Svg))
        close.pressed.connect(self.closeRequest)

        closeLayout = QHBoxLayout()
        closeLayout.addWidget(self.category, alignment=Qt.AlignLeft)
        closeLayout.addWidget(close, alignment=Qt.AlignRight)

        self.title.setWordWrap(True)
        self.title.setObjectName(Parapluie.Object_Item_Tittle)

        self.category.setVisible(False)
        self.category.setObjectName(Parapluie.Object_Item_Category)

        self.description.setVisible(False)
        self.description.setWordWrap(True)
        self.description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.description.setObjectName(Parapluie.Object_Item_Description)
        self.description.setMaximumWidth(290)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop)
        layout.addLayout(closeLayout)
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        self.setLayout(layout)
        self.setMaximumWidth(290)
        self.setMaximumHeight(100)

        self.onSelected = None
        self.data = None
        self.onClose = None
        self.desc = ""

    def setText(self, title, category, description, selected):
        self.setTitle(title)
        self.setCategory(category)
        self.setDescription(description)
        self.setSelected(selected)

    def setTitle(self, title: str):
        self.title.setText(title.upper())

    def setCategory(self, category: str):
        self.category.setText(category)
        self.category.setVisible(category != "")

    def setDescription(self, t):
        self.desc = t
        self.description.setText(self.updateText(self.desc))
        self.description.setVisible(t != "")

    def setSelected(self, selected):
        self.setEnabled(not selected)
        if selected:
            self.setStyleSheet("""QLabel{color:white}""")
        else:
            self.setStyleSheet("")

    def setData(self, data):
        self.data = data

    def mouseDoubleClickEvent(self, a0: QtGui.QMouseEvent):
        if self.onSelected is not None:
            self.onSelected(self.data)

    def setOnSelected(self, onSelected):
        self.onSelected = onSelected

    def closeRequest(self):
        if self.onClose is not None:
            self.onClose(self.data)

    def setOnClose(self, onClose):
        self.onClose = onClose

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.description.setText(self.updateText(self.desc))

    def updateText(self, text):
        metrics = self.title.fontMetrics()
        elidedText = metrics.elidedText(text, Qt.ElideRight, (self.description.width()) * 2)
        return elidedText

    def itemSize(self):
        size = super(ItemHolder, self).itemSize()
        if size.height() <= 100:
            return size
        else:
            size.setHeight(100)
            return size
