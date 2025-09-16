import os
import sys
import time
import re

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.helper_functions import *
from .bundle import Bundle

# class Layout(QWidget, Bundle):
#     def __init__(self, initial_path="", parent=None):
#         super().__init__(parent)
#         self.layout = QHBoxLayout(self)
#         self.line_edit = QLineEdit(self)
#         self.line_edit.setText(initial_path)
#         self.browse_button = QPushButton("Browse", self)
#         self.layout.addWidget(self.line_edit)
#         self.layout.addWidget(self.browse_button)


class Layout(UiManager, Bundle):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()
        
        layout_data = [
            self.group("horizontal",
                    [
                        self.line_edit,
                        self.browse_button
                    ])
            
        ]

        self.apply_layout(layout_data)


    def set_widgets(self):
        self.line_edit.setText("")
        self.browse_button.setText("Browse")