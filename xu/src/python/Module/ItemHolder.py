from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QSize
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QToolButton, QHBoxLayout, QSizePolicy

from xu.compa.Parapluie import PResource, Parapluie, PHolder, PWidget


class ItemHolder(PHolder):

    def __init__(self, parent: PWidget):
        super().__init__()
        self.setObjectName(Parapluie.Object_Item)
        self.parent = parent
        self.title = QLabel()
        self.category = QLabel()
        self.description = QLabel()

        self.closeButton = QToolButton()
        self.closeButton.setIconSize(QSize(12, 12))
        self.closeButton.setFixedSize(24, 24)
        self.closeButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Cancel_Svg))
        self.closeButton.pressed.connect(self.closeRequest)

        label = QLabel()

        icon = QIcon(":/icon/label.svg")
        pixmap = icon.pixmap(QSize(12, 12))
        label.setPixmap(pixmap)
        label.setFixedHeight(24)

        closeLayout = QHBoxLayout()
        closeLayout.setAlignment(Qt.AlignTop)
        closeLayout.addWidget(label, alignment=Qt.AlignLeft)
        closeLayout.addWidget(self.category, alignment=Qt.AlignLeft | Qt.AlignTop)
        closeLayout.addStretch()
        closeLayout.addWidget(self.closeButton, alignment=Qt.AlignRight)

        self.title.setWordWrap(True)
        self.title.setObjectName(Parapluie.Object_Item_Tittle)

        self.category.setVisible(False)
        self.category.setFixedHeight(20)
        self.category.setAlignment(Qt.AlignVCenter)
        self.category.setObjectName(Parapluie.Object_Item_Category)

        self.description.setVisible(False)
        self.description.setWordWrap(True)
        self.description.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
        self.description.setObjectName(Parapluie.Object_Item_Description)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        layout.addLayout(closeLayout)
        layout.addWidget(self.title)
        layout.addWidget(self.description)
        self.setLayout(layout)
        self.setMaximumHeight(100)

        self.onSelected = None
        self.data = None
        self.onClose = None
        self.desc = ""
        self.cate = ""
        self.ttl = ""

        self.parent.resized.connect(self.parentResized)

    def setText(self, title, category, description, selected):
        self.setTitle(title)
        self.setCategory(category)
        self.setDescription(description)
        self.setSelected(selected)

    def setTitle(self, title: str):
        self.ttl = title.upper()
        self.title.setText(self.updateText(self.ttl, self.title.width()))
        self.title.setToolTip(title)

    def setCategory(self, category: str):
        self.cate = category
        self.category.setText(self.updateText(self.cate, self.category.width()))
        self.category.setVisible(category != "")
        self.category.setToolTip(category)

    def setDescription(self, t):
        self.desc = t
        self.description.setText(self.updateText(self.desc, self.description.width()))
        self.description.setVisible(t != "")
        self.description.setToolTip(t)

    def setSelected(self, selected):
        self.setEnabled(not selected)
        self.closeButton.setVisible(not selected)

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

    def parentResized(self):
        self.description.setText(self.updateText(self.desc, self.parent.width()))
        self.category.setText(self.updateText(self.cate, self.parent.width()))
        self.title.setText(self.updateText(self.ttl, self.parent.width()))

    def updateText(self, text, width):
        if " " not in text:
            numChar = int(width / 10)
            if numChar <= 0:
                numChar = 1
            if len(text) > numChar:
                return text[:numChar] + ".."
            else:
                return text
        else:
            metrics = self.title.fontMetrics()
            elidedText = metrics.elidedText(text, Qt.ElideRight, width)
            return elidedText

    def itemSize(self):
        size = super(ItemHolder, self).itemSize()
        if size.height() <= 70:
            return size
        else:
            size.setHeight(70)
            return size
