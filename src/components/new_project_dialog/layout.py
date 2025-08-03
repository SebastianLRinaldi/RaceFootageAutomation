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


class Layout(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")

        self.date_input = QLineEdit()
        self.run_input = QLineEdit()
        self.create_btn = QPushButton("Create")
        self.cancel_btn = QPushButton("Cancel")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Date (MM-DD-YY):"))
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Run ID (e.g. R1, R2, Enduro):"))
        layout.addWidget(self.run_input)

        btns = QHBoxLayout()
        btns.addWidget(self.create_btn)
        btns.addWidget(self.cancel_btn)
        layout.addLayout(btns)

        self.setLayout(layout)





