from PySide6.QtGui import QColor, QTextCharFormat


class BlueTextCharFormat(QTextCharFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setForeground(QColor(135, 113, 181))
