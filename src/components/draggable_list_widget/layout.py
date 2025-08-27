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

from src.core.gui.ui_manager import *
# from src.components import YourNeededLayoutLogicConnection


# class Layout(UiManager):

#     def __init__(self):
#         super().__init__()
#         self.init_widgets()
#         self.set_widgets()

#         layout_data = []

#         self.apply_layout(layout_data)

#     def init_widgets(self):
#         for name, widget_type in self.__annotations__.items():
#             widget = widget_type()
#             setattr(self, name, widget)

#     def set_widgets(self):
#         pass

class Layout(QListWidget):
    def __init__(self):
        super().__init__()
        self.setViewMode(QListWidget.ViewMode.ListMode)
        self.setIconSize(QPixmap(128, 128).size())
        self.setSpacing(5)
        self.setMovement(QListView.Movement.Snap)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.drag_start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_start_pos is None:
            return
        if (event.position().toPoint() - self.drag_start_pos).manhattanLength() >= QApplication.startDragDistance():
            drag_item = self.currentItem()
            if drag_item:
                drag = QDrag(self)
                mime_data = self.model().mimeData(self.selectedIndexes())
                drag.setMimeData(mime_data)
                drag.exec(Qt.DropAction.MoveAction)
        super().mouseMoveEvent(event)






