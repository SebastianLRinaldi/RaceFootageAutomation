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
            self.tabs(tab_labels=["Chapter Creation", "Settings"], children=[

                self.group("vertical", [
                    "status_label",
                    self.text_area,
                    "generate_button",
                ]),

                self.scroll([
                    self.reset_settings_btn,
                    
                    self.group("vertical", [
                            self.box("vertical", "Video Settings", [
                                    self.form([
                                        ("Start Duration", "start_duration_input"),
          
                                        ("End Duration", "end_duration_input"),
                                    ])
                                ]),
                            
       
                            
                        ])
                    ])
                ]),
    
        ]

        self.apply_layout(component, self)

    def set_properties(self):
        self.fps_input.setRange(0.1, 240.0)
        self.fps_input.setDecimals(2)
        self.start_duration_input.setRange(1, 600)
        self.end_duration_input.setRange(1, 600)


    def set_widgets(self):
        self.status_label.setText("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generate_button.setText("Generate Overlay")











