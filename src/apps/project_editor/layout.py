import os
import sys
import time
import re

import threading
from threading import Thread
from enum import Enum
from queue import Queue
from typing import List
from datetime import timedelta

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *



from src.core.gui.ui_manager import *
from src.components import *
from src.modules import *


class Layout(UiManager):
    project_name_label: QLabel
    project_path_label: QLabel


    # Export button
    export_btn: QPushButton

    #######################
    gatherracetimes: GatherRaceTimes
    # makemergedfootage: MakeMergedFootage
    makesegmentoverlay: MakeSegmentOverlay
    # makestreamviewer: MakeStreamViewer
    maketableoverlay: MakeTableOverlay
    maketelemoverlay: MakeTelemOverlay
    maketimeroverlay: MakeTimerOverlay

    def __init__(self):
        super().__init__()
        self.init_widgets()
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




    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)

    def set_widgets(self):
        self.project_name_label.setText("Project: (None)")
        self.project_path_label.setText("Path: (None)")
        
        self.export_btn.setText("Export")


