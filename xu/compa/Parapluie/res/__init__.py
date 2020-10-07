import os
from enum import Enum

from PyQt5.QtGui import QIcon

from xu.compa.Parapluie.res import resources, resource2qrc


class DayNight(Enum):
    DayMode = 1
    NightMode = 0


def initResource():
    resources.qInitResources()


def runQrc(build=False):
    if build:
        resource2qrc.run(os.path.dirname(resource2qrc.__file__))
    else:
        resource2qrc.runWithoutBuildRes(os.path.dirname(resource2qrc.__file__))


def white(iconName: str) -> str:
    return ":/icons_white/" + iconName


def dark(iconName: str) -> str:
    return ":/icons/" + iconName


def invertIcon(iconName: str, mode: DayNight = DayNight.DayMode) -> QIcon:
    if mode:
        return QIcon(white(iconName))
    else:
        return QIcon(dark(iconName))


def defaultIcon(iconName: str, mode: DayNight = DayNight.DayMode) -> QIcon:
    if mode:
        return QIcon(dark(iconName))
    else:
        return QIcon(white(iconName))


def stylesheet(mode: DayNight = DayNight.DayMode) -> str:
    if mode:
        return ":/style/parapluie.css"
    else:
        return ":/style/parapluie.css"
