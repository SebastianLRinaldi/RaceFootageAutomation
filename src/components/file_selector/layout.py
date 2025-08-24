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


# from PyQt6.QtWidgets import (
#     QWidget, QVBoxLayout, QHBoxLayout, QComboBox, QPushButton,
#     QFileDialog, QMessageBox
# )
# import os


# class DriveSelector(QWidget):
#     valueChanged = pyqtSignal(list)
    
#     def __init__(self):
#         super().__init__()

#         layout = QVBoxLayout(self)

#         # combo box allows typing
#         self.drive_combo = QComboBox()
#         self.drive_combo.setEditable(True)
#         layout.addWidget(self.drive_combo)

#         # buttons row
#         btn_row = QHBoxLayout()
#         self.browse_btn = QPushButton("Browse...")
#         self.delete_btn = QPushButton("Delete Selected")
#         btn_row.addWidget(self.browse_btn)
#         btn_row.addWidget(self.delete_btn)
#         layout.addLayout(btn_row)

#         # connections
#         self.browse_btn.clicked.connect(self.browse_directory)
#         self.delete_btn.clicked.connect(self.delete_selected)

#     def browse_directory(self):
#         path = QFileDialog.getExistingDirectory(self, "Select Directory")
#         if path:
#             self.add_directory(path)

#     def add_directory(self, path: str):
#         if not path.strip():  # ignore empty or whitespace-only
#             return
        
#         if not os.path.isdir(path):
#             QMessageBox.warning(self, "Invalid Directory", f"Path does not exist:\n{path}")
#             return

#         # avoid duplicates
#         if path not in [self.drive_combo.itemText(i) for i in range(self.drive_combo.count())]:
#             self.drive_combo.addItem(path)
#         self.drive_combo.setCurrentText(path)

#         self.directories = self.get_all_directories()
#         self.valueChanged.emit(self.directories)

#     def delete_selected(self):
#         idx = self.drive_combo.currentIndex()
#         if idx >= 0:
#             self.drive_combo.removeItem(idx)

#     def delete_all_directories(self):
#         """Remove all saved directories."""
#         self.drive_combo.clear()

#     def get_current_directory(self) -> str:
#         return self.drive_combo.currentText()

#     def get_all_directories(self) -> list[str]:
#         """Return all saved paths in the combo box."""
#         return [self.drive_combo.itemText(i) for i in range(self.drive_combo.count())]


#     def value(self):
#         return self.directories 

#     def setValue(self, directories):
#         self.directories = directories
#         self.delete_all_directories()
#         for path in directories:
#             self.add_directory(path)









class Layout(UiManager):
    selected_files : QListWidget
    drive_file_tree: QTreeView
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [
            
            # # Drive selector row
            # self.box("vertical", "Drive Selection", [
            #     self.drive_selector,
            #     ]),
                
            self.group("horizontal", [
                    # Selected / Ordered files
                    self.box("vertical", "Selected Files", [
                        self.selected_files,
                    ]),
                    # Available files
                    self.box("vertical", "Available Files", [

                        self.drive_file_tree
                    ]),
                ]),

        ]


        self.apply_layout(layout_data)

    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)
            
    def setup_stylesheets(self):
        self.setStyleSheet(""" """)
        
    def set_widgets(self):
        pass
        # --- Drive selection ---
        # self.drive_combo.addItems(["C:/", "D:/", "E:/"])   # example drives



        # # --- Optional sizing / behavior ---
        # self.available_files.setSelectionMode(QListWidget.SelectionMode.ExtendedSelection)
        # self.selected_files.setSelectionMode(QListWidget.SelectionMode.SingleSelection)


# import sys
# import os
# from PyQt6.QtWidgets import (
#     QApplication, QWidget, QVBoxLayout, QHBoxLayout,
#     QLabel, QComboBox, QListWidget, QPushButton,
#     QListWidgetItem, QSpinBox
# )
# from PyQt6.QtCore import Qt


# class FileSelector(QWidget):
#     def __init__(self):
#         super().__init__()
#         self.setWindowTitle("Drive File Selector")

#         layout = QVBoxLayout(self)

#         # --- Drive selector ---
#         drive_layout = QHBoxLayout()
#         drive_layout.addWidget(QLabel("Select Drive:"))
#         self.drive_combo = QComboBox()
#         # Dummy drives for demo (on Windows you'd list A:/, C:/, etc.)
#         self.drive_combo.addItems(["C:/", "D:/", "E:/"])
#         drive_layout.addWidget(self.drive_combo)
#         load_btn = QPushButton("Load Files")
#         drive_layout.addWidget(load_btn)
#         layout.addLayout(drive_layout)

#         # --- File list from drive ---
#         self.file_list = QListWidget()
#         layout.addWidget(QLabel("Available Files:"))
#         layout.addWidget(self.file_list)

#         # --- Selected file order ---
#         layout.addWidget(QLabel("Selected Files (with order):"))
#         self.selected_list = QListWidget()
#         layout.addWidget(self.selected_list)

#         # --- Connections ---
#         load_btn.clicked.connect(self.load_files)
#         self.file_list.itemDoubleClicked.connect(self.add_file)

#     def load_files(self):
#         self.file_list.clear()
#         drive_path = self.drive_combo.currentText()
#         # Fake files for demo
#         files = ["file1.txt", "file2.png", "file3.mp3"]
#         for f in files:
#             self.file_list.addItem(f)

#     def add_file(self, item):
#         widget = QWidget()
#         h = QHBoxLayout()
#         h.setContentsMargins(0, 0, 0, 0)

#         label = QLabel(item.text())
#         spin = QSpinBox()
#         spin.setMinimum(1)
#         spin.setValue(self.selected_list.count() + 1)

#         h.addWidget(label)
#         h.addWidget(spin)
#         widget.setLayout(h)

#         lw_item = QListWidgetItem()
#         lw_item.setSizeHint(widget.sizeHint())
#         self.selected_list.addItem(lw_item)
#         self.selected_list.setItemWidget(lw_item, widget)


# if __name__ == "__main__":
#     app = QApplication(sys.argv)
#     w = FileSelector()
#     w.resize(400, 500)
#     w.show()
#     sys.exit(app.exec())
