import logging

from PyQt5.QtWidgets import QApplication

from xu.compa.Parapluie import PResource
from xu.src.python.Window.MainWindow import MainWindow
from xu.src.res import Manage


def app(args):
    application = QApplication(args)
    PResource.initResource()
    Manage.initResource()
    window = MainWindow()
    window.showMaximized()
    try:
        a = application.exec_()
    except Exception as ex:
        a = -1
        logging.exception(ex)
    return a
