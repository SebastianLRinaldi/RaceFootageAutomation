from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .bundle import Bundle

"""
Close methods
Ctrl+k + Ctrl+0

Open Methods 
Ctrl+k + Ctrl+J
"""
class Logic(Bundle):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component_window = component.layout
