from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *
from .bundle import Bundle

class Layout(UiManager, Bundle):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()

        layout_data = [

            self.group("vertical", [
                "btn",
                self.box("vertical","Files", [self.file_tree.layout]),
                "output"
            ])
    
        ]

        self.apply_layout(layout_data)
            
    def setup_stylesheets(self):
        self.setStyleSheet(""" """)

    def set_widgets(self):
        self.btn.setText("Select Video File")
        self.output.setReadOnly(True)
