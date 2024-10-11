from PySide6.QtGui import QTextOption
from PySide6.QtCore import Qt

from .abc_text_edit import ABCTextEdit
from src.diff_widget import highlighter


class EditTextEdit(ABCTextEdit):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setWordWrapMode(QTextOption.NoWrap)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)

        highlighter.Highlighter(diff_file=self)

        self.setStyleSheet("""
            padding: -3.7px; 
            color: #EBEBEB;
            background-color: rgb(36, 41, 46);
        """)
