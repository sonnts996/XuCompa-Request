import os
import platform

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


def getUserFolder():
    return os.path.expanduser('~')


def linux_mkdir(folder, path, name):
    plt = platform.system()
    if plt == "Windows":
        if not os.path.exists(path):
            os.makedirs(path)
    elif plt == "Linux":
        if not os.path.exists(path):
            try:
                os.makedirs(path)
            except PermissionError as pe:
                print(pe)
                current = os.getcwd()
                os.chdir(folder)
                os.makedirs(name, 0o777)
                os.chdir(current)
    elif plt == "Darwin":
        print("Your system is MacOS")
        # do x y z
    else:
        print("Unidentified system")
