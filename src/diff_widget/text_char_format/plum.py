from PySide6.QtGui import QColor, QTextCharFormat


class PlumTextCharFormat(QTextCharFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setForeground(QColor(153, 17, 153))
