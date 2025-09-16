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
            self.group("vertical", 
                [
                    self.button,
                    self.label
                    ]),
        ]

        self.apply_layout(layout_data)


    def set_widgets(self):
        self.button.setText("Pick Color")