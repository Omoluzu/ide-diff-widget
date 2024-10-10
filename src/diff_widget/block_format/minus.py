from PySide6.QtGui import QColor, QTextBlockFormat


class MinusTextBlockFormat(QTextBlockFormat):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setBackground(QColor(69, 12, 15))
