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


class MediaBtnControls(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Controls")

        # Playback Controls
        self.playBtn = QPushButton("Play/Pause")
        self.skipFwdBtn = QPushButton(">> 5s")
        self.skipBackBtn = QPushButton("<< 5s")
        self.stepFwdBtn = QPushButton("Frame →")
        self.stepBackBtn = QPushButton("← Frame")

        self.add_widgets_to_window(

            self.skipBackBtn,
            self.skipFwdBtn,
            self.playBtn,
            self.stepBackBtn,
            self.stepFwdBtn,
            setlayout="H"
            
        )