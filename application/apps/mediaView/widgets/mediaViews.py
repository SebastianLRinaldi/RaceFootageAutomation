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


class MediaView(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dual Media Video Player")

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
        # file1 = 'main_bg.mp4'   # Background video
        # file2 = 'main_overlay.mp4'   # Overlay video

        file1 = r'outputFiles\merged_output(5-23-25)-R2.mp4'
        file2 = r'overlays\segment_overlay1.mp4'
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



        mediaViewsSpliter = MasterSpliterGroup()


        self.add_widgets_to_window(
            mediaViewsSpliter.add_widgets_to_spliter(
                    self.overlayVideoWidget,
                    self.bgVideoWidget,
            )
        )
            