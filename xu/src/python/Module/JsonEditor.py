from PyQt5 import Qsci


class JSONEditor(Qsci.QsciScintilla):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.lexer = Qsci.QsciLexerJSON(self)
        self.lexer.setAutoIndentStyle(Qsci.QsciScintilla.AiMaintain)
        self.setLexer(self.lexer)
