from PyQt5 import QtGui
from PyQt5.QtCore import Qt, QEvent
from PyQt5.QtGui import QPainter
from PyQt5.QtWidgets import QStackedWidget, QLabel, QLineEdit, QStyleOption, QStyle


class PLabelEdit(QStackedWidget):
    def __init__(self, text: str = ""):
        super().__init__()
        self.editable = True
        self.label = QLabel()
        self.edit = QLineEdit()
        self.edit.installEventFilter(self)
        self.setText(text)

        self.addWidget(self.label)
        self.addWidget(self.edit)
        self.setCurrentIndex(0)

    def setText(self, text):
        self.label.setText(text)
        self.edit.setText(text)

    def setEditable(self, editable):
        self.editable = editable
        self.setCurrentIndex(0)

    def text(self):
        if self.currentIndex() == 0:
            return self.label.text()
        else:
            return self.edit.text()

    def mousePressEvent(self, a0: QtGui.QMouseEvent):
        if self.editable:
            if self.currentIndex() == 0:
                self.setCurrentIndex(1)
                self.setText(self.label.text())

    def eventFilter(self, a0: 'QObject', a1: 'QEvent'):
        if a1.type() == QEvent.KeyPress and a0 == self.edit:
            if self.editable:
                if a1.key() == Qt.Key_Enter or a1.key() == Qt.Key_Return:
                    if self.currentIndex() == 1:
                        self.setCurrentIndex(0)
                        self.setText(self.edit.text())
        return super(PLabelEdit, self).eventFilter(a0, a1)

    def paintEvent(self, a0: QtGui.QPaintEvent) -> None:
        opt = QStyleOption()
        opt.initFrom(self)
        painter = QPainter(self)
        self.style().drawPrimitive(QStyle.PE_Widget, opt, painter, self)
