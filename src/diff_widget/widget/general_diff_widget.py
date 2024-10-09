from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSplitter, QTextEdit, QHBoxLayout
)
from PySide6.QtCore import Qt


class ABCFile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text = QTextEdit()
        self.line = QTextEdit()
        self.line.setFixedWidth(50)

        self.layout = QHBoxLayout(self)
        self.draw()

    def draw(self):
        pass


class CurrentFile(ABCFile):
    def draw(self):
        self.layout.addWidget(self.text)
        self.layout.addWidget(self.line)


class ModifiedFile(ABCFile):
    def draw(self):
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.text)


class DiffWidget(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.current_file = CurrentFile()
        self.modified_file = ModifiedFile()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.current_file)
        splitter.addWidget(self.modified_file)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(splitter)
