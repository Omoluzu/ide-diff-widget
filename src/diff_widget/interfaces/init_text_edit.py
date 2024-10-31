from src.diff_widget import widget, block_format


def index_update(func):
    def wrapper(self, *args, **kwargs):
        self.line_index += 1
        return func(self, *args, **kwargs)

    return wrapper


def index_save(func):
    def wrapper(self, *args, **kwargs):
        self.show_lines.append(self.line_index)
        return func(self, *args, **kwargs)

    return wrapper

def show_equals_text(func):
    def wrapper(self, *args, **kwargs):
        if len(self.save_equals_text) >= 3:
            if len(self.save_equals_text[:-3]) > 0:
                self.current.set_text(
                    text="@@ __,__ @@\n", block_format=block_format.OpenBlock()
                )
                self.modified.set_text(
                    text="@@ __,__ @@\n", block_format=block_format.OpenBlock()
                )

            for equal_text in self.save_equals_text[-3:]:
                self.current.set_text(
                    text=equal_text['text'],
                    line_number=equal_text['current_line'],
                    block_format=block_format.Simple()
                )
                self.modified.set_text(
                    text=equal_text['text'],
                    line_number=equal_text['modified_line'],
                    block_format=block_format.Simple()
                )

        elif len(self.save_equals_text) > 0:
            for equal_text in self.save_equals_text:
                self.current.set_text(
                    text=equal_text['text'],
                    line_number=equal_text['current_line'],
                    block_format=block_format.Simple()
                )
                self.modified.set_text(
                    text=equal_text['text'],
                    line_number=equal_text['modified_line'],
                    block_format=block_format.Simple()
                )

        func(self, *args, **kwargs)
        self.save_equals_text = []
        self.change_index = 3
        return

    return wrapper


class InterfacesInitTextEdit:
    """Initiation Text to EditTextEdit and LineTextEdit

    Represents the initial text display interface for the file difference
        comparison widget.
    """

    def __init__(
            self, current_text_edit: 'widget.CurrentFile',
            modified_text_edit: 'widget.ModifiedFile'
    ) -> 'None':
        self.current = current_text_edit
        self.modified = modified_text_edit
        self.save_equals_text: list[dict[str, str]] = []
        self.change_index = 0

        self.line_index = 0  # todo: temp
        self.show_lines: list[int] = []  # todo: temp

    @index_update
    def equals(self, current_line: int, modified_line: int, text: str) -> None:
        """Method for adding unchanged text

        Method for adding text to widgets if it has not been changed.

        :param current_line: LineNumber of text in current file
        :param modified_line: LineNumber of text in modified file
        :param text: Text
        """
        if not self.change_index:
            self.save_equals_text.append({
                "text": text, "current_line": current_line,
                "modified_line": modified_line
            })
            return

        self.current.set_text(
            line_number=current_line, text=text,
            block_format=block_format.Simple())

        self.modified.set_text(
            line_number=modified_line, text=text,
            block_format=block_format.Simple())
        self.change_index -= 1

    @index_save
    @index_update
    @show_equals_text
    def modified(
            self, index1: int, index2: int, text1: str, text2: str
    ) -> None:
        """Method for adding changed text

        Method for adding text to widgets if it has been changed

        :param index1: LineNumber of text in current file
        :param text1: Text in current file
        :param index2: LineNumber of text in modified file
        :param text2: Text in modified file
        """
        self.current.set_text(
            line_number=index1, text=text1.replace('\n', ''),
            block_format=block_format.Simple())

        self.modified.set_text(
            line_number=index2, text=text2.replace('\n', ''),
            block_format=block_format.Simple())

    @index_save
    @index_update
    @show_equals_text
    def remove(self, index: int, text: str) -> None:
        """Метод добавления текста если он был удален после модификации

        :param index: LineNumber of text in current file
        :param text: Text in current file
        """
        self.current.set_text(
            line_number=index, text=text,
            block_format=block_format.Minus())

        self.modified.set_text(block_format=block_format.Diff())

    @index_save
    @index_update
    @show_equals_text
    def added(self, index: int, text: str) -> None:
        """Method of adding text if it was added after modification

        :param index: LineNumber of text in modified file
        :param text: Text in modified file
        """
        self.current.set_text(block_format=block_format.Diff())

        self.modified.set_text(
            line_number=index, text=text,
            block_format=block_format.Plus())
