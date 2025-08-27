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


import sys, json, os
MARKS_FILE = "marks.json"

class MarkedSlider(QSlider):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.custom_marks = {}  # dict of dicts keyed by name

        self.setTickPosition(QSlider.TickPosition.TicksBelow)
        self.setTickInterval(10)

        self.load_marks()
        self.setMouseTracking(True)

    def add_mark(self, value):
        name = f'Mark {value}'
        if name in self.custom_marks:
            return

        mark = {
            'value': value,
            'name': name,
            'note': '',
            'color': '#FF0000',
            'timestamp': float(time.time())
        }
        self.custom_marks[name] = mark
        self.save_marks()
        self.update()

    def delete_mark(self, name):
        if name in self.custom_marks:
            del self.custom_marks[name]
            self.save_marks()
            self.update()

    def remove_mark_near(self, pixel_x):
        for name, mark in list(self.custom_marks.items()):
            if abs(self._value_to_pixel(mark['value']) - pixel_x) < 5:
                del self.custom_marks[name]
                self.save_marks()
                self.update()
                break

    def edit_mark_near(self, pixel_x):
        for name, mark in self.custom_marks.items():
            if abs(self._value_to_pixel(mark['value']) - pixel_x) < 5:
                self._open_edit_dialog(name, mark)
                break

    def _open_edit_dialog(self, name, mark):
        new_name, ok = QInputDialog.getText(self, "Edit Mark Name", "Name:", text=mark['name'])
        if not ok or not new_name:
            return

        note, ok = QInputDialog.getMultiLineText(self, "Edit Mark Note", "Note:", text=mark['note'])
        if not ok:
            return

        color = QColorDialog.getColor(QColor(mark['color']), self, "Choose Mark Color")
        if not color.isValid():
            return

        # Remove old if name changes
        if new_name != name:
            del self.custom_marks[name]

        self.custom_marks[new_name] = {
            **mark,
            'name': new_name,
            'note': note,
            'color': color.name()
        }
        self.save_marks()
        self.update()

    def mousePressEvent(self, event: QMouseEvent):
        pixel_x = event.position().x()
        if event.button() == Qt.MouseButton.RightButton:
            for name, mark in self.custom_marks.items():
                if abs(self._value_to_pixel(mark['value']) - pixel_x) < 5:
                    choice = QMessageBox.question(
                        self, "Mark Options",
                        f"Mark: {name}\n\nChoose action:",
                        QMessageBox.StandardButton.Cancel |
                        QMessageBox.StandardButton.Yes |  # Edit
                        QMessageBox.StandardButton.No    # Delete
                    )
                    if choice == QMessageBox.StandardButton.Yes:
                        self._open_edit_dialog(name, mark)
                    elif choice == QMessageBox.StandardButton.No:
                        self.delete_mark(name)
                    return
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        pos_x = event.position().x()
        for mark in self.custom_marks.values():
            if abs(self._value_to_pixel(mark['value']) - pos_x) < 7 and mark['note']:
                QToolTip.showText(event.globalPosition().toPoint(), mark['note'], self)
                return
        QToolTip.hideText()
        super().mouseMoveEvent(event)

    def paintEvent(self, event):
        super().paintEvent(event)
        painter = QPainter(self)
        painter.setFont(QFont("Arial", 8))

        for mark in self.custom_marks.values():
            x = self._value_to_pixel(mark['value'])
            y = self.height() - 60
            painter.setPen(QColor(mark['color']))
            painter.drawLine(x, y, x, y - 10)
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