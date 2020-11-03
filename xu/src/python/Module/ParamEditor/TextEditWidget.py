import json
import os
import xml.etree.ElementTree as Et

from PyQt5 import Qsci
from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QToolButton, QHBoxLayout, QFileDialog

from xu.compa.Parapluie import Parapluie, PWidget, PResource, PLabelEdit, PComboBox
from xu.src.python.Model import XFile
from xu.src.python.Module.ParamEditor import Formatter, EditorType
from xu.src.python.Module.ParamEditor.TextEditor import TextEditor
from xu.src.python.Utilities import MiniView, Config


class TextEditWidget(PWidget):
    alert = pyqtSignal(str, str, object, object)
    syncRequest = pyqtSignal(object)
    editorTypeChanged = pyqtSignal(object)

    def __init__(self, editType: EditorType = EditorType.Manual, save: bool = True, sync: bool = True):
        super().__init__()
        self.editor = TextEditor()
        self.editor.keyEvent.connect(self.editorEvent)

        tool = QHBoxLayout()

        if save:
            iconSize = 36
        else:
            iconSize = 24

        if save:
            self.title = PLabelEdit()
            self.title.setMaximumWidth(300)
            self.title.setFixedHeight(iconSize)
            self.title.setMaximumHeight(iconSize)
            # self.title.setStyleSheet("QLabel{color:white; font-size:16px}")
            self.title.setText("Untitled")
            tool.addWidget(self.title)

        tool.addStretch()

        if editType == EditorType.Manual:
            self.editorTypeBox = PComboBox()
            self.editorTypeBox.setView(MiniView.listView())
            self.editorTypeBox.addItems(["Text", "JSON", "XML", "HTML"])
            self.editorTypeBox.currentIndexChanged.connect(self.editorTypeChange)
            tool.addWidget(self.editorTypeBox)

        self.wrapButton = QToolButton()
        self.wrapButton.setCheckable(True)
        self.wrapButton.setText("Wrap")
        self.wrapButton.setToolTip("Wrap/Unwrap (Ctrl+W)")
        self.wrapButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Wrap_Text_Svg))
        self.wrapButton.setFixedSize(iconSize, iconSize)
        self.wrapButton.pressed.connect(self.wrapText)
        tool.addWidget(self.wrapButton)


        formatButton = QToolButton()
        formatButton.setText("Format")
        formatButton.setToolTip("Format Code (Ctrl+F)")
        formatButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Clean_Code_Svg))
        formatButton.setFixedSize(iconSize, iconSize)
        formatButton.pressed.connect(self.formatText)
        tool.addWidget(formatButton)

        if save:
            saveButton = QToolButton()
            saveButton.setText("Save")
            saveButton.setToolTip("Save (Ctrl+S)")
            saveButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Save_Svg))
            saveButton.setFixedSize(iconSize, iconSize)
            saveButton.pressed.connect(self.saveData)
            tool.addWidget(saveButton)

        if sync:
            syncButton = QToolButton()
            syncButton.setText("Sync")
            syncButton.setToolTip("Sync (Ctrl+B)")
            syncButton.setIcon(PResource.defaultIcon(Parapluie.Icon_Double_Right_Chevron_Svg))
            syncButton.setFixedSize(iconSize, iconSize)
            syncButton.pressed.connect(self.syncJson)
            tool.addWidget(syncButton)

        widget = QWidget()
        widget.setLayout(tool)
        widget.layout().setContentsMargins(8, 0, 8, 0)
        widget.setObjectName(Parapluie.Object_Editor_Header)
        widget.setMaximumHeight(iconSize)

        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(self.editor)

        self.setLayout(layout)
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.setObjectName(Parapluie.Object_Editor)

        self.currentFile = None

        self.editType = EditorType.Text
        self.setEditorType(EditorType.Text)

    def formatText(self, key: bool = False):
        text = self.editor.text()
        if text != "":
            new_text = Formatter.dumps(text, self.editType, self.pushAlert if not key else None)
            if new_text:
                self.editor.setText(new_text)

    def syncJson(self, key: bool = False):
        obj = self.getData(key)
        if self.editType == EditorType.JSON or self.editType == EditorType.XML:
            self.syncRequest.emit(obj)

    def pushAlert(self, text, tpe=Parapluie.Alert_Error):
        self.alert.emit(text, tpe, None, None)

    def setData(self, obj):
        text = Formatter.dumps(obj, self.editType, self.pushAlert if obj is None else None)
        self.editor.setText(text)

    def getData(self, key: bool = False):
        text = self.editor.text()
        if text != "":
            if self.editType == EditorType.JSON:
                try:
                    obj = json.loads(text)
                    return obj
                except Exception as ex:
                    if not key:
                        self.pushAlert(str(ex))
                    return None
            elif self.editType == EditorType.XML:
                try:
                    obj = Et.fromstring(text)
                    return obj
                except Exception as ex:
                    if not key:
                        self.pushAlert(str(ex))
                    return None
        else:
            if self.editType == EditorType.JSON:
                return {}
            elif self.editType == EditorType.XML:
                return None
        return text

    def setText(self, text):
        self.editor.setText(text)

    def text(self):
        return self.editor.text()

    def wrapText(self):
        if self.wrapButton.isChecked():
            self.editor.setWrapMode(Qsci.QsciScintilla.WrapNone)
        else:
            self.editor.setWrapMode(Qsci.QsciScintilla.WrapWord)

    def editorEvent(self, key):
        if key == "ENTER":
            self.syncJson(True)
        elif key == "B":
            self.syncJson()
        elif key == "F":
            self.formatText()

    def setTitle(self, title):
        self.title.setText(title)

    def setEditorType(self, tpe: EditorType, inner=False):
        self.editType = tpe
        if not inner:
            self.editorTypeBox.setCurrentIndex(tpe.value)

        if tpe == EditorType.JSON:
            self.editor.changeLexer(Qsci.QsciLexerJSON(self.editor), 'JSON')
        elif tpe == EditorType.XML:
            self.editor.changeLexer(Qsci.QsciLexerXML(self.editor), 'XML')
        elif tpe == EditorType.HTML:
            self.editor.changeLexer(Qsci.QsciLexerHTML(self.editor), 'HTML')
        elif tpe == EditorType.Javascript:
            self.editor.changeLexer(Qsci.QsciLexerJavaScript(self.editor), 'Javascript')
        else:
            self.editor.changeLexer(Qsci.QsciLexerMarkdown(self.editor), 'Text<')

        self.editorTypeChanged.emit(tpe.value)

    def blockEditorType(self, block):
        self.editorTypeBox.setVisible(not block)

    # ["Text", "JSON", "XML", "HTML"]
    def editorTypeChange(self, index):
        if index == 0:
            self.setEditorType(EditorType.Text, True)
        elif index == 1:
            self.setEditorType(EditorType.JSON, True)
        elif index == 2:
            self.setEditorType(EditorType.XML, True)
        elif index == 3:
            self.setEditorType(EditorType.HTML, True)

    def setFile(self, file: XFile):
        # save data cũ
        if self.currentFile is not None:
            self.currentFile.unsavedData = self.text()
        # load data moi
        self.currentFile = file
        self.setTitle(file.name()[0])

        if file.name()[1].lower() == '.json':
            self.setEditorType(EditorType.JSON)
        elif file.name()[1].lower() == '.xml':
            self.setEditorType(EditorType.XML)
        elif file.name()[1].lower() == '.html':
            self.setEditorType(EditorType.HTML)
        elif file.name()[1].lower() == '.js':
            self.setEditorType(EditorType.Javascript)
        else:
            self.setEditorType(EditorType.Text)

        self.title.setEditable(not os.path.isfile(file.getPath()))
        if file.unsavedData != "":
            self.setText(file.unsavedData)
        else:
            if os.path.isfile(file.getPath()):
                d = open(file.getPath(), "r", encoding="utf-8").read()
                self.setText(d)
            else:
                self.setText("")
        self.syncJson()

    def saveData(self):
        if self.currentFile is None:
            init_dir = Config.getViewerConfig_LastOpen()
            file = os.path.join(init_dir, self.title.text())
            name = QFileDialog.getSaveFileName(self, 'Save file', file, self.getFileExtension())
            if name[0] != "":
                config = Config.getConfig()
                config["viewer"]["last_open"] = os.path.dirname(name[0])
                Config.updateConfig(config)
                self.currentFile = XFile(name[0])
                self.save(self.currentFile)
        else:
            if not os.path.isfile(self.currentFile.getPath()):
                name = QFileDialog.getSaveFileName(self, 'Save file', self.currentFile.getPath(), self.getFileExtension())
                if name[0] != "":
                    self.currentFile.setPath(name)
                    self.save(self.currentFile)
            else:
                self.save(self.currentFile)

    def save(self, f: XFile):
        try:
            file = open(f.getPath(), "w", encoding="utf-8")
            file.write(self.text())
            file.close()
            f.unsavedData = ""
            self.pushAlert("Saved: " + f.getPath(), Parapluie.Alert_Information)
        except Exception as ex:
            self.pushAlert(str(ex))

    def getFileExtension(self):
        if self.editType == EditorType.JSON:
            return "JSON files (*.json);; All files (*)"
        elif self.editType == EditorType.XML:
            return "XML files (*.xml);; All files (*)"
        elif self.editType == EditorType.HTML:
            return "HTML files (*.html);; All files (*)"
        elif self.editType == EditorType.Javascript:
            return "Javascript files (*.js);; All files (*)"
        else:
            return "All files (*)"
