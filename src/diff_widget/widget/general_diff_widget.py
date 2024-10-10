from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt

from src.diff_widget.script import compare_files
from .current_file_widget import CurrentFile
from .modified_file_widget import ModifiedFile
from src.diff_widget import block_format


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

    def equals(self, index1: int, index2: int, text: str):
        self.current_file.set_text(
            line_number=str(index1),
            text=text.replace('\n', ''),
            block_format=block_format.Simple)

        self.modified_file.set_text(
            line_number=str(index2),
            text=text.replace('\n', ''),
            block_format=block_format.Simple)

    def modified(self, index1: int, index2: int, text1: str, text2: str):
        self.current_file.set_text(
            line_number=str(index1),
            text=text1.replace('\n', ''),
            block_format=block_format.Simple)

        self.modified_file.set_text(
            line_number=str(index2),
            text=text2.replace('\n', ''),
            block_format=block_format.Simple)

    def remove(self, index: int, text: str):
        self.current_file.set_text(
            line_number=str(index),
            text=text.replace('\n', ''),
            block_format=block_format.Minus)

        self.modified_file.set_text(
            line_number='',
            text='',
            block_format=block_format.Diff)

    def added(self, index: int, text: str):
        self.current_file.set_text(
            line_number='',
            text='',
            block_format=block_format.Diff)

        self.modified_file.set_text(
            line_number=str(index),
            text=text.replace('\n', ''),
            block_format=block_format.Plus)

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
