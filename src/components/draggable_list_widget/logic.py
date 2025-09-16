from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .bundle import Bundle
from src.helper_functions import *

class Logic(Bundle):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)


        