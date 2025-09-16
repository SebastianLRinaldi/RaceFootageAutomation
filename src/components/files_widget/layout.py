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
            # Selected / Ordered files
            self.box("vertical", "Selected Files", [
                self.files_widget,
            ]),
        ]

        self.apply_layout(layout_data)
        
    def set_widgets(self):
        self.files_widget.setDragEnabled(True)
        self.files_widget.setAcceptDrops(True)
        self.files_widget.setDropIndicatorShown(True)
        self.files_widget.setDragDropMode(QTreeWidget.DragDropMode.InternalMove)
        self.files_widget.setColumnCount(2)
        self.files_widget.setHeaderLabels(["Name", "Full Path"])  
        self.files_widget.setIconSize(QSize(256, 144))