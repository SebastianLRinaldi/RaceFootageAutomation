from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .blueprint import Blueprint
from src.modules import *
from src.components import *
from src.helper_functions import *
from src.helper_classes import *

class Logic(Blueprint):

    def __init__(self, component):
        super().__init__()
        self.component = component
        self._map_widgets(component)


    def update_modules_lap_times(self):
        targets = [
            "gatherracetimes",
            # "makestreamviewer",
            # "makemergedfootage",
            "makesegmentoverlay",
            "maketableoverlay",
            "maketelemoverlay",
            "maketimeroverlay"
        ]


        for name in targets:
            sub_ui = getattr(self.component_window, name)
            if hasattr(sub_ui, "logic") and callable(getattr(sub_ui.logic, "update_lap_times", None)):
                sub_ui.logic.update_lap_times()







