from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSplitter, QTextEdit, QHBoxLayout
)
from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

from src.diff_widget.script import compare_files


class ABCFile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # self.text: str = file.read()

        self.text_edit = QTextEdit()
        # self.text_edit.append(self.text)
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)

        self.line = QTextEdit()
        self.line.setFixedWidth(50)

        self.layout = QHBoxLayout(self)
        self.draw()

    def draw(self):
        pass


class CurrentFile(ABCFile):
    def draw(self):
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.line)


class ModifiedFile(ABCFile):
    def draw(self):
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.text_edit)


class DiffWidget(QWidget):
    def __init__(self, files, *args, **kwargs):
        super().__init__(*args, **kwargs)

        with (
                open(files.current_file, encoding='utf-8') as current_file,
                open(files.modified_file, encoding='utf-8') as modified_file,
        ):
            compare_files(
                lines1=current_file.readlines(),
                lines2=modified_file.readlines(),
                sequence_percent=90
            )

        self.current_file = CurrentFile()
        self.modified_file = ModifiedFile()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.current_file)
        splitter.addWidget(self.modified_file)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(splitter)
