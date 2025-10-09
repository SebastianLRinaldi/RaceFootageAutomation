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
            self.tabs(tab_labels=["Segment Creation", "Files", "Settings"], children=[

                self.group("vertical", [
                    "status_label",
                    "progress",
                    "generate_button",
                ]),

                self.box("vertical","Files", [self.file_tree]),

                
                self.scroll([
                    self.reset_settings_btn,
                    
                    self.group("vertical", [
                            self.box("vertical", "Video Settings", [
                                    self.form([
                                        ("Width", "width_input"),
                                        ("Height", "height_input"),
                                        ("FPS", "fps_input"),
                                        ("End Duration", "end_duration_input"),
                                    ])
                                ]),
                            
                            self.box("vertical", "Font Settings", [
                                    self.form([
                                        ("Font Path", self.font_path_input),
                                        ("Font Size", "font_size_input"),
                                    ])
                                ]),
                            
                        ])
                    ])
                ]),
    
        ]

        self.apply_layout(component, self)

    def set_properties(self):
        self.width_input.setMaximum(10000)
        self.height_input.setMaximum(10000)
        self.fps_input.setRange(0.1, 240.0)
        self.fps_input.setDecimals(2)
        self.end_duration_input.setRange(1, 600)
        self.font_size_input.setRange(1, 256)

    def set_widgets(self):
        self.status_label.setText("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generate_button.setText("Generate Overlay")


        self.progress.setFormat("Ready") 
        self.progress.setRange(0, 0)
        self.progress.setVisible(True)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)  # Percent scale
        self.progress.setValue(0)
        self.progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)







