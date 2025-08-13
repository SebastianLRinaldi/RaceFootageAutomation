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
    valueChanged = pyqtSignal(tuple)  # Emits (R, G, B)

    def __init__(self, parent=None):
        super().__init__(parent)

        self.rgb = None

        self.button = QPushButton("Pick Color")
        self.button.clicked.connect(self.open_dialog)

        self.label = QLabel()

        # Option 1: using stylesheet
        self.label.setStyleSheet(f"background-color: rgb{self.rgb};")


        layout = QHBoxLayout(self)
        layout.addWidget(self.button)
        layout.addWidget(self.label)
        self.setLayout(layout)

        self.valueChanged.connect(self.update_label_color)

        

    def open_dialog(self):
        dialog = QColorDialog(self)
        dialog.colorSelected.connect(self._color_selected)
        dialog.exec()  # Modal, will emit colorSelected

    def _color_selected(self, color):
        self.rgb = (color.red(), color.green(), color.blue())
        self.valueChanged.emit(self.rgb)  # Send tuple directly
        # print("Selected RGB:", self.rgb)

    def update_label_color(self, rgb):
        self.label.setStyleSheet(f"background-color: rgb{rgb};")

    def value(self):
        return self.rgb

    def setValue(self, rgb):
        self.rgb = rgb
        self.update_label_color(rgb)


