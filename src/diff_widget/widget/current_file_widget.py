from .abc_file_widget import ABCFile


class CurrentFile(ABCFile):
    def draw(self):
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.line)