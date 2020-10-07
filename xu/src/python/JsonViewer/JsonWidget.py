import json
import os

from PyQt5.QtCore import pyqtSignal
from PyQt5.QtWidgets import QVBoxLayout, QWidget, QToolButton, QHBoxLayout, QFileDialog

from xu.compa.Parapluie import Parapluie, PWidget, PResource, PLabelEdit
from xu.src.python.JsonViewer.Model import JSONFile
from xu.src.python.JsonViewer import JSONEditor
from xu.src.python.Utilities import Config


class JSONWidget(PWidget):
    alert = pyqtSignal(str, str, object, object)
    syncRequest = pyqtSignal(object)

    def __init__(self):
        super().__init__()

        self.jsonEditor = JSONEditor()
        self.jsonEditor.keyEvent.connect(self.editorEvent)

        syncButton = QToolButton()
        syncButton.setText("Sync")
        syncButton.setToolTip("Sync (Ctrl+B)")
        syncButton.setIcon(PResource.invertIcon(Parapluie.Icon_Double_Right_Chevron_Svg))
        syncButton.setFixedSize(36, 36)
        syncButton.pressed.connect(self.syncJson)

        formatButton = QToolButton()
        formatButton.setText("Format")
        formatButton.setToolTip("Format Code (Ctrl+F)")
        formatButton.setIcon(PResource.invertIcon(Parapluie.Icon_Clean_Code_Svg))
        formatButton.setFixedSize(36, 36)
        formatButton.pressed.connect(self.formatJson)

        saveButton = QToolButton()
        saveButton.setText("Save")
        saveButton.setToolTip("Save (Ctrl+S)")
        saveButton.setIcon(PResource.invertIcon(Parapluie.Icon_Save_Svg))
        saveButton.setFixedSize(36, 36)
        saveButton.pressed.connect(self.saveData)

        self.title = PLabelEdit()
        self.title.setFixedHeight(36)
        self.title.setMaximumHeight(36)
        self.title.setStyleSheet("QLabel{color:white; font-size:16px}")
        self.title.setText("Untitled")

        tool = QHBoxLayout()
        tool.addWidget(self.title)
        tool.addStretch()
        tool.addWidget(saveButton)
        tool.addWidget(formatButton)
        tool.addWidget(syncButton)

        widget = QWidget()
        widget.setLayout(tool)
        widget.layout().setContentsMargins(8, 0, 8, 0)
        widget.setObjectName(Parapluie.Object_Header)
        widget.setMaximumHeight(36)

        layout = QVBoxLayout()
        layout.addWidget(widget)
        layout.addWidget(self.jsonEditor)

        self.setLayout(layout)
        self.layout().setContentsMargins(5, 5, 5, 5)
        self.setObjectName(Parapluie.Object_Header)

        self.formater = JSONFormat()
        self.formater.setOnError(self.pushAlert)
        self.currentFile = None

    def formatJson(self, key: bool = False):
        text = self.jsonEditor.text()
        if text != "":
            new_text = self.formater.dumps(text, key)
            if new_text:
                self.jsonEditor.setText(new_text)

    def syncJson(self, key: bool = False):
        text = self.jsonEditor.text()
        if text != "":
            try:
                obj = json.loads(text)
                self.syncRequest.emit(obj)
            except Exception as ex:
                if not key:
                    self.pushAlert(str(ex))
        else:
            self.syncRequest.emit({})

    def pushAlert(self, text, tpe=Parapluie.Alert_Error):
        self.alert.emit(text, tpe, None, None)

    def setData(self, obj):
        text = self.formater.dumps(obj)
        self.jsonEditor.setText(text)

    def setText(self, text):
        self.jsonEditor.setText(text)

    def text(self):
        return self.jsonEditor.text()

    def editorEvent(self, key):
        if key == "ENTER":
            self.syncJson(True)
        elif key == "B":
            self.syncJson()
        elif key == "F":
            self.formatJson()

    def setTitle(self, title):
        self.title.setText(title)

    def setFile(self, file: JSONFile):
        # save data cũ
        if self.currentFile is not None:
            self.currentFile.unsavedData = self.text()
        # load data moi
        self.currentFile = file
        self.setTitle(file.name()[0])
        self.title.setEditable(not os.path.isfile(file.path))
        if file.unsavedData != "":
            self.setText(file.unsavedData)
        else:
            if os.path.isfile(file.path):
                d = open(file.path, "r", encoding="utf-8").read()
                self.setText(d)
            else:
                self.setText("")
        self.syncJson()

    def saveData(self):
        if self.currentFile is None:
            init_dir = Config.getViewerConfig_LastOpen()
            file = os.path.join(init_dir, self.title.text())
            name = QFileDialog.getSaveFileName(self, 'Save file', file, "JSON files (*.json)")
            if name[0] != "":
                config = Config.getConfig()
                config["viewer"]["last_open"] = os.path.dirname(name[0])
                Config.updateConfig(config)
                self.currentFile = JSONFile(name[0])
                self.save(self.currentFile)
        else:
            if not os.path.isfile(self.currentFile.path):
                name = QFileDialog.getSaveFileName(self, 'Save file', self.currentFile.path, "JSON files (*.json)")
                if name[0] != "":
                    self.currentFile.path = name
                    self.save(self.currentFile)
            else:
                self.save(self.currentFile)

    def save(self, f: JSONFile):
        try:
            file = open(f.path, "w", encoding="utf-8")
            file.write(self.text())
            file.close()
            f.unsavedData = ""
            self.pushAlert("Saved: " + f.path, Parapluie.Alert_Information)
        except Exception as ex:
            self.pushAlert(str(ex))


class JSONFormat:
    error = None

    def dumps(self, obj, key: bool = False):
        if isinstance(obj, str):
            return self.string_to_html(obj, key)
        else:
            return self.json_to_html(obj)

    def json_to_html(self, obj):
        formatted_json = json.dumps(obj, sort_keys=False, indent=4, ensure_ascii=False)
        return formatted_json

    def string_to_html(self, obj, key: bool = False):
        try:
            js = json.loads(obj)
            formatted_json = json.dumps(js, sort_keys=False, indent=4, ensure_ascii=False)
            return formatted_json
        except Exception as ex:
            if self.error is not None and not key:
                self.error(str(ex))
            return None

    def setOnError(self, error):
        self.error = error
