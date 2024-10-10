
from PySide6.QtWidgets import QTextEdit
from PySide6.QtGui import QTextCursor, QTextBlockFormat
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

    def set_text(self, text: str, block_format: QTextBlockFormat) -> None:
        self.append(text)
        if block_format:
            cursor = self.textCursor()
            cursor.mergeBlockFormat(block_format())

