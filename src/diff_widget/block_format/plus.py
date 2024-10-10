from PySide6.QtGui import QColor, QTextBlockFormat


class PlusTextBlockFormat(QTextBlockFormat):
    def __init__(self, *args, **kwargs):
        super().__init__()
        self.setBackground(QColor(12, 69, 50))


