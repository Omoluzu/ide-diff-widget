from PySide6.QtGui import QColor, QTextBlockFormat


class SimpleTextBlockFormat(QTextBlockFormat):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.setBackground(QColor(36, 41, 46))

        self.setLeftMargin(0)
        self.setRightMargin(0)
        self.setRightMargin(0)
        self.setBottomMargin(0)
