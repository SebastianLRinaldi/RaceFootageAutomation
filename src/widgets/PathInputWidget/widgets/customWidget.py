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
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *



from src.core.GUI.UiManager import *


class CustomWidget(UiManager):

    label: QLabel
    list: QListWidget
    btn: QPushButton
    label1: QLabel
    list2: QListWidget
    btn3: QPushButton


    def __init__(self):
        super().__init__()

        self.init_widgets()
        # self.resize(1000, 600)
        
        self.setWindowTitle("Custom Widget")
        self.label.setText("Custom Header Label")
        self.btn.setText("Action")

        # self.layout().setContentsMargins(0, 0, 0, 0)



    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            setattr(self, name, widget_type())

        layout_data = [
            "label",
            self.group(children=["list", "btn"]),
            self.box(children=["list2", "btn3"]),
        ]

        self.apply_layout(layout_data)


        self.print_margins_recursive(self)





