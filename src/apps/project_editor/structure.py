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
            self.box("horizontal", "Project Info", [
                "project_name_label",
                "project_path_label"
            ]),

            self.tabs(
                tab_labels=[
                    "Data Grabber", 
                    "Segment Overlay", "Table Overlay", "Telemetry Overlay", "Timer Overlay", "End Stats",
                    "Chapters"
                    # "Stream Viewer", "Merge Footage",
                ],
                children=[
                    self.gatherracetimes,
                    self.makesegmentoverlay,
                    self.maketableoverlay,
                    self.maketelemoverlay,
                    self.maketimeroverlay,
                    self.makeendstats,
                    self.makechapters,
                    # self.makestreamviewer,
                    # self.makemergedfootage,
                    
                ]),
        ]
        
        self.apply_layout(component, self)


    def set_widgets(self):
        self.project_name_label.setText("Project: (None)")
        self.project_path_label.setText("Path: (None)")
        self.export_btn.setText("Export")


