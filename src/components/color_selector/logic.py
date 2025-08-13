from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
from src.helper_functions import *

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui

    # def pick_color(self):
    #     color = QColorDialog.getColor()
    #     if color.isValid():
    #         rgb = (color.red(), color.green(), color.blue())
    #         print("Selected RGB:", rgb)