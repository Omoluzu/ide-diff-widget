from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt

from src.diff_widget.script import compare_files
from .current_file_widget import CurrentFile
from .modified_file_widget import ModifiedFile
from src.diff_widget import block_format, script


def index_update(func):
    def wrapper(self, *args, **kwargs):
        self.line_index += 1
        return func(self, *args, **kwargs)

    return wrapper


def index_save(func):
    def wrapper(self, *args, **kwargs):
        self.show_lines.append(self.line_index)
        return func(self, *args, **kwargs)

    return wrapper


class DiffWidget(QWidget):
    def __init__(self, files, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_font_size = 10
        self.line_index = 0
        self.show_lines: list[int] = []

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
                sequence_percent=files.sequence_percent
            )

        self.set_logical_vertical_scroll_bar()
        self.hiding_unmodified_lines_code()

    @index_update
    def equals(self, index1: int, index2: int, text: str):
        self.current_file.set_text(
            line_number=str(index1),
            text=text.replace('\n', ''),
            block_format=block_format.Simple)

        self.modified_file.set_text(
            line_number=str(index2),
            text=text.replace('\n', ''),
            block_format=block_format.Simple)

    @index_save
    @index_update
    def modified(self, index1: int, index2: int, text1: str, text2: str):
        self.current_file.set_text(
            line_number=str(index1),
            text=text1.replace('\n', ''),
            block_format=block_format.Simple)

        self.modified_file.set_text(
            line_number=str(index2),
            text=text2.replace('\n', ''),
            block_format=block_format.Simple)

    @index_save
    @index_update
    def remove(self, index: int, text: str):
        self.current_file.set_text(
            line_number=str(index),
            text=text.replace('\n', ''),
            block_format=block_format.Minus)

        self.modified_file.set_text(
            line_number='',
            text='',
            block_format=block_format.Diff)

    @index_save
    @index_update
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

    def hiding_unmodified_lines_code(self):
        margin_show_lines = set()

        for line in self.show_lines:
            for i in range(1, 4):
                if line - 1 >= 0:
                    margin_show_lines.add(line - i)
                if line + i <= self.line_index:
                    margin_show_lines.add(line + i)

            margin_show_lines.add(line)

        hide_lines = list(margin_show_lines ^ set(range(self.line_index + 1)))
        blocks_hide_lines = script.break_into_blocks(hide_lines)

        for line in hide_lines[::-1]:
            text = self.current_file.text_edit.get_text_from_line(line)
            blocks_hide_lines[line]['text'] = text

        self.current_file.text_edit.delete_lines(hide_lines)
        self.current_file.line.delete_lines(hide_lines)
        self.modified_file.text_edit.delete_lines(hide_lines)
        self.modified_file.line.delete_lines(hide_lines)

        indices = []
        for block, start_number in blocks_hide_lines['block_id'].items():
            indices.append(start_number - hide_lines.index(start_number))

        self.current_file.text_edit.add_lines(
            indices, block_format.Diff, "@@ __,__ @@")
        self.current_file.line.add_lines(indices, block_format.Diff)
        self.modified_file.text_edit.add_lines(
            indices, block_format.Diff, "@@ __,__ @@")
        self.modified_file.line.add_lines(indices, block_format.Diff)

        # print(hide_lines)
        # print(blocks_hide_lines)
        #
        # data = {
        #     'block_id': {
        #         0: 18,
        #         1: 37
        #     },
        #     18: {
        #         'block_id': 0,
        #         'text': '    def draw(self):'
        #     },
        #
        #     37:  {
        #         'block_id': 1
        #     }
        # }

