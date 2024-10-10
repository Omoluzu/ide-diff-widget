from abc import abstractmethod

from PySide6.QtWidgets import QWidget, QHBoxLayout


from src.diff_widget import text_edit


class ABCFile(QWidget):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        self.text_edit = text_edit.Edit()
        self.line = text_edit.Line()

        self.layout = QHBoxLayout(self)
        self.draw()

    @abstractmethod
    def draw(self):
        pass

    def scaled_font_size(self, new_font_size: int) -> None:
        """Scaled font size current Widget and update width size widget
        :param new_font_size: new size
        """
        self.text_edit.scaled_font_size(new_font_size)
        self.line.scaled_font_size(new_font_size)

    def set_text(self, line_number: str, text: str, color=None) -> None:
        """Set text TextWidget and set line number and color
        :param line_number: line number
        :param text: added text
        :param color: color text
        """
        self.text_edit.append(text)
        self.line.append(line_number)
