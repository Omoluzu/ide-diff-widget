from collections import namedtuple

from PySide6.QtWidgets import QApplication

from src.diff_widget import widget


Config = namedtuple(
    'Config',
    ['current_file', 'modified_file', 'sequence_percent', 'backlight']
)


def main():

    config = Config(
        current_file=r'files/file1.py',
        modified_file=r'files/file2.py',
        sequence_percent=1,  # Эксперементальная редактировать не рекомендуется
        backlight='.py'
    )

    app = QApplication([])
    window = widget.Diff(config)
    window.setGeometry(800, 100, 800, 400)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
