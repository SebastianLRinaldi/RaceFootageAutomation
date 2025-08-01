from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET

class Layout(UiManager):

    btn: QPushButton
    output: QTextEdit

    file_tree: QTreeView
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [

            self.group("vertical", [
                "btn",
                self.box("vertical","Files", ["file_tree"]),
                "output"
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
        self.btn.setText("Select Video File")
        self.output.setReadOnly(True)
