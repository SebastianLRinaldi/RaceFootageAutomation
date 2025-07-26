from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

# from .widgets.CUSTOMWIDGET import YOURWIDGET

class Layout(UiManager):

    status_label: QLabel
    pick_button: QPushButton
    generate_button: QPushButton
    progress: QProgressBar
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [
            self.group(orientation="vertical", children=[
                "status_label",
                "pick_button",
                "generate_button",
                "progress"
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
        self.status_label.setText("Ready")
        self.pick_button.setText("Set Output File")
        self.generate_button.setText("Generate Overlay")
        self.generate_button.setEnabled(False)
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)
