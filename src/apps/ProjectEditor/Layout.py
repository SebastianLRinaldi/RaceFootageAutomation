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



from src.core.GUI.UiManager import *

from src.widgets.GatherRaceTimes.Layout import Layout as GatherRaceTimesLayout
from src.widgets.MakeMergedFootage.Layout import Layout as MakeMergedFootageLayout
from src.widgets.MakeSegmentOverlay.Layout import Layout as MakeSegmentOverlayLayout
from src.widgets.MakeStreamViewer.Layout import Layout as MakeStreamViewerLayout
from src.widgets.MakeTableOverlay.Layout import Layout as MakeTableOverlayLayout
from src.widgets.MakeTelemOverlay.Layout import Layout as MakeTelemOverlayLayout
from src.widgets.MakeTimerOverlay.Layout import Layout as MakeTimerOverlayLayout


class Layout(UiManager):
    project_name_label: QLabel
    project_path_label: QLabel

    # Overlay widgets for 5 overlays
    overlay1_list: QListWidget
    overlay1_preview: QLabel
    add_overlay1_btn: QPushButton
    remove_overlay1_btn: QPushButton
    edit_overlay1_btn: QPushButton
    overlay1_settings_widget: QWidget

    overlay2_list: QListWidget
    overlay2_preview: QLabel
    add_overlay2_btn: QPushButton
    remove_overlay2_btn: QPushButton
    edit_overlay2_btn: QPushButton
    overlay2_settings_widget: QWidget

    overlay3_list: QListWidget
    overlay3_preview: QLabel
    add_overlay3_btn: QPushButton
    remove_overlay3_btn: QPushButton
    edit_overlay3_btn: QPushButton
    overlay3_settings_widget: QWidget

    overlay4_list: QListWidget
    overlay4_preview: QLabel
    add_overlay4_btn: QPushButton
    remove_overlay4_btn: QPushButton
    edit_overlay4_btn: QPushButton
    overlay4_settings_widget: QWidget

    overlay5_list: QListWidget
    overlay5_preview: QLabel
    add_overlay5_btn: QPushButton
    remove_overlay5_btn: QPushButton
    edit_overlay5_btn: QPushButton
    overlay5_settings_widget: QWidget

    # DataGrabber widgets
    datagrabber_controls_list: QListWidget  # or appropriate widget
    datagrabber_preview: QLabel
    datagrabber_action_btn1: QPushButton
    datagrabber_action_btn2: QPushButton
    datagrabber_edit_btn: QPushButton
    datagrabber_settings_widget: QWidget

    # DataViewer widgets
    dataviewer_controls_list: QListWidget  # or appropriate widget
    dataviewer_preview: QLabel
    dataviewer_action_btn1: QPushButton
    dataviewer_action_btn2: QPushButton
    dataviewer_edit_btn: QPushButton
    dataviewer_settings_widget: QWidget

    # Export button
    export_btn: QPushButton

    #######################
    gatherracetimes: GatherRaceTimesLayout
    makemergedfootage: MakeMergedFootageLayout
    makesegmentoverlay: MakeSegmentOverlayLayout
    makestreamviewer: MakeStreamViewerLayout
    maketableoverlay: MakeTableOverlayLayout
    maketelemoverlay: MakeTelemOverlayLayout
    maketimeroverlay: MakeTimerOverlayLayout

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
                    "Data Grabber", "Stream Viewer", "Merge Footage", 
                    "Segment Overlay", "Table Overlay", "Telemetry Overlay", "Timer Overlay", 
                ],
                children=[
                    "gatherracetimes",
                    "makestreamviewer",
                    "makemergedfootage",
                    "makesegmentoverlay",
                    "maketableoverlay",
                    "maketelemoverlay",
                    "maketimeroverlay",
                    
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

        # Overlays (5)
        for i in range(1, 6):
            getattr(self, f"overlay{i}_preview").setText(f"Overlay {i} Preview")
            getattr(self, f"add_overlay{i}_btn").setText("Add")
            getattr(self, f"remove_overlay{i}_btn").setText("Remove")
            getattr(self, f"edit_overlay{i}_btn").setText("Edit")

        # DataGrabber
        self.datagrabber_preview.setText("DataGrabber Preview")
        self.datagrabber_action_btn1.setText("Action 1")
        self.datagrabber_action_btn2.setText("Action 2")
        self.datagrabber_edit_btn.setText("Edit")

        # DataViewer
        self.dataviewer_preview.setText("DataViewer Preview")
        self.dataviewer_action_btn1.setText("Action 1")
        self.dataviewer_action_btn2.setText("Action 2")
        self.dataviewer_edit_btn.setText("Edit")

        # Export button
        self.export_btn.setText("Export")


