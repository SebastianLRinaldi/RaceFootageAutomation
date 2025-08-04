from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
# from src.components import YourNeededLayoutLogicConnection


class Layout(UiManager):
    racer_name_input: QLineEdit
    text_area: QTextEdit
    save_button : QPushButton

    file_tree: QTreeView
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [
            "racer_name_input",
            "text_area",
            "save_button",
            self.box("vertical","Files", ["file_tree"]),
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
        self.racer_name_input.setPlaceholderText("Enter Racer Name...")
        self.save_button.setText("Save to CSV")
        self.text_area.setPlaceholderText("Paste raw lap data here...")
