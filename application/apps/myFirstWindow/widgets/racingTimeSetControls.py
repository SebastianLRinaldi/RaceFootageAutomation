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


class RacingTimeSetControls(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Racing Time Set Controls")


        self.currentRaceTimeStartLabel = QLabel("00:00")
        self.currentRaceTimeStartLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.currentRaceTimeStartLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.markRaceStartTime = QPushButton("Start Race Timer")
        self.grabLapTimeDuration = QPushButton("Grab lap Times From A Racer")

        setRaceTimeSubmitGroup = WidgetGroup(title="Set Race Time Submit")
        self.raceStartTimeInput = QLineEdit()
        self.setRaceStartTimeBtn = QPushButton("Submit Race Start Time")


        self.add_widgets_to_window(

            self.currentRaceTimeStartLabel,
            
            self.grabLapTimeDuration,
            self.markRaceStartTime,
            

            setRaceTimeSubmitGroup.add_widgets_to_group(
                self.setRaceStartTimeBtn,
                self.raceStartTimeInput,
                setlayout="H"
            ),


            


        )