from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *


from src.core.GUI.UiManager import *

"""
Something to Override a Known widgte
"""
# class ChunkHolder(QListWidget):

#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Chunk Holder")


"""
If you just need another window with complexlayout in the app
"""
# class ChunkInput(UiManager):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Media Controls")


class PathInputWidget(QWidget):
    def __init__(self, initial_path="", parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(initial_path)
        self.browse_button = QPushButton("Browse", self)
        self.browse_button.clicked.connect(self.browse)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.browse_button)

    def browse(self):
        # Customize filter as needed
        path, _ = QFileDialog.getExistingDirectory(self, "Select Directory")  
        # or QFileDialog.getOpenFileName for files
        if path:
            self.line_edit.setText(path)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)