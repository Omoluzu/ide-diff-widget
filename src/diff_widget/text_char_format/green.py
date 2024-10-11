from PySide6.QtGui import QColor, QTextCharFormat


class GreenTextCharFormat(QTextCharFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setForeground(QColor(179, 222, 82))
