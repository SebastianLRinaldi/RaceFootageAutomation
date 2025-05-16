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

import sys, json, os
MARKS_FILE = "marks.json"

class MarkedSlider(QSlider):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.custom_marks = []  # list of dicts with keys: value, name, note, color

        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setTickInterval(10)

        self.load_marks()

        self.setMouseTracking(True)  # For tooltips

    def add_mark(self, value):
        if any(abs(m['value'] - value) < 1e-5 for m in self.custom_marks):
            return  # Already exists

        mark = {
            'value': value,
            'name': f'Mark {value}',
            'note': '',
            'color': '#FF0000'  # default red
        }
        self.custom_marks.append(mark)
        self.save_marks()
        self.update()

    def remove_mark_near(self, pixel_x):
        for mark in self.custom_marks:
            mark_x = self._value_to_pixel(mark['value'])
            if abs(mark_x - pixel_x) < 5:
                self.custom_marks.remove(mark)
                self.save_marks()
                self.update()
                break

    def edit_mark_near(self, pixel_x):
        for mark in self.custom_marks:
            mark_x = self._value_to_pixel(mark['value'])
            if abs(mark_x - pixel_x) < 5:
                self._open_edit_dialog(mark)
                break

    def _open_edit_dialog(self, mark):
        # Name
        name, ok = QInputDialog.getText(self, "Edit Mark Name", "Name:", text=mark['name'])
        if not ok:
            return
        # Note
        note, ok = QInputDialog.getMultiLineText(self, "Edit Mark Note", "Note:", text=mark['note'])
        if not ok:
            return
        # Color
        color = QColorDialog.getColor(QColor(mark['color']), self, "Choose Mark Color")
        if not color.isValid():
            return

        mark['name'] = name
        mark['note'] = note
        mark['color'] = color.name()

        self.save_marks()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        if event.button() == Qt.MouseButton.RightButton:
            # Show context menu: remove or edit?
            pixel_x = event.position().x()

            # Detect if click is on a mark
            for mark in self.custom_marks:
                mark_x = self._value_to_pixel(mark['value'])
                if abs(mark_x - pixel_x) < 5:
                    # Ask what to do
                    choice = QMessageBox.question(
                        self, "Mark Options",
                        f"Mark: {mark['name']}\n\nChoose action:",
                        QMessageBox.StandardButton.Cancel |
                        QMessageBox.StandardButton.Yes |  # Use Yes for edit
                        QMessageBox.StandardButton.No    # Use No for remove
                    )
                    if choice == QMessageBox.StandardButton.Yes:
                        self._open_edit_dialog(mark)
                    elif choice == QMessageBox.StandardButton.No:
                        self.custom_marks.remove(mark)
                        self.save_marks()
                        self.update()
                    return
            # If no mark nearby, pass event
            super().mousePressEvent(event)
        else:
            super().mousePressEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 8))

        for mark in self.custom_marks:
            x = self._value_to_pixel(mark['value'])
            y = self.height() - 60
            # Draw colored line
            color = QColor(mark['color'])
            painter.setPen(color)
            painter.drawLine(x, y, x, y - 10)
            # Draw name label above line (centered)
            text_width = painter.fontMetrics().horizontalAdvance(mark['name'])
            painter.drawText(QPoint(x - text_width // 2, y - 12), mark['name'])

        painter.end()

    def _value_to_pixel(self, value):
        slider_min = self.minimum()
        slider_max = self.maximum()
        slider_range = slider_max - slider_min

        slider_length = self.style().pixelMetric(QStyle.PixelMetric.PM_SliderLength)
        available_width = self.width() - slider_length
        offset = slider_length // 2

        ratio = (value - slider_min) / slider_range
        return int(offset + ratio * available_width)

    def save_marks(self):
        try:
            with open(MARKS_FILE, "w") as f:
                json.dump(self.custom_marks, f, indent=2)
        except Exception as e:
            print(f"Save failed: {e}")

    def load_marks(self):
        if not os.path.exists(MARKS_FILE):
            return
        try:
            with open(MARKS_FILE, "r") as f:
                self.custom_marks = json.load(f)
        except Exception as e:
            print(f"Load failed: {e}")

    def mouseMoveEvent(self, event):
        # Show tooltip with note if hovering near mark
        pos_x = event.position().x()
        for mark in self.custom_marks:
            mark_x = self._value_to_pixel(mark['value'])
            if abs(mark_x - pos_x) < 7 and mark['note']:
                QToolTip.showText(event.globalPosition().toPoint(), mark['note'], self)
                return
        QToolTip.hideText()
        super().mouseMoveEvent(event)


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