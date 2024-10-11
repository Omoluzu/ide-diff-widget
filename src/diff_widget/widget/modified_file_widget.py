from PySide6.QtCore import Qt

from .abc_file_widget import ABCFile


class ModifiedFile(ABCFile):
    def draw(self):
        self.layout.addWidget(self.line)
        self.layout.addWidget(self.text_edit)

        self.line.setAlignment(Qt.AlignRight)
