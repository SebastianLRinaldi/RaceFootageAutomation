from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
# from src.components import YourNeededLayoutLogicConnection
from src.helpers import *

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
