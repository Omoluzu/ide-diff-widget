from PySide6.QtWidgets import QWidget, QTextEdit, QHBoxLayout
from PySide6.QtGui import QTextOption


class ABCFile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)


        self.text_edit = QTextEdit()
        self.text_edit.setWordWrapMode(QTextOption.NoWrap)

        self.line = QTextEdit()
        self.line.setFixedWidth(50)

        self.layout = QHBoxLayout(self)
        self.draw()

    def draw(self):
        pass