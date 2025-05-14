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

        # # === Main (center) video ===
        # self.bgPlayer = QMediaPlayer()
        # self.bgVideoItem = QGraphicsVideoItem()
        # self.bgScene = QGraphicsScene()
        # self.bgScene.addItem(self.bgVideoItem)
        # self.bgView = QGraphicsView(self.bgScene)
        # self.bgView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.bgView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.bgView.setFrameShape(QGraphicsView.Shape.NoFrame)
        # self.bgPlayer.setVideoOutput(self.bgVideoItem)
        # # === Rear (left) video ===
        # self.overlayPlayer = QMediaPlayer()
        # self.overlayItem = QGraphicsVideoItem()
        # self.overlayItem.setZValue(1)
        # self.overlayItem.setScale(0.4)
        # self.bgScene.addItem(self.overlayItem)
        # self.overlayPlayer.setVideoOutput(self.overlayItem)

        
        # # === Main (center) video ===
        # self.bgPlayer = QMediaPlayer()
        # self.bgVideoItem = QGraphicsVideoItem()
        # self.bgScene = QGraphicsScene()
        # self.bgScene.addItem(self.bgVideoItem)
        # self.bgView = QGraphicsView(self.bgScene)
        # self.bgView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.bgView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.bgView.setFrameShape(QGraphicsView.Shape.NoFrame)
        # self.bgView.setMinimumSize(853, 480)
        # self.bgPlayer.setVideoOutput(self.bgVideoItem)
        # # === Rear (left) video ===
        # self.overlayPlayer = QMediaPlayer()
        # self.overlayItem = QGraphicsVideoItem()
        # self.overlayScene = QGraphicsScene()
        # self.overlayScene.addItem(self.overlayItem)
        # self.overlayView = QGraphicsView(self.overlayScene)
        # self.overlayView.setHorizontalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.overlayView.setVerticalScrollBarPolicy(Qt.ScrollBarPolicy.ScrollBarAlwaysOff)
        # self.overlayView.setFrameShape(QGraphicsView.Shape.NoFrame)
        # self.overlayPlayer.setVideoOutput(self.overlayItem)


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

        # # Check if videos are available and playing
        # if not self.bgPlayer.isAvailable():
        #     print("Background video not available.")
        # if not self.overlayPlayer.isAvailable():
        #     print("Overlay video not available.")

        # # === Start playback ===
        # self.bgPlayer.play()
        # self.overlayPlayer.play()


        # self.bgPlayer.errorChanged.connect(self.handle_error)
        # self.overlayPlayer.errorChanged.connect(self.handle_error)





        
        # # === Load media ===
        # file1 = 'main_bg.mp4'   # Background video
        # file2 = 'main_overlay.mp4'   # Overlay video
        # self.bgPlayer.setSource(QUrl.fromLocalFile(file1))
        # self.overlayPlayer.setSource(QUrl.fromLocalFile(file2))
        # self.bgAudio = QAudioOutput()
        # self.overlayAudio = QAudioOutput()
        # self.bgPlayer.setAudioOutput(self.bgAudio)
        # self.overlayPlayer.setAudioOutput(self.overlayAudio)

        # self.bgPlayer.play()
        # self.overlayPlayer.play()


        # High-resolution timer for more accurate position tracking
        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()



        # === Timer (top right) ===
        self.ElapsVideoTimer = QLabel("00:00")
        self.ElapsVideoTimer.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.ElapsVideoTimer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Table (bottom right) ===
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(['Col 1', 'Col 2', 'Col 3'])
        for i in range(5):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"Item {i},{j}"))
        

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

        mediaElements = WidgetGroup(title="Media Elements")
        trackAnaylsis = WidgetGroup(title="Track Anaylsis")
        timeKeeperGroup = WidgetGroup(title="Lap Timer")
        playbackControls = WidgetGroup(title="Playback Controls")
        offsetControls = WidgetGroup(title="Offset Controls")
        timelineControls = WidgetGroup(title="Timeline Controls")


        spliter = MasterSpliterGroup(Qt.Orientation.Vertical)
        mediaToControlsSpliter = MasterSpliterGroup()
        


        self.add_widgets_to_window(

                mediaElements.add_widgets_to_group(

                    mediaToControlsSpliter.add_widgets_to_spliter(
                        self.overlayVideoWidget,
                        self.bgVideoWidget,
                        
                        timeKeeperGroup.add_widgets_to_group(
                            self.table,
                        ),
                    ),
                ),

                trackAnaylsis.add_widgets_to_group(
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
                    )
            
        )


    def resizeEvent(self, event):
        super().resizeEvent(event)
        print(self.size())
    #     size = self.bgView.size()
    #     self.bgVideoItem.setSize(QSizeF(size.width(), size.height()))
    #     self.bgView.fitInView(self.bgVideoItem, Qt.AspectRatioMode.KeepAspectRatioByExpanding)



    # def resizeEvent(self, event):
    #     super().resizeEvent(event)

    #     # Resize and fit background video
    #     size = self.bgView.size()
    #     self.bgVideoItem.setSize(QSizeF(size.width(), size.height()))
    #     self.bgView.fitInView(self.bgVideoItem, Qt.AspectRatioMode.KeepAspectRatioByExpanding)

    #     # # x = 10
    #     # # y = 10
    #     # # self.overlayItem.setPos(x, y)

    #     # raw_rect = self.overlayItem.nativeSize()  # way more reliable than boundingRect
    #     # scale = self.overlayItem.scale()
    #     # overlay_width = raw_rect.width() * scale
    #     # overlay_height = raw_rect.height() * scale

    #     # x = 10
    #     # y = 10
    #     # self.overlayItem.setPos(x, y)
        