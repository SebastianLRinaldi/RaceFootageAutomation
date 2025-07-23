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



from src.core.GUI.UiManager import *

from .widgets.customWidget import CustomWidget


class Layout(UiManager):
    
    another_widget:CustomWidget

    label1: QLabel
    label2: QLabel
    label3: QLabel
    label4: QLabel
    label5: QLabel
    list1: QListWidget
    list2: QListWidget
    list3: QListWidget
    list4: QListWidget
    btn1: QPushButton
    btn2: QPushButton
    btn3: QPushButton
    btn4: QPushButton


    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            "another_widget",
                self.box(
                    title="Top Labels",
                    orientation="horizontal",
                    children=["label1", "label2", "label3", "label4", "label5"]
                ),
                self.splitter(
                    orientation="horizontal",
                    children=[
                        self.group(
                            orientation="vertical",
                            children=["list1", "btn1", "btn2"]
                        ),
                        self.group(
                            orientation="vertical",
                            children=["list2", "btn3", "btn4"]
                        ),
                        self.group(
                            orientation="vertical",
                            children=["list3", "list4"]
                        )
                    ]
                )
            ]

        self.apply_layout(layout_data)


    """
        for name, widget_type in self.__annotations__.items():
            setattr(self, name, widget_type())
    """
    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            if isinstance(widget, QListWidget):
                widget.setFlow(QListWidget.Flow.LeftToRight)
                widget.setWrapping(True)
                widget.setResizeMode(QListWidget.ResizeMode.Adjust)
            setattr(self, name, widget)

    def set_widgets(self):
        self.label1.setText("Header 1")
        self.label2.setText("Header 2")
        self.label3.setText("Header 3")
        self.label4.setText("Header 4")
        self.label5.setText("Header 5")

        for i, btn in enumerate([self.btn1, self.btn2, self.btn3, self.btn4], 1):
            btn.setText(f"Button {i}")

        for i, lst in enumerate([self.list1, self.list2, self.list3, self.list4], 1):
            lst.addItems([f"Item {j}" for j in range(5)])






