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

from .widgets.raceTimerViews import RaceTimerView
from .widgets.mediaViews import MediaView
from .widgets.mediaBtnControls import MediaBtnControls
from .widgets.secondViewOffsetControls import SecondViewOffsetControls
from .widgets.racingTimeSetControls import RacingTimeSetControls
from .widgets.mediaTimelineControls import MediaTimeLineControls


class My_First_Page(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dual Video Player with Timer & Table")

        self.myMediaView = MediaView()
        self.myMediaControls = MediaBtnControls()
        self.myTimerKeeperView = RaceTimerView()
        self.myRacingTimeSetControls = RacingTimeSetControls()
        self.mySecondViewOffsetControls = SecondViewOffsetControls()
        self.myMediaTimeline = MediaTimeLineControls()
    
        viewToControlsSpliter = MasterSpliterGroup(Qt.Orientation.Vertical)
        mediaViewsSpliter = MasterSpliterGroup()

        mediaControls = WidgetGroup(title="Sync Video and Play Media")

        controls = TabHolder()
        
        self.add_widgets_to_window(

            viewToControlsSpliter.add_widgets_to_spliter(

                mediaViewsSpliter.add_widgets_to_spliter(
                self.myMediaView,
                self.myTimerKeeperView,
            ),

                controls.add_groups_as_tabs(
                    mediaControls.add_widgets_to_group(
                        self.myMediaControls,
                        self.myMediaTimeline,
                        ),
                        self.myRacingTimeSetControls,
                        self.mySecondViewOffsetControls,
                        
                ),

            )
        )


    def resizeEvent(self, event):
        super().resizeEvent(event)
        print(self.size())

        