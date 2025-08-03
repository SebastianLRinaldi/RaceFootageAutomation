from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import sys

from .layout import Layout
from src.components import *
from src.helpers import *



"""
https://www.youtube.com/watch?v=Q2d1tYvTjRw
https://www.blackmagicdesign.com/products/davinciresolve
https://www.mltframework.org
text timers - https://www.youtube.com/watch?v=__CJ20RQUlY
keyframes - https://www.youtube.com/watch?v=vcnsA38xDx4
"""


class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
    

    def process_and_save(self, data:str):
        if isinstance(data, str):
            parser = LapDataParser()
            parser.process_and_save_csv(data)
        else:
            QMessageBox.warning(self.ui, "Bad Data", f"{type(data)}")

    def get_lap_times(self):
        times = get_racer_times( 'EpicX18 GT9')
        return times