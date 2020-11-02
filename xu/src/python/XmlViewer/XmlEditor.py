from PyQt5 import Qsci
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QKeyEvent


class XMLEditor(Qsci.QsciScintilla):
    keyEvent = pyqtSignal(str)
    ARROW_MARKER_NUM = 8

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the default font
        font = QFont()
        font.setFamily('Courier')
        font.setFixedPitch(True)
        font.setPointSize(10)
        self.setFont(font)
        self.setMarginsFont(font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(font)
        self.setMarginsFont(font)
        self.setMarginWidth(0, fontmetrics.width("000") + 6)
        self.setMarginLineNumbers(0, True)
        self.setMarginsBackgroundColor(QColor("#E3F0FF"))

        # Brace matching: enable for a brace immediately before or after
        # the current position
        #
        self.setBraceMatching(QsciScintilla.SloppyBraceMatch)

        # Current line visible with special background color
        self.setCaretLineVisible(True)
        self.setCaretLineBackgroundColor(QColor("#A5ABBD"))

        # Set Python lexer
        # Set style for Python comments (style number 1) to a fixed-width
        # courier.
        #
        lexer = Qsci.QsciLexerXML(self)
        lexer.setDefaultFont(font)
        self.setLexer(lexer)
        # self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(300, 100)

    def keyPressEvent(self, *args, **kwargs):
        super(XMLEditor, self).keyPressEvent(*args, **kwargs)
        if len(args) > 0:
            if isinstance(args[0], QKeyEvent):
                event: QKeyEvent = args[0]
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    self.keyEvent.emit("ENTER")
                elif event.modifiers() == Qt.ControlModifier:
                    try:
                        self.keyEvent.emit(chr(event.key()))
                    except:
                        pass
                elif event.key() == Qt.Key_Less:
                    self.insert(">")
