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
# from src.components import YourNeededLayoutLogicConnection


# class Layout(UiManager):
#     my_btn: QPushButton

#     def __init__(self):
#         super().__init__()
#         self.init_widgets()
#         self.set_widgets()

#         layout_data = ["my_btn"]

#         self.apply_layout(layout_data)

#     def init_widgets(self):
#         annotations = getattr(self.__class__, "__annotations__", {})
#         print(f"annotations: {annotations}")
#         for name, widget_type in annotations.items():
#             widget = widget_type()
#             setattr(self, name, widget)

#     def set_widgets(self):
#         self.my_btn.setText("Click below to generate segment overlay video.")



class Layout(QWidget):
    def __init__(self, initial_path="", parent=None):
        super().__init__(parent)
        self.layout = QHBoxLayout(self)
        self.line_edit = QLineEdit(self)
        self.line_edit.setText(initial_path)
        self.browse_button = QPushButton("Browse", self)
        # self.browse_button.clicked.connect(self.browse)
        self.layout.addWidget(self.line_edit)
        self.layout.addWidget(self.browse_button)

    def browse(self):
        # Customize filter as needed
        path, _ = QFileDialog.getExistingDirectory(self, "Select Directory")  
        # or QFileDialog.getOpenFileName for files
        if path:
            self.line_edit.setText(path)

    def text(self):
        return self.line_edit.text()

    def setText(self, text):
        self.line_edit.setText(text)



