from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
from src.helper_functions import *

class Logic(QObject):
    valueChanged = pyqtSignal(str)
    
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui
        self.last_path = ""

        self.file_tree_loader = fileTreeLoader(self.ui.drive_file_tree, "")
        self.file_tree_loader.set_file_filter(["*.mp4"])


    def update_directory(self, path: str):
        self.last_path = path
        self.file_tree_loader.set_directory(self.last_path)
        self.valueChanged.emit(self.last_path)

    def value(self):
        return self.last_path

    def setValue(self, path):
        if path != self.last_path: 
            self.update_directory(path)
        # self.last_path = path
        # self.file_tree_loader.set_directory(self.last_path)



