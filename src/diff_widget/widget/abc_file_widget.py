from PySide6.QtWidgets import QWidget, QTextEdit, QHBoxLayout
from PySide6.QtGui import QTextOption, QTextCursor


class ABCTextEdit(QTextEdit):
    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """
        cursor = self.textCursor()
        cursor.select(QTextCursor.Document)
        char_format = cursor.charFormat()
        char_format.setFontPointSize(new_font_size)
        cursor.mergeCharFormat(char_format)
        cursor.clearSelection()


class LineTextEdit(ABCTextEdit):
    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """ 
        super().scaled_font_size(new_font_size)
        self.setFixedWidth(new_font_size * 4)


class ABCFile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_edit = ABCTextEdit()
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)

        self.line = LineTextEdit()
        self.line.setFixedWidth(50)

        self.layout = QHBoxLayout(self)
        self.draw()

    def draw(self):
        pass

    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """
        self.text_edit.scaled_font_size(new_font_size)
        self.line.scaled_font_size(new_font_size)
