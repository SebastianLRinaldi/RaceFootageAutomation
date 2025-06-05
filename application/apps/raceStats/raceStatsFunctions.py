from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import csv
import re

from application.apps.raceStats.raceStatsLayout import RaceStatsLayout

from .functions.lapDataParser import LapDataParser

class RaceStatsLogic:
    def __init__(self, ui: RaceStatsLayout):
        self.ui = ui


    def process_and_save(self, data:str):
        if isinstance(data, str):
            parser = LapDataParser()
            parser.process_and_save_csv(data)
        else:
            print(f"bad data: {type(data)}")
