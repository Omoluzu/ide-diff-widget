from PySide6.QtWidgets import QApplication

from src.diff_widget import widget


def main():
    app = QApplication([])
    window = widget.Diff()
    window.setGeometry(800, 100, 800, 400)
    window.show()
    app.exec()


if __name__ == '__main__':
    main()
