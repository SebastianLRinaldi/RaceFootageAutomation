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

class Layout(UiManager):
    drive_combo: QComboBox
    browse_btn: QPushButton
    delete_btn: QPushButton

    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()
        

        layout_data = [
            # Drive selector row
            self.box("vertical", "Drive Selection", [
                self.group("horizontal", [
                    self.drive_combo,
                    self.browse_btn,
                    ]),
                self.delete_btn,
                ]),
                
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
        self.drive_combo.setEditable(True)
        self.browse_btn.setText("Browse...")
        self.delete_btn.setText("Remove Path")
