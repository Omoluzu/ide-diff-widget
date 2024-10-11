from PySide6.QtCore import Qt

from .abc_text_edit import ABCTextEdit


class LineTextEdit(ABCTextEdit):
    def __init__(self):
        super().__init__()
        self.setReadOnly(True)

        self.setVerticalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setHorizontalScrollBarPolicy(Qt.ScrollBarAlwaysOff)
        self.setTextInteractionFlags(Qt.NoTextInteraction)

        self.setStyleSheet("""
            padding: -3.7px; 
            color: gray;
            background-color: rgb(36, 41, 46);
        """)

    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """
        super().scaled_font_size(new_font_size)
        self.setFixedWidth(new_font_size * 3)
