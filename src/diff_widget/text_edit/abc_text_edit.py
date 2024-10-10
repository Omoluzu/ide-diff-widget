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

    def get_text_from_line(self, line_number: int):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)

        for _ in range(line_number):
            cursor.movePosition(QTextCursor.Down)

        return cursor.block().text()

    def delete_lines(self, lines_to_delete):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)
        lines_deleted = 0

        for line in range(self.document().blockCount() + 1):
            if line in lines_to_delete:
                cursor.movePosition(QTextCursor.StartOfBlock)
                cursor.movePosition(QTextCursor.EndOfBlock, QTextCursor.KeepAnchor)
                cursor.removeSelectedText()

                cursor.movePosition(QTextCursor.EndOfBlock)
                cursor.deleteChar()
                lines_deleted += 1

            else:
                cursor.movePosition(QTextCursor.Down)

            if lines_deleted == len(lines_to_delete):
                break

    def add_lines(
            self, indices: list[int],
            block_format: QTextBlockFormat,
            text: str = " "
    ):
        cursor = self.textCursor()
        cursor.movePosition(QTextCursor.Start)

        for line in range(1, self.document().blockCount() + 1):
            cursor.movePosition(QTextCursor.Down)

            if line in indices:
                cursor.insertText(text + "\n")
                cursor.movePosition(QTextCursor.Up)
                cursor.mergeBlockFormat(block_format())
                cursor.movePosition(QTextCursor.Down)
