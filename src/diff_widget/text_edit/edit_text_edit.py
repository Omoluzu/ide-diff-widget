from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

from .abc_text_edit import ABCTextEdit
from src.diff_widget import highlighter


class EditTextEdit(ABCTextEdit):
    def __init__(self, backlight, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        highlighter.Highlighter(document=self.document(), backlight=backlight)

        self.setStyleSheet("""
            padding: -3.7px; 
            color: #EBEBEB;
            background-color: rgb(36, 41, 46);
        """)

    def keyPressEvent(self, event):
        cursor = self.textCursor()
        current_line = cursor.blockNumber()

        index_hide_lines = self.parent().parent().parent().index_hide_lines
        if current_line in index_hide_lines:
            if event.key() not in [Qt.Key_Down, Qt.Key_Up]:
                event.ignore()
                return

        super().keyPressEvent(event)
