from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

from .abc_text_edit import ABCTextEdit


class EditTextEdit(ABCTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
