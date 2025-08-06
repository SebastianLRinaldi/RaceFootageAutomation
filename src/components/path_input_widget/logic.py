from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
from src.helpers import *

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        
    def browse(self):
        # Customize filter as needed
        path, _ = QFileDialog.getExistingDirectory(self.ui, "Select Directory")  
        # or QFileDialog.getOpenFileName for files
        if path:
            self.ui.line_edit.setText(path)

    def text(self):
        return self.ui.line_edit.text()

    def setText(self, text):
        self.ui.line_edit.setText(text)