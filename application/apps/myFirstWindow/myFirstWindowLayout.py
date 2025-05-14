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


class My_First_Page(AppLayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dual Video Player with Timer & Table")

        # Create the QVideoWidget
        self.bgVideoWidget = QVideoWidget(self)
        self.overlayVideoWidget = QVideoWidget(self)

        # Create the players
        self.bgPlayer = QMediaPlayer()
        self.overlayPlayer = QMediaPlayer()

        # Set video output to the QVideoWidget
        self.bgPlayer.setVideoOutput(self.bgVideoWidget)
        self.overlayPlayer.setVideoOutput(self.overlayVideoWidget)

        # === Load media ===
        file1 = 'main_bg.mp4'   # Background video
        file2 = 'main_overlay.mp4'   # Overlay video
        self.bgPlayer.setSource(QUrl.fromLocalFile(file1))
        self.overlayPlayer.setSource(QUrl.fromLocalFile(file2))

        # Set up audio outputs if necessary
        self.bgAudio = QAudioOutput()
        self.overlayAudio = QAudioOutput()
        self.bgPlayer.setAudioOutput(self.bgAudio)
        self.overlayPlayer.setAudioOutput(self.overlayAudio)


        # Set minimum size for video widgets
        self.bgVideoWidget.setMinimumSize(225, 120)
        self.overlayVideoWidget.setMinimumSize(225, 120)

        # High-resolution timer for more accurate position tracking
        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()

        # === Timer (top right) ===
        self.ElapsVideoTimer = QLabel("00:00")
        self.ElapsVideoTimer.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.ElapsVideoTimer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Table (bottom right) ===
        self.table = QTableWidget(1, 1)
        self.table.setHorizontalHeaderLabels(['EpicX18 G9'])
        

        # Playback Controls
        self.playBtn = QPushButton("Play/Pause")
        self.skipFwdBtn = QPushButton(">> 5s")
        self.skipBackBtn = QPushButton("<< 5s")
        self.stepFwdBtn = QPushButton("Frame →")
        self.stepBackBtn = QPushButton("← Frame")

        # Offset Controls
        self.offsetFwdBtn = QPushButton("Overlay +0.1s")
        self.offsetBackBtn = QPushButton("Overlay -0.1s")

        # Timelines
        self.mainTimeline = QSlider(Qt.Orientation.Horizontal)
        self.mainTimeline.setRange(0, 1000)
        self.overlayTimeline = QSlider(Qt.Orientation.Horizontal)
        self.overlayTimeline.setRange(0, 1000)

        

        mediaViews = WidgetGroup(title="Media Viewers")
        timeKeeperGroup = WidgetGroup(title="Lap Timer")
        playbackControls = WidgetGroup(title="Playback Controls")
        offsetControls = WidgetGroup(title="Offset Controls")
        timelineControls = WidgetGroup(title="Timeline Controls")

        spliter = MasterSpliterGroup(Qt.Orientation.Vertical)
        mediaViewsSpliter = MasterSpliterGroup()

        mediaControls = WidgetGroup(title="Sync Video and Play Media")
        raceTimeGroup = WidgetGroup(title="Lap Time Setup Controls")
        




        self.raceStartTimeInput = QLineEdit()
        self.overlayOffsetTimeInput = QLineEdit()

        setRaceTimeSubmitGroup = WidgetGroup(title="Set Race Time Submit")
        setOverlayOffsetSubmitGroup = WidgetGroup(title="Overlay Offset Time Submit")
        setTimesGroup = WidgetGroup(title="Set Time Controls")



        
        # Track Times Placement
        self.markRaceStartTime = QPushButton("Start Race Timer")
        self.grabLapTimeDuration = QPushButton("Grab lap Times From A Racer")
        self.setRaceStartTimeBtn = QPushButton("Submit Race Start Time")
        self.setOverlayOffsetTimeBtn = QPushButton("Submit Overlay Offset Time")
        
        self.RaceTimerLabel = QLabel("00:00")
        self.RaceTimerLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.RaceTimerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)
        
        self.LapTimerLabel = QLabel("00:00")
        self.LapTimerLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.LapTimerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        controls = TabHolder()
        


        self.add_widgets_to_window(
            mediaViews.add_widgets_to_group(
                mediaViewsSpliter.add_widgets_to_spliter(
                    self.overlayVideoWidget,
                    self.bgVideoWidget,
                    
                    timeKeeperGroup.add_widgets_to_group(
                        self.RaceTimerLabel,
                        self.LapTimerLabel,
                        self.table,
                    ),
                ),
            ),
            
            controls.add_groups_as_tabs(
                mediaControls.add_widgets_to_group(
                    playbackControls.add_widgets_to_group(
                        self.skipBackBtn,
                        self.skipFwdBtn,
                        self.playBtn,
                        self.stepBackBtn,
                        self.stepFwdBtn,
                        setlayout="H"
                        ),

                    self.ElapsVideoTimer,

                    timelineControls.add_widgets_to_group(

                        self.mainTimeline,
                        self.overlayTimeline,
                        offsetControls.add_widgets_to_group(
                            self.offsetBackBtn,
                            self.offsetFwdBtn,
                            setlayout="H"
                            ),
                        ),
                    ),


                raceTimeGroup.add_widgets_to_group(
                    self.grabLapTimeDuration,
                    self.markRaceStartTime,
                ),

                setTimesGroup.add_widgets_to_group(
                    setRaceTimeSubmitGroup.add_widgets_to_group(
                        self.setRaceStartTimeBtn,
                        self.raceStartTimeInput,
                        setlayout="H"
                        ),
                    setOverlayOffsetSubmitGroup.add_widgets_to_group(
                        self.setOverlayOffsetTimeBtn,
                        self.overlayOffsetTimeInput,
                        setlayout="H"
                    ),
                    
                )

            )
        )


    def resizeEvent(self, event):
        super().resizeEvent(event)
        print(self.size())

        