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
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_font_size = 10
        self.line_index = 0
        self.show_lines: list[int] = []
        self.blocks_hide_lines = {}

        self.current_file = CurrentFile(backlight=config.backlight)
        self.current_file.scaled_font_size(self.current_font_size)
        self.modified_file = ModifiedFile(backlight=config.backlight)
        self.modified_file.scaled_font_size(self.current_font_size)

        splitter = QSplitter(Qt.Horizontal)
        splitter.addWidget(self.current_file)
        splitter.addWidget(self.modified_file)

        self.layout = QVBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(0)
        self.layout.addWidget(splitter)

        with (
                open(config.current_file, encoding='utf-8') as current_file,
                open(config.modified_file, encoding='utf-8') as modified_file,
        ):
            compare_files(
                lines1=current_file.readlines(),
                lines2=modified_file.readlines(),
                func_equals=self.equals,
                func_modified=self.modified,
                func_remove=self.remove,
                func_added=self.added,
                sequence_percent=config.sequence_percent
            )

        self.set_logical_vertical_scroll_bar()
        self.hiding_unmodified_lines_code()

        self.setStyleSheet("""
            margin: 0; 
            padding: 0;  
            border: none !important;
            background-color: gray;
        """)

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
        self.blocks_hide_lines = script.break_into_blocks(hide_lines)

        for line in hide_lines[::-1]:
            text = self.current_file.text_edit.get_text_from_line(line)
            current_line = self.current_file.line.get_text_from_line(line)
            modified_line = self.modified_file.line.get_text_from_line(line)
            self.blocks_hide_lines['line_id'][line]['text'] = text
            self.blocks_hide_lines['line_id'][line]['current_line'] = current_line
            self.blocks_hide_lines['line_id'][line]['modified_line'] = modified_line

        self.current_file.text_edit.delete_lines(hide_lines)
        self.current_file.line.delete_lines(hide_lines)
        self.modified_file.text_edit.delete_lines(hide_lines)
        self.modified_file.line.delete_lines(hide_lines)

        indices = []
        for block, start_number in self.blocks_hide_lines['block_id'].items():
            block_start_pos = start_number - hide_lines.index(start_number)
            indices.append(block_start_pos)
            self.blocks_hide_lines['block_id'][block] = block_start_pos + block

        self.current_file.text_edit.add_lines(
            indices, block_format.OpenBlock, " @@ __,__ @@")
        self.current_file.line.add_lines(indices, block_format.OpenBlock)
        self.modified_file.text_edit.add_lines(
            indices, block_format.OpenBlock, " @@ __,__ @@")
        self.modified_file.line.add_lines(indices, block_format.OpenBlock)

    @property
    def index_hide_lines(self) -> list[int]:
        return list(self.blocks_hide_lines['block_id'].values())

    def show_hide_lines_block(self, index_position_block: int):
        block_id = None
        for key, value in self.blocks_hide_lines['block_id'].items():
            if value == index_position_block:
                block_id = key
                del self.blocks_hide_lines['block_id'][block_id]
                break

        self.current_file.text_edit.delete_lines([index_position_block])
        self.current_file.line.delete_lines([index_position_block])
        self.modified_file.text_edit.delete_lines([index_position_block])
        self.modified_file.line.delete_lines([index_position_block])

        index_position_new_text = 0
        for line in self.blocks_hide_lines['line_id'].values():
            if line['block_id'] == block_id:
                self.current_file.text_edit.add_text(
                    position=index_position_block + index_position_new_text,
                    block_format=block_format.OpenBlock, text=line['text']
                )
                self.current_file.line.add_text(
                    position=index_position_block + index_position_new_text,
                    block_format=block_format.OpenBlock,
                    text=line['current_line']
                )
                self.modified_file.text_edit.add_text(
                    position=index_position_block + index_position_new_text,
                    block_format=block_format.OpenBlock, text=line['text']
                )
                self.modified_file.line.add_text(
                    position=index_position_block + index_position_new_text,
                    block_format=block_format.OpenBlock,
                    text=line['modified_line']
                )
                index_position_new_text += 1

        index_offset = index_position_new_text - 1

        for key, value in self.blocks_hide_lines['block_id'].items():
            if key > block_id:
                self.blocks_hide_lines['block_id'][key] = value + index_offset
