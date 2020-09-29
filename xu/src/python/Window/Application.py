from PyQt5.QtWidgets import QApplication

import xu.compa.parapluie as Parapluie
from xu.src.python.Window.MainWindow import MainWindow
from xu.src.res import Manage


def app(args):
    application = QApplication(args)
    Parapluie.Resource.initResource()
    Manage.initResource()
    window = MainWindow()
    window.showMaximized()
    return application.exec_()
