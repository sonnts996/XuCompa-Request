from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QHBoxLayout, QSizePolicy

from xu.compa.Parapluie import Parapluie, PHolder, PWidget, PClose, PFunction


class ItemHolder(PHolder):
    colors = ["#B86878", "#E57373", "#F0C0C8", "#F17657",
              "#FFB74D", "#FFCA28", "#6FCF97", "#66BB6A",
              "#4B894E", "#64B5F6", "#5C6BC0", "#386090",
              "#6E8CC8", "#9575CD", "#FFFFFF", "#242424"]

    def __init__(self, parent: PWidget, special=False):
        super().__init__()
        self.setObjectName(Parapluie.Object_Item)
        self.special = special
        if special:
            PFunction.applyShadow(self)
        self.parent = parent
        self.title = QLabel()
        self.category = QLabel()
        self.description = QLabel()

        self.closeButton = PClose()
        self.closeButton.setFixedSize(24, 24)
        self.closeButton.pressed.connect(self.closeRequest)

        # label = QLabel()
        #
        # icon = QIcon(":/icon/label.svg")
        # pixmap = icon.pixmap(QSize(12, 12))
        # label.setPixmap(pixmap)
        # label.setFixedHeight(24)

        closeLayout = QHBoxLayout()
        closeLayout.setAlignment(Qt.AlignTop)
        # closeLayout.addWidget(label, alignment=Qt.AlignLeft)
        closeLayout.addWidget(self.category, alignment=Qt.AlignLeft)
        closeLayout.addStretch()
        closeLayout.addWidget(self.closeButton, alignment=Qt.AlignRight)

        self.title.setWordWrap(True)
        self.title.setObjectName(Parapluie.Object_Item_Tittle)
        self.title.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)

        self.category.setVisible(False)
        self.category.setFixedHeight(20)
        self.category.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.category.setAlignment(Qt.AlignVCenter | Qt.AlignLeft)
        self.category.setObjectName(Parapluie.Object_Item_Category)

        self.description.setVisible(False)
        self.description.setSizePolicy(QSizePolicy.Fixed, QSizePolicy.Fixed)
        self.description.setObjectName(Parapluie.Object_Item_Description)

        layout = QVBoxLayout()
        layout.setSpacing(2)
        layout.setAlignment(Qt.AlignTop)
        layout.addLayout(closeLayout, 1)
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
        self.parentResized()
        self.title.setToolTip(title)

    def setCategory(self, category: str):
        self.cate = category
        self.parentResized()
        self.category.setVisible(category != "")
        self.category.setToolTip(category)

        c = ord(category[0]) % 15
        self.category.setStyleSheet("""
        #Item #Category {
            border: none;
            background: %s;
            border-radius: 5px;
            color: #FFFFFF;
            font-weight: bold;
            font-size: 11px;
            padding-left: 5px;
            padding-right: 5px;
        }""" % self.colors[c])

    def setDescription(self, t):
        self.desc = t
        self.parentResized()
        self.description.setVisible(t != "")
        self.description.setToolTip(t)

    def setSelected(self, selected):
        self.setEnabled(not selected)
        if self.graphicsEffect() is not None:
            self.graphicsEffect().setEnabled(not selected)
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
        self.description.setText(self.updateText(self.desc, self.parent.width(), 7))
        self.category.setText(self.updateText(self.cate, self.parent.width(), 7))
        self.title.setText(self.updateText(self.ttl, self.parent.width(), 10))

        self.setFixedWidth(self.parent.width() - (23 if self.special else 15))

    def updateText(self, text, width, unit):
        if " " not in text:
            numChar = int(width / unit)
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
