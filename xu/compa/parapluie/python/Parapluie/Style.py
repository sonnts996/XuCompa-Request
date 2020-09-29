from PyQt5.QtCore import QFile, QTextStream
from PyQt5.QtGui import QColor
from PyQt5.QtWidgets import QWidget, QGraphicsDropShadowEffect


def applyStyle(w: QWidget, stylePath: str):
    file = QFile(stylePath)
    file.open(QFile.ReadOnly | QFile.Text)
    stream = QTextStream(file)
    style = stream.readAll()
    w.setStyleSheet(style)


def shadow() -> QGraphicsDropShadowEffect:
    s = QGraphicsDropShadowEffect()
    s.setBlurRadius(10)
    s.setXOffset(2)
    s.setYOffset(2)
    s.setColor(QColor(200, 200, 200))
    return s


def applyShadow(w: QWidget):
    w.setGraphicsEffect(shadow())
