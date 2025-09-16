from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os

from .blueprint import Blueprint
from src.helper_functions import *

class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self.component = component
        self._map_widgets(component)
        
        
    def browse(self):
        # Customize filter as needed
        path, _ = os.path.normpath(QFileDialog.getExistingDirectory(self.component_window, "Select Directory") ) 
        # or QFileDialog.getOpenFileName for files
        if path:
            self.line_edit.setText(path)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)