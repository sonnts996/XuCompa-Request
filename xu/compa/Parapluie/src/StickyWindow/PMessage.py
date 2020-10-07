from PyQt5.QtCore import QRect, Qt
from PyQt5.QtWidgets import QWidget, QVBoxLayout, QPushButton, QHBoxLayout, QLabel, QSizePolicy

import xu.compa.Parapluie as Parapluie
from xu.compa.Parapluie.src.StickyWindow.PSticky import PSticky


class PMessage(PSticky):
    def __init__(self, parent: QWidget):
        super().__init__(parent)

        x = parent.x() + parent.width() / 2 - 150
        y = parent.y() + parent.height() / 2 - 50
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
        self.setCentralWidget(widget)

    def addButton(self, text, tpe, action=None):
        apply = QPushButton()
        apply.setText(text)
        if action:
            apply.clicked.connect(action)

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
        self.addButton("CLOSE", Parapluie.Button_Neutral, lambda: self.completeDestroy(0))
        for o in option:
            if isinstance(o, str):
                self.addButton(o, Parapluie.Button_Positive, lambda: self.completeDestroy(option.index(o)))
            elif isinstance(o, dict):
                if "text" in o and "type" in o:
                    self.addButton(o["text"], o["type"], lambda: self.completeDestroy(option.index(o)))

        self.setSizePolicy(QSizePolicy.Expanding, QSizePolicy.Fixed)
