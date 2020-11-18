from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy

from xu.compa.Parapluie import Parapluie
from xu.compa.Parapluie.src.StickyWindow.PSticky import PSticky


class PMessage(PSticky):
    def __init__(self, parent: QWidget, rect: QRect = None):
        super().__init__(parent)

        if rect is None:
            x = parent.x() + parent.width() / 2 - 150
            y = parent.y() + parent.height() / 2 - 50
            window_rect = QRect(x, y, 300, 100)
        else:
            x = rect.x() + rect.width() / 2 - 150
            y = rect.y() + rect.height() / 2 - 100
            window_rect = QRect(x, y, 300, 100)
        self.setGeometry(window_rect)

        self.action = QHBoxLayout()
        self.action.addStretch()
        self.action.addStretch()

        self.text = QLabel()
        self.text.setWordWrap(True)
        self.text.setStyleSheet("color:#666666;")

        layout = QVBoxLayout()
        layout.setSpacing(18)
        layout.addWidget(self.text, alignment=Qt.AlignTop)
        layout.addLayout(self.action)
        layout.setContentsMargins(12, 12, 12, 0)

        widget = QWidget()
        widget.setLayout(layout)
        widget.setContentsMargins(0, 8, 0, 0)
        widget.setObjectName(Parapluie.Object_Raised_Off)
        self.setCentralWidget(widget)

    def addButton(self, text, tpe, action=None, data=None):
        apply = QPushButton()
        apply.setText(text)
        if action:
            if data is None:
                apply.clicked.connect(action)
            else:
                apply.clicked.connect(lambda: action(text, data))

        if tpe == Parapluie.Button_Positive:
            apply.setObjectName(Parapluie.Object_OptimizeButton)
        elif tpe == Parapluie.Button_Negative:
            apply.setObjectName(Parapluie.Object_NegativeButton)

        self.action.insertWidget(1, apply, alignment=Qt.AlignCenter)

    def setMessage(self, message):
        self.text.setText(message)

    def initInformation(self, message, title="Notice"):
        self.setWindowTitle(title.upper())
        self.setMessage(message)
        self.addButton("CLOSE", Parapluie.Button_Neutral, lambda: self.completeDestroy(0))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initWarning(self, message, title="Warning!!!", negative="CONTINUE"):
        self.setWindowTitle(title.upper())
        self.setMessage(message)
        self.addButton("CLOSE", Parapluie.Button_Neutral, lambda: self.completeDestroy(0))
        self.addButton(negative, Parapluie.Button_Negative, lambda: self.completeDestroy(1))
        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def initQuestion(self, message, option: list, title="Choose a option..."):
        self.setWindowTitle(title.upper())
        self.setMessage(message)
        for o in option:
            if isinstance(o, str):
                self.addButton(o, Parapluie.Button_Positive, self.onSelectedOption, option.index(o))
            elif isinstance(o, dict):
                if "text" in o and "type" in o:
                    self.addButton(o["text"], o["type"], self.onSelectedOption,  option.index(o))

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)

    def onSelectedOption(self, text, data):
        self.completeDestroy(data)
