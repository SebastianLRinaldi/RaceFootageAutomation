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


class Layout(UiManager):
    project_list: QListWidget
    open_project_btn: QPushButton
    new_project_btn: QPushButton

    directory_search: PathInputWidgetLayout

    project_tree: QTreeView

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [

            self.splitter(
                "horizontal",
                [
                    self.box("vertical", "Projects",[
                        "project_list",
                        "new_project_btn",
                        "open_project_btn",
                        self.box("horizontal", "Current Directory",["directory_search"]),
                        
                    ]),

                    self.box("vertical", "Project", ["project_tree"]),
                ]),
        ]
        self.apply_layout(layout_data)

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            if isinstance(widget, QListWidget):
                widget.setFlow(QListWidget.Flow.TopToBottom)
            setattr(self, name, widget)


    def set_widgets(self):
        self.new_project_btn.setText("New Project")
        self.open_project_btn.setText("Open Project")





