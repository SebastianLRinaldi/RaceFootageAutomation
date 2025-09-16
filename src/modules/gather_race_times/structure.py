from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import *
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()

        self.layout_data = [
            "racer_name_input",
            "text_area",
            "save_button",
            self.box("vertical","Files", [self.file_tree]),
        ]

        self.apply_layout(component, self)

    def set_widgets(self):
        self.racer_name_input.setPlaceholderText("Enter Racer Name...")
        self.save_button.setText("Save to CSV")
        self.text_area.setPlaceholderText("Paste raw lap data here...")
