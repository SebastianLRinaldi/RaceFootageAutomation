from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import *
from src.components import *
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

            self.group("vertical", [
                "btn",
                self.box("vertical","Files", [self.file_tree]),
                "output"
            ])
    
        ]

        self.apply_layout(component, self)
            
    def setup_stylesheets(self):
        self.setStyleSheet(""" """)

    def set_widgets(self):
        self.btn.setText("Select Video File")
        self.output.setReadOnly(True)
