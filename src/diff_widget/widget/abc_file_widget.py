from PySide6.QtWidgets import QWidget, QTextEdit, QHBoxLayout
from PySide6.QtGui import QTextOption, QTextCursor
from PySide6.QtCore import Qt


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

    def wheelEvent(self, event):
        if event.modifiers() == Qt.ControlModifier:
            self.parent().parent().parent().scaled_font_size(
                y_mouse_rotation=event.angleDelta().y())
            event.accept()
        else:
            y = event.angleDelta().y()
            self.verticalScrollBar().setValue(
                self.verticalScrollBar().value() + (-20 if y > 0 else 20))


class EditTextEdit(ABCTextEdit):
    pass


class LineTextEdit(ABCTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """ 
        super().scaled_font_size(new_font_size)
        self.setFixedWidth(new_font_size * 4)


class ABCFile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_edit = EditTextEdit()
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)
        self.text_edit.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

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
