# This Python file uses the following encoding: utf-8
import os
import sys
from pathlib import Path

import PySide2.QtCore as QtCore
from PySide2.QtCore import QFile as QFile
from PySide2.QtUiTools import QUiLoader as QUiLoader
from PySide2.QtWidgets import QApplication, QMainWindow

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
    sys.exit(app.exec_())
