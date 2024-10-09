from .abc_file_widget import ABCFile


class CurrentFile(ABCFile):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.text_edit.setReadOnly(True)

    def draw(self):
        self.layout.addWidget(self.text_edit)
        self.layout.addWidget(self.line)
