from PySide6.QtGui import QColor, QTextCharFormat


class OrangeTextCharFormat(QTextCharFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setForeground(QColor(185, 141, 93))
