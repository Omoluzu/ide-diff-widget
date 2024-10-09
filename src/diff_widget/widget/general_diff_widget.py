from PySide6.QtWidgets import (
    QWidget, QVBoxLayout, QSplitter
)
from PySide6.QtCore import Qt

from src.diff_widget.script import compare_files
from .current_file_widget import CurrentFile
from .modified_file_widget import ModifiedFile


class DiffWidget(QWidget):
    def __init__(self, files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_font_size = 10

        self.current_file = CurrentFile()
        self.current_file.scaled_font_size(self.current_font_size)
        self.modified_file = ModifiedFile()
        self.modified_file.scaled_font_size(self.current_font_size)

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

        self.set_logical_vertical_scroll_bar()

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.scaled_font_size(y_mouse_rotation=event.angleDelta().y())
            event.accept()

    def equals(self, index1: int, index2: int, text: str):
        text = text.replace('\n', '')
        self.current_file.text_edit.append(text)
        self.current_file.line.append(str(index1))
        self.modified_file.text_edit.append(text)
        self.modified_file.line.append(str(index2))

    def modified(self, index1: int, index2: int, text1: str, text2: str):
        self.current_file.text_edit.append(text1.replace('\n', ''))
        self.current_file.line.append(str(index1))
        self.modified_file.text_edit.append(text2.replace('\n', ''))
        self.modified_file.line.append(str(index2))

    def remove(self, index: int, text: str):
        self.current_file.text_edit.append(text.replace('\n', ''))
        self.current_file.line.append(str(index))
        self.modified_file.text_edit.append('')
        self.modified_file.line.append('')

    def added(self, index: int, text: str):
        self.current_file.text_edit.append('')
        self.current_file.line.append('')
        self.modified_file.text_edit.append(text.replace('\n', ''))
        self.modified_file.line.append(str(index))

    def set_logical_vertical_scroll_bar(self) -> None:
        """Set logical vertical scroll bar"""
        self.current_file.text_edit.verticalScrollBar().valueChanged.connect(
            self.current_file.line.verticalScrollBar().setValue)
        self.current_file.text_edit.verticalScrollBar().valueChanged.connect(
            self.modified_file.text_edit.verticalScrollBar().setValue)
        self.current_file.text_edit.verticalScrollBar().valueChanged.connect(
            self.modified_file.line.verticalScrollBar().setValue)

        self.current_file.line.verticalScrollBar().valueChanged.connect(
            self.current_file.text_edit.verticalScrollBar().setValue)
        self.current_file.line.verticalScrollBar().valueChanged.connect(
            self.modified_file.text_edit.verticalScrollBar().setValue)
        self.current_file.line.verticalScrollBar().valueChanged.connect(
            self.modified_file.line.verticalScrollBar().setValue)

        self.modified_file.text_edit.verticalScrollBar().valueChanged.connect(
            self.current_file.line.verticalScrollBar().setValue)
        self.modified_file.text_edit.verticalScrollBar().valueChanged.connect(
            self.current_file.text_edit.verticalScrollBar().setValue)
        self.modified_file.text_edit.verticalScrollBar().valueChanged.connect(
            self.modified_file.line.verticalScrollBar().setValue)

        self.modified_file.line.verticalScrollBar().valueChanged.connect(
            self.current_file.line.verticalScrollBar().setValue)
        self.modified_file.line.verticalScrollBar().valueChanged.connect(
            self.current_file.text_edit.verticalScrollBar().setValue)
        self.modified_file.line.verticalScrollBar().valueChanged.connect(
            self.modified_file.text_edit.verticalScrollBar().setValue)

    def scaled_font_size(self, y_mouse_rotation: int) -> None:
        """Scaled font size all diff widget
        :param y_mouse_rotation: Mouse rotation angle by z
        """
        if y_mouse_rotation > 0:
            self.current_font_size += 1
        else:
            if self.current_font_size < 10:
                return
            self.current_font_size -= 1

        self.current_file.scaled_font_size(self.current_font_size)
        self.modified_file.scaled_font_size(self.current_font_size)
