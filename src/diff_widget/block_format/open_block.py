from PySide6.QtGui import QColor, QTextBlockFormat


class OpenBlockTextBlockFormat(QTextBlockFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setBackground(QColor(65, 71, 74))

        self.setLeftMargin(0)
        self.setRightMargin(0)
        self.setRightMargin(0)
        self.setBottomMargin(0)
