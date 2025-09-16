from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
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
            self.box("horizontal", "Project Info", [
                "project_name_label",
                "project_path_label"
            ]),

            self.tabs(
                tab_labels=[
                    "Data Grabber", 
                    "Segment Overlay", "Table Overlay", "Telemetry Overlay", "Timer Overlay", 
                    # "Stream Viewer", "Merge Footage",
                ],
                children=[
                    self.gatherracetimes.layout,
                    self.makesegmentoverlay.layout,
                    self.maketableoverlay.layout,
                    self.maketelemoverlay.layout,
                    self.maketimeroverlay.layout,
                    # self.makestreamviewer.layout,
                    # self.makemergedfootage.layout,
                    
                ]),
        ]
        
        self.apply_layout(layout_data)


    def set_widgets(self):
        self.project_name_label.setText("Project: (None)")
        self.project_path_label.setText("Path: (None)")
        self.export_btn.setText("Export")


