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

# class Layout(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.button = QPushButton("Select Color", self)


# class Layout(QWidget):
#     def __init__(self, parent=None):
#         super().__init__(parent)
#         self.layout = QHBoxLayout(self)

#         self.button = QPushButton("Select Color", self)
#         self.layout.addWidget(self.button)

class Layout(QWidget):
    def __init__(self, parent=None):
        super().__init__(parent)

        self.button = QPushButton("Pick Color")

        self.label = QLabel()

        layout = QHBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)


