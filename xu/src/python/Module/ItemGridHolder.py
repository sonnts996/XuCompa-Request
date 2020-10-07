import textwrap

from PyQt5 import QtGui
from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QLabel, QVBoxLayout, QSizePolicy

from xu.compa.Parapluie import PWidget
from xu.compa.Parapluie.src import PFunction


class ItemGridHolder(PWidget):
    colors = ["#B86878", "#E57373", "#F0C0C8", "#F17657",
              "#FFB74D", "#FFCA28", "#6FCF97", "#66BB6A",
              "#4B894E", "#64B5F6", "#5C6BC0", "#386090",
              "#6E8CC8", "#9575CD", "#FFFFFF", "#242424"]

    def __init__(self):
        super().__init__()
        self.setStyleSheet("""QWidget{
                                background: white;
                                }
                                QWidget:hover{
                                background:#ece1dd;
                                }""")

        self.title = QLabel()
        self.title.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        self.title.setStyleSheet("""QLabel{
                                    border: none;
                                    color: #424242;
                                    background: transparent;
                                    font-weight: bold;
                                    font-size: 12px;
                                    }""")
        self.title.setWordWrap(True)
        self.title.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Expanding)

        layout = QVBoxLayout()
        layout.setAlignment(Qt.AlignTop | Qt.AlignLeft)
        layout.addWidget(self.title)
        self.setLayout(layout)
        PFunction.applyShadow(self)

        self.titleText = ""
        self.onItemClick = None

    def resizeEvent(self, a0: QtGui.QResizeEvent):
        self.title.setText(self.updateText(self.titleText).upper())

    def setTitle(self, title: str):
        self.titleText = title
        self.title.setText(title)

        if title != "":
            c = ord(title[0]) % 15
            self.setStyleSheet("""  QWidget{
                                background: %s;
                                }
                                QWidget:hover{
                                background:#ece1dd;
                                }""" % self.colors[c])
            self.title.setStyleSheet("""QLabel{
                                    border: none;
                                    color: %s;
                                    background: transparent;
                                    font-weight: bold;
                                    font-size: 12px;
                                    }""" % "#FFFFFF" if self.colors[c] != "#FFFFFF" else "#424242")

    def updateText(self, text):
        metrics = self.title.fontMetrics()
        if " " not in text:
            width = metrics.boundingRect("A").width()
            numChar = int(self.title.width() / width)
            if numChar <= 0:
                numChar = 1
            if len(text) > numChar:
                newText = textwrap.wrap(text, numChar)
                if len(newText) >= 3:
                    return "\n".join(newText[:3])
                else:
                    return "\n".join(newText)
            else:
                return text
        else:
            elidedText = metrics.elidedText(text, Qt.ElideRight, (self.title.width() - 40) * 3)
            return elidedText

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        super(ItemGridHolder, self).mousePressEvent(a0)
        if self.onItemClick is not None:
            self.onItemClick(self.titleText)

    def setOnItemClick(self, onItemClickFunc):
        self.onItemClick = onItemClickFunc
