import logging

from PyQt5 import Qsci
from PyQt5.Qsci import QsciScintilla
from PyQt5.QtCore import pyqtSignal, Qt
from PyQt5.QtGui import QColor, QFont, QFontMetrics, QKeyEvent




class TextEditor(Qsci.QsciScintilla):
    keyEvent = pyqtSignal(str)
    ARROW_MARKER_NUM = 8
    lexerType = ''

    def __init__(self, parent=None):
        super().__init__(parent)

        # Set the default font
        self.font = QFont()
        self.font.setFamily('Courier')
        self.font.setFixedPitch(True)
        self.font.setPointSize(10)
        self.setFont(self.font)
        self.setMarginsFont(self.font)

        # Margin 0 is used for line numbers
        fontmetrics = QFontMetrics(self.font)
        self.setMarginsFont(self.font)
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
        lexer = Qsci.QsciLexerMarkdown(self)
        lexer.setDefaultFont(self.font)
        self.setLexer(lexer)
        # self.SendScintilla(QsciScintilla.SCI_STYLESETFONT, 1, 'Courier')

        """
        Customization - AUTOCOMPLETION (Partially usable without a lexer)
        """
        # Set the autocompletions to case INsensitive
        self.setAutoCompletionCaseSensitivity(False)
        # Set the autocompletion to not replace the word to the right of the cursor
        self.setAutoCompletionReplaceWord(False)
        # Set the autocompletion source to be the words in the
        # document
        self.setAutoCompletionSource(Qsci.QsciScintilla.AcsDocument)
        # Set the autocompletion dialog to appear as soon as 1 character is typed
        self.setAutoCompletionThreshold(1)

        # Don't want to see the horizontal scrollbar at all
        # Use raw message to Scintilla here (all messages are documented
        # here: http://www.scintilla.org/ScintillaDoc.html)
        # self.SendScintilla(QsciScintilla.SCI_SETHSCROLLBAR, 0)

        # not too small
        self.setMinimumSize(300, 100)

    def changeLexer(self, lexer, tpe=''):
        self.lexerType = tpe
        lexer.setDefaultFont(self.font)
        self.setLexer(lexer)

    def keyPressEvent(self, *args, **kwargs):
        super(TextEditor, self).keyPressEvent(*args, **kwargs)
        if len(args) > 0:
            if isinstance(args[0], QKeyEvent):
                event: QKeyEvent = args[0]
                if event.key() == Qt.Key_Return or event.key() == Qt.Key_Enter:
                    self.keyEvent.emit("ENTER")
                elif event.modifiers() == Qt.ControlModifier:
                    try:
                        self.keyEvent.emit(chr(event.key()))
                    except Exception as ex:
                        logging.exception(ex)
                else:
                    t = autoKey(self.lexerType, event.text())
                    if t:
                        self.insert(t)


keyList = {
    'JSON': {
        '{': '}',
        '[': ']',
    },
    'XML': {
        '<': '>'
    },
    'HTML': {
        '<': '>'
    }
}


def autoKey(tpe, key):
    if tpe in keyList:
        if key in keyList[tpe]:
            return keyList[tpe][key]
