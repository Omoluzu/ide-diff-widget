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

        self.current_file = CurrentFile()
        self.modified_file = ModifiedFile()

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.current_file)
        splitter.addWidget(self.modified_file)

        self.layout = QVBoxLayout(self)
        self.layout.addWidget(splitter)

        with (
                open(files.current_file, encoding='utf-8') as current_file,
                open(files.modified_file, encoding='utf-8') as modified_file,
        ):
            compare_files(
                lines1=current_file.readlines(),
                lines2=modified_file.readlines(),
                func_equals=self.equals,
                func_modified=self.modified,
                func_remove=self.remove,
                func_added=self.added,
                sequence_percent=90
            )

    def equals(self, index1: int, index2: int, text: str):
        text = text.replace('\n', '')
        self.current_file.text_edit.append(text)
        self.modified_file.text_edit.append(text)

    def modified(self, index1: int, index2: int, text1: str, text2: str):
        self.current_file.text_edit.append(text1.replace('\n', ''))
        self.modified_file.text_edit.append(text2.replace('\n', ''))

    def remove(self, index: int, text: str):
        self.current_file.text_edit.append(text.replace('\n', ''))
        self.modified_file.text_edit.append('')

    def added(self, index: int, text: str):
        self.current_file.text_edit.append('')
        self.modified_file.text_edit.append(text.replace('\n', ''))
