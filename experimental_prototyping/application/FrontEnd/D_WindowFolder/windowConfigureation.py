from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from typing import Dict, TypeVar, Union

class LayoutManager(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("My Progressive FlashCards")
        self.resize(1000, 600)
        self.setup_stylesheets()

    def add_widgets_to_window(self, *widgets, setlayout:str=None):
        if setlayout == "V" or setlayout == None:
            layout = QVBoxLayout()
            for index, widget in enumerate(widgets):
                layout.addWidget(widget)
            self.setLayout(layout)

        elif setlayout == "H":
            layout = QHBoxLayout()
            for index, widget in enumerate(widgets):
                layout.addWidget(widget)
            self.setLayout(layout)
            
        return self

    def show_window(self):
        self.show()

    def setup_stylesheets(self):
        self.setStyleSheet("""
            QMainWindow {
                background-color: #1a0d1c;
            }
            QLabel {
                background-color: #AAAAAA;
            }
        """)
        