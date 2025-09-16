from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os

from .bundle import Bundle
from src.helper_functions import *

class Logic(Bundle):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component_window = component.layout
        
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