from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .blueprint import Blueprint
from src.helper_functions import *

class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self.component = component
        self._map_widgets(component)
        
