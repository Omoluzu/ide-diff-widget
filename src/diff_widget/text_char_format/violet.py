from PySide6.QtGui import QColor, QTextCharFormat


class VioletTextCharFormat(QTextCharFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setForeground(QColor(215, 104, 117))
