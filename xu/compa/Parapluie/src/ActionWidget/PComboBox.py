from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import QComboBox


class PComboBox(QComboBox):
    def __init__(self, scrollWidget=None, *args, **kwargs):
        super(PComboBox, self).__init__(*args, **kwargs)
        self.scrollWidget = scrollWidget
        self.setFocusPolicy(Qt.StrongFocus)

    def wheelEvent(self, *args, **kwargs):
        if self.hasFocus():
            return QComboBox.wheelEvent(self, *args, **kwargs)
        else:
            if self.scrollWidget:
                return self.scrollWidget.wheelEvent(*args, **kwargs)
