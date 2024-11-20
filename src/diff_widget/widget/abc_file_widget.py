from abc import abstractmethod
from typing import Union

from PySide6.QtWidgets import QWidget, QHBoxLayout


from src.diff_widget import text_edit


class ABCFile(QWidget):
    def __init__(self, backlight, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_edit = text_edit.Edit(backlight=backlight)
        self.line = text_edit.Line()

        self.layout = QHBoxLayout(self)
        self.layout.setContentsMargins(0, 0, 0, 0)
        self.layout.setSpacing(1)

        self.draw()

        self.setStyleSheet("""
            margin: 0; 
            padding: 0;  
            border: none !important;
            background-color: gray;
        """)

    @abstractmethod
    def draw(self):
        pass

    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """
        self.text_edit.scaled_font_size(new_font_size)
        self.line.scaled_font_size(new_font_size)

    def set_text(
            self, line_number: Union[str, int] = '',
            text: str = '\n',
            block_format=None
    ) -> None:
        """Set text TextWidget and set line number and color
        :param line_number: line number, default ''
        :param text: added text, default ''
        :param block_format: color text. default None
        """
        self.text_edit.set_text(text, block_format)
        self.line.set_text(str(line_number) + '\n', block_format)

    def delete_lines(self, lines_to_delete: list[int]) -> None:
        """Deleted lines to QTextWidget
        :param lines_to_delete: List line to deleted
        """
        self.text_edit.delete_lines(lines_to_delete=lines_to_delete)
        self.line.delete_lines(lines_to_delete=lines_to_delete)
