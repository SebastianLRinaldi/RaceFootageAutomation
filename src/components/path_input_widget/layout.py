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
from src.helper_functions import *

class Layout(QWidget):
    def __init__(self, initial_path="", parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(initial_path)
        self.browse_button = QPushButton("Browse", self)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.browse_button)




