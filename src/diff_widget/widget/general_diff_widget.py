from PySide6.QtWidgets import QWidget, QVBoxLayout, QSplitter
from PySide6.QtCore import Qt

from src.diff_widget.script import compare_files
from .current_file_widget import CurrentFile
from .modified_file_widget import ModifiedFile
from src.diff_widget import block_format, script, interfaces, control


class DiffWidget(QWidget):
    def __init__(self, config, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.current_font_size = 10
        self.blocks_hide_lines = {}  # todo: remove
        self.hidden_block = control.HiddenBlock()

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

        interfaces_init_text_edit = interfaces.InitTextEdit(
            current_text_edit=self.current_file,
            modified_text_edit=self.modified_file,
            control_hide_block=self.hidden_block
        )

        with (
                open(config.current_file, encoding='utf-8') as current_file,
                open(config.modified_file, encoding='utf-8') as modified_file,
        ):
            compare_files(
                lines1=current_file.readlines(),
                lines2=modified_file.readlines(),
                func_equals=interfaces_init_text_edit.equals,
                func_modified=interfaces_init_text_edit.modified,
                func_remove=interfaces_init_text_edit.remove,
                func_added=interfaces_init_text_edit.added,
                sequence_percent=config.sequence_percent
            )

        self.line_index = interfaces_init_text_edit.line_index  # todo: remove
        self.show_lines = interfaces_init_text_edit.show_lines  # todo: remove

        self.set_logical_vertical_scroll_bar()
        # self.hiding_unmodified_lines_code()

        self.setStyleSheet("""
            margin: 0; 
            padding: 0;  
            border: none !important;
            background-color: gray;
        """)

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
        # todo: improve hiding lines.
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
        """Getting index position hide lines block
        :return: List index hide lines block"""
        return self.hidden_block.position

    def delete_lines(self, lines_to_delete: list[int]) -> None:
        """Deleted lines to QTextWidget
        :param lines_to_delete: List line to deleted
        """
        self.current_file.delete_lines(lines_to_delete)
        self.modified_file.delete_lines(lines_to_delete)

    def show_hide_lines_block(self, index_position_block: int):
        hidden_block = self.hidden_block.get_block(index_position_block)

        self.delete_lines(lines_to_delete=[index_position_block])

        index_position_new_text = 0
        for line in self.blocks_hide_lines['line_id'].values():  # todo: нету больше blocks_hide_lines
            if line['block_id'] == hidden_block.id:
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
            if key > hidden_block.id:
                self.blocks_hide_lines['block_id'][key] = value + index_offset
