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

from src.core.gui.layout_builder import *
from .blueprint import Blueprint

class Structure(LayoutBuilder, Blueprint):

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
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

        self.apply_layout(component, self)
        
    def set_widgets(self):
        self.drive_combo.setEditable(True)
        self.browse_btn.setText("Browse...")
        self.delete_btn.setText("Remove Path")
