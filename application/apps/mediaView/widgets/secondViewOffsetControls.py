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

from application.FrontEnd.C_Grouper.SpliterGroupConfiguration import *
from application.FrontEnd.C_Grouper.TabGroupConfigureation import *
from application.FrontEnd.C_Grouper.widgetGroupFrameworks import *

from application.FrontEnd.D_WindowFolder.windowConfigureation import *


class SecondViewOffsetControls(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Second View Offset Controls")


        self.currentOffsetTimeLabel = QLabel("00:00")
        self.currentOffsetTimeLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.currentOffsetTimeLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        

        self.overlayTimeline = QSlider(Qt.Orientation.Horizontal)
        self.overlayTimeline.setRange(0, 1000)
        
        largeJumpOffsetControls = WidgetGroup(title="Large Jump Offsets ")
        mediumJumpOffsetControls = WidgetGroup(title="Medium Jump Offsets ")
        smallJumpOffsetControls = WidgetGroup(title="Small Jump Offsets ")
        
        self.offsetLFwdBtn = QPushButton("Overlay +0.1s")
        self.offsetLBackBtn = QPushButton("Overlay -0.1s")
        self.offsetMFwdBtn = QPushButton("Overlay +0.01s")
        self.offsetMBackBtn = QPushButton("Overlay -0.01s")
        self.offsetSFwdBtn = QPushButton("Overlay +0.001s")
        self.offsetSBackBtn = QPushButton("Overlay -0.001s")


                
        setOverlayOffsetSubmitGroup = WidgetGroup(title="Overlay Offset Time Submit")
        self.overlayOffsetTimeInput = QLineEdit()
        self.setOverlayOffsetTimeBtn = QPushButton("Submit Overlay Offset Time")


        self.add_widgets_to_window(

            self.currentOffsetTimeLabel,

            self.overlayTimeline,

            largeJumpOffsetControls.add_widgets_to_group(
                    self.offsetLBackBtn,
                    self.offsetLFwdBtn,
                    setlayout="H"
                ),
            
            mediumJumpOffsetControls.add_widgets_to_group(
                    self.offsetMBackBtn,
                    self.offsetMFwdBtn,
                    setlayout="H"
                ),

            smallJumpOffsetControls.add_widgets_to_group(
                    self.offsetSBackBtn,
                    self.offsetSFwdBtn,
                    setlayout="H"
                ),

            setOverlayOffsetSubmitGroup.add_widgets_to_group(
                    self.setOverlayOffsetTimeBtn,
                    self.overlayOffsetTimeInput,
                    setlayout="H"
                ),
            
        )