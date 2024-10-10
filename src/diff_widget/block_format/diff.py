from PySide6.QtGui import QColor, QTextBlockFormat


class DiffTextBlockFormat(QTextBlockFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setBackground(QColor(29, 33, 37))
