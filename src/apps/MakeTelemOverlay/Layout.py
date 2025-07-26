from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET

class Layout(UiManager):

    label: QLabel
    file_list: QListWidget
    button_add: QPushButton
    button_generate: QPushButton
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [
            self.group("vertical", [
                "label",
                "file_list",
                "button_add",
                "button_generate"
            ])
    
        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)
            
    def setup_stylesheets(self):
        self.setStyleSheet(""" """)

    def set_widgets(self):
        self.label.setText("Queued files:")
        self.button_add.setText("Add GPX File")
        self.button_generate.setText("Generate All Overlays")
