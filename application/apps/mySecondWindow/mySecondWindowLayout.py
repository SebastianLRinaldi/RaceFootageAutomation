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

from application.FrontEnd.C_Grouper.SpliterGroupConfiguration import *
from application.FrontEnd.C_Grouper.TabGroupConfigureation import *
from application.FrontEnd.C_Grouper.widgetGroupFrameworks import *

from application.FrontEnd.D_WindowFolder.windowConfigureation import *


"""
https://www.youtube.com/watch?v=Q2d1tYvTjRw
https://www.blackmagicdesign.com/products/davinciresolve
https://www.mltframework.org
text timers - https://www.youtube.com/watch?v=__CJ20RQUlY
keyframes - https://www.youtube.com/watch?v=vcnsA38xDx4
"""


class My_Second_Page(LayoutManager):
    def __init__(self):
        super().__init__()
        
        self.canvas = QLabel(text="Canvas")
        self.mainVideo = QLabel(text="Canvas")
        self.overlayVideo = QLabel(text="Canvas")
        self.lapTimerElement = QLabel(text="Canvas")
        self.labTableElement = QLabel(text="Canvas")
        
        self.overlayOffsetTime = QLabel(text="Canvas")
        
        self.videoStartTime = QLabel(text="Addtional Time to keep before race start")
        self.raceStartTime = QLabel(text="Canvas")
        
        self.raceEndTime = QLabel(text="Canvas")
        self.videoEndTime = QLabel(text="Addtional Time to keep after race ends")

        self.markedTimeline = QLabel(text="Canvas")
        
        self.playBtn = QPushButton("Play/Pause")
        self.skipFwdBtn = QPushButton(">> 5s")
        self.skipBackBtn = QPushButton("<< 5s")
        self.stepFwdBtn = QPushButton("Frame →")
        self.stepBackBtn = QPushButton("← Frame")


        
        middleSplit = MasterSpliterGroup(orientation=Qt.Orientation.Vertical)
        labelsGroup = WidgetGroup(title="Random Labels")
        btnsGroup = WidgetGroup(title="Random Btns")
        
        self.add_widgets_to_window(

        )
