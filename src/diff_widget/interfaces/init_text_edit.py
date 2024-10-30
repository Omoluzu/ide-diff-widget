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


class InterfacesInitTextEdit:
    """Initiation Text to EditTextEdit and LineTextEdit

    Represents the initial text display interface for the file difference
        comparison widget.
    """

    def __init__(
            self, current_text_edit: 'widget.CurrentFile',
            modified_text_edit: 'widget.ModifiedFile'
    ) -> 'None':
        self.__current = current_text_edit
        self.__modified = modified_text_edit

        self.line_index = 0
        self.show_lines: list[int] = []

    @index_update
    def equals(self, index1: int, index2: int, text: str) -> None:
        """Method for adding unchanged text

        Method for adding text to widgets if it has not been changed.

        :param index1: LineNumber of text in current file
        :param index2: LineNumber of text in modified file
        :param text: Text
        """
        text = text.replace('\n', '')
        self.__current.set_text(
            line_number=index1, text=text, block_format=block_format.Simple)

        self.__modified.set_text(
            line_number=index2, text=text, block_format=block_format.Simple)

    @index_save
    @index_update
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
        self.__current.set_text(
            line_number=index1, text=text1.replace('\n', ''),
            block_format=block_format.Simple)

        self.__modified.set_text(
            line_number=index2, text=text2.replace('\n', ''),
            block_format=block_format.Simple)

    @index_save
    @index_update
    def remove(self, index: int, text: str) -> None:
        """Метод добавления текста если он был удален после модификации

        :param index: LineNumber of text in current file
        :param text: Text in current file
        """
        self.__current.set_text(
            line_number=index, text=text.replace('\n', ''),
            block_format=block_format.Minus)

        self.__modified.set_text(block_format=block_format.Diff)

    @index_save
    @index_update
    def added(self, index: int, text: str) -> None:
        """Method of adding text if it was added after modification

        :param index: LineNumber of text in modified file
        :param text: Text in modified file
        """
        self.__current.set_text(block_format=block_format.Diff)

        self.__modified.set_text(
            line_number=index, text=text.replace('\n', ''),
            block_format=block_format.Plus)