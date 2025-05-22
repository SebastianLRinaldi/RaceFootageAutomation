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


from .markedSliderCustomWidget import MarkedSlider

from application.FrontEnd.D_WindowFolder.windowConfigureation import *



class MediaTimeLineControls(LayoutManager):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Media Controls")

        
        button = QPushButton("Mark This Point")
        button.clicked.connect(lambda: self.mainTimeline.add_mark(self.mainTimeline.value()))
        

        # === Timer ===
        self.ElapsMainVideoTimer = QLabel("00:00")
        self.ElapsMainVideoTimer.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.ElapsMainVideoTimer.setAlignment(Qt.AlignmentFlag.AlignCenter)


        # === Timer ===
        self.ElapsSecondVideoTimer = QLabel("00:00")
        self.ElapsSecondVideoTimer.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.ElapsSecondVideoTimer.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # Timelines
        self.mainTimeline = MarkedSlider(Qt.Orientation.Horizontal)
        self.mainTimeline.setMinimum(0)
        self.mainTimeline.setMaximum(100)
        self.mainTimeline.setFixedHeight(80)
        self.mainTimeline.setRange(0, 1000)

        
        self.overlayTimeline = QSlider(Qt.Orientation.Horizontal)
        self.overlayTimeline.setRange(0, 1000)

        self.add_widgets_to_window(
            button,

            self.ElapsMainVideoTimer,
            self.mainTimeline,
            self.ElapsSecondVideoTimer,
            self.overlayTimeline,

        )


# from PyQt6.QtWidgets import (
#     QApplication, QSlider, QWidget, QVBoxLayout, QPushButton, QStyle
# )
# from PyQt6.QtCore import Qt
# from PyQt6.QtGui import QPainter, QBrush, QColor, QPaintEvent


# self.lap_segments = [
#     {'start': 0, 'end': 85.3, 'color': Qt.green},
#     {'start': 85.3, 'end': 172.6, 'color': Qt.red},
#     ...
# ]

# class LapSlider(QSlider):
#     def __init__(self, orientation, parent=None):
#         super().__init__(orientation, parent)
#         self.setMinimum(0)
#         self.setMaximum(1000)
#         self.lap_segments = []

#     def set_lap_segments(self, segments):
#         self.lap_segments = segments
#         self.update()

#     def _value_to_pixel(self, value: float) -> int:
#         groove_margin = self.style().pixelMetric(QStyle.PixelMetric.PM_SliderLength) // 2
#         available_width = self.width() - groove_margin * 2
#         if self.maximum() == self.minimum():
#             return 0
#         x = groove_margin + int((value - self.minimum()) / (self.maximum() - self.minimum()) * available_width)
#         return x

#     def paintEvent(self, event: QPaintEvent):
#         super().paintEvent(event)
#         painter = QPainter(self)
#         for seg in self.lap_segments:
#             x1 = self._value_to_pixel(seg['start'])
#             x2 = self._value_to_pixel(seg['end'])
#             width = max(1, x2 - x1)
#             color = QColor(seg.get('color', 'black'))
#             y = (self.height() // 2) - 3
#             painter.setBrush(QBrush(color))
#             painter.setPen(Qt.PenStyle.NoPen)
#             painter.drawRect(x1, y, width, 6)
#         painter.end()


# class Window(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("LapSlider Example")
#         self.slider = LapSlider(Qt.Orientation.Horizontal)
#         self.slider.setValue(0)

#         self.button = QPushButton("Add Test Lap")
#         self.button.clicked.connect(self.add_lap)

#         self.laps = []
#         self.last_val = 0
#         self.layout = QVBoxLayout()
#         self.layout.addWidget(self.slider)
#         self.layout.addWidget(self.button)
#         self.setLayout(self.layout)

#     def add_lap(self):
#         current = self.slider.value()
#         if current <= self.last_val:
#             return
#         # Alternate colors for demo
#         color = 'green' if len(self.laps) % 2 == 0 else 'red'
#         self.laps.append({'start': self.last_val, 'end': current, 'color': color})
#         self.last_val = current
#         self.slider.set_lap_segments(self.laps)


# if __name__ == '__main__':
#     import sys
#     app = QApplication(sys.argv)
#     w = Window()
#     w.resize(600, 150)
#     w.show()
#     sys.exit(app.exec())
