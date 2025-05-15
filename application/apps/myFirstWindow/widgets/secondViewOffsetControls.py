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

        
        setOverlayOffsetSubmitGroup = WidgetGroup(title="Overlay Offset Time Submit")
        self.overlayOffsetTimeInput = QLineEdit()
        self.setOverlayOffsetTimeBtn = QPushButton("Submit Overlay Offset Time")

        offsetControls = WidgetGroup(title="Offset Controls")
        self.offsetFwdBtn = QPushButton("Overlay +0.1s")
        self.offsetBackBtn = QPushButton("Overlay -0.1s")


        self.add_widgets_to_window(
            
            offsetControls.add_widgets_to_group(
                        self.offsetBackBtn,
                        self.offsetFwdBtn,
                        setlayout="H"
                        ),


            setOverlayOffsetSubmitGroup.add_widgets_to_group(
                    self.setOverlayOffsetTimeBtn,
                    self.overlayOffsetTimeInput,
                    setlayout="H"
                ),

        )