from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

import xu.compa.parapluie as Parapluie


def style() -> str:
    return Parapluie.Resource.stylesheet()


def applyStyle(w: QWidget, stylePath: str = None):
    if stylePath is None:
        stylePath = style()
    Parapluie.Style.applyStyle(w, stylePath)


def windowTitle() -> str:
    return "Request - XuCompa"


def applyWindowTitle(w: QWidget, title: str = None):
    if title is None:
        w.setWindowTitle(windowTitle())
    else:
        w.setWindowTitle(title)


def windowIcon() -> str:
    return ":/window-icon/link.svg"


def applyWindowIcon(w: QWidget, icon: QIcon = None):
    if icon is None:
        w.setWindowIcon(QIcon(windowIcon()))
    else:
        w.setWindowIcon(icon)
