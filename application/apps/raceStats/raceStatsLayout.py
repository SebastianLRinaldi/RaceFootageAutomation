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


class RaceStatsLayout(LayoutManager):
    def __init__(self):
        super().__init__()

        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Paste raw lap data here...")

        self.save_button = QPushButton("Save to CSV")
        
        
        self.add_widgets_to_window(
            self.text_area,
            self.save_button,

        )
