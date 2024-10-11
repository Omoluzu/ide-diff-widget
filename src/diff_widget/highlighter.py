from PySide6.QtGui import QSyntaxHighlighter
from PySide6.QtCore import QRegularExpression

from src.diff_widget import text_char_format


class Highlighter(QSyntaxHighlighter):
    def __init__(self, document, backlight: str):
        super().__init__(document)

        self.highlighting_rules = []

        syntax_highlighting = text_char_format.keywords.get(backlight, {})
        for keyword, char_format in syntax_highlighting.items():
            pattern = QRegularExpression(keyword)
            self.highlighting_rules.append((
                pattern, char_format()
            ))

    def highlightBlock(self, text: str) -> None:
        """Highlights the given text block.
        :param text: current text of DiffTextEdit widget
        """
        for pattern, keyword_format in self.highlighting_rules:
            match_iterator = pattern.globalMatch(text)
            while match_iterator.hasNext():
                match = match_iterator.next()

                self.setFormat(
                    match.capturedStart(), match.capturedLength(),
                    keyword_format
                )
