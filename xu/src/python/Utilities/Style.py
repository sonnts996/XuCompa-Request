from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QWidget

from xu.compa.Parapluie import PResource, PFunction


def style() -> str:
    return PResource.stylesheet()


def applyStyle(w: QWidget, stylePath: str = None):
    if stylePath is None:
        stylePath = style()
    PFunction.applyStyle(w, stylePath)


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
