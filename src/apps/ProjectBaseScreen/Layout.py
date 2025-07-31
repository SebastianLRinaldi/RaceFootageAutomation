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




"""

"""





class Layout(UiManager):
    project_root_label: QLabel
    project_root_input: QLineEdit
    browse_root_btn: QPushButton

    project_list: QListWidget
    open_project_btn: QPushButton
    new_project_btn: QPushButton

    overlay_list: QListWidget
    asset_list: QListWidget
    template_list: QListWidget

    add_overlay_btn: QPushButton
    add_asset_btn: QPushButton
    add_template_btn: QPushButton

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.box(
                "horizontal",
                "Project Root",
                ["project_root_label", "project_root_input", "browse_root_btn"]
            ),
            self.splitter(
                "horizontal",
                [
                    self.group("vertical", [
                        "project_list",
                        "new_project_btn",
                        "open_project_btn"
                    ]),
                    self.group("vertical", [
                        self.box("vertical", "Overlays", ["overlay_list", "add_overlay_btn"]),
                        self.box("vertical", "Assets", ["asset_list", "add_asset_btn"]),
                        self.box("vertical", "Templates", ["template_list", "add_template_btn"]),
                    ])
                ]
            )
        ]
        self.apply_layout(layout_data)

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            if isinstance(widget, QListWidget):
                widget.setFlow(QListWidget.Flow.TopToBottom)
            setattr(self, name, widget)

    def set_widgets(self):
        self.project_root_label.setText("Project Directory:")
        self.browse_root_btn.setText("Browse")

        self.new_project_btn.setText("New Project")
        self.open_project_btn.setText("Open Project")

        self.add_overlay_btn.setText("Add Overlay")
        self.add_asset_btn.setText("Add Asset")
        self.add_template_btn.setText("Add Template")

        self.project_list.addItems(["Project A", "Project B"])
        self.overlay_list.addItems(["Overlay 1", "Overlay 2"])
        self.asset_list.addItems(["Image.png", "Sound.wav"])
        self.template_list.addItems(["Template X", "Template Y"])






