# This Python file uses the following encoding: utf-8
import os
from pathlib import Path
import sys

from PySide6.QtWidgets import QApplication, QMainWindow
import PySide6.QtCore as QtCore
from PySide6.QtCore import QFile as QFile
from PySide6.QtUiTools import QUiLoader as QUiLoader

if "PYSIDE_DESIGNER_PLUGINS" not in os.environ:
    PYSIDE_DESIGNER_PLUGINS = os.path.dirname(os.path.realpath(__file__))


class MainWindow(QMainWindow):
    def __init__(self):
        super(MainWindow, self).__init__()
        self.load_ui()

    def load_ui(self):
        loader = QUiLoader()
        path = os.fspath(Path(__file__).resolve().parent / "form.ui")
        ui_file = QFile(path)
        ui_file.open(QFile.ReadOnly)
        loader.load(ui_file, self)
        ui_file.close()


if __name__ == "__main__":
    QtCore.QCoreApplication.setAttribute(QtCore.Qt.AA_ShareOpenGLContexts)
    app = QApplication([])
    widget = MainWindow()
    widget.show()
    sys.exit(app.exec())
