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


class RaceTimerView(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("LapTimes and Race Timer View")


        # === Table (bottom right) ===
        self.table = QTableWidget(1, 1)
        self.table.setHorizontalHeaderLabels(['EpicX18 G9'])

        self.RaceTimerLabel = QLabel("00:00")
        self.RaceTimerLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.RaceTimerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.LapTimerLabel = QLabel("00:00")
        self.LapTimerLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.LapTimerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)


        self.add_widgets_to_window(

            self.RaceTimerLabel,
            self.LapTimerLabel,
            self.table,

        )