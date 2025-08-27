from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import sys
import csv

from .layout import Layout
# from src.components import YourNeededLayoutLogicConnection
from src.helper_functions import *
from src.helper_classes import *



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
        self.project_directory = ProjectDirectory()
        self.raw_lap_times = None
        self.processed_lap_times = None
        self.lap_time_csv_path = None
        self.lap_times = None
        self.lap_time_deltas = None
    

    def process_lap_times(self): 
        self.raw_lap_times = self.ui.text_area.toHtml()
        if isinstance(self.raw_lap_times, str):
            parser = LapDataParser()
            self.processed_lap_times = parser.process_raw_html(self.raw_lap_times)
        else:
            QMessageBox.warning(self.ui, "Bad Data", f"{type(self.raw_lap_times)}")
            
    def save_to_lap_times_to_csv(self):
        self.lap_time_csv_path = os.path.join(
            self.project_directory.module_path,
            f"Lap_Times_{self.project_directory.project_name}.csv"
        )

        filename, _ = QFileDialog.getSaveFileName(
            self.ui,
            "Save Lap Times",
            self.lap_time_csv_path,
            "CSV Files (*.csv);;All Files (*)"
        )
        if filename:
            with open(filename, "w", newline="", encoding="utf-8") as f:
                writer = csv.writer(f)
                writer.writerows(self.processed_lap_times)
            print(f"Saved at Location: {filename}")

    def set_lap_time_data(self):
        set_config_value(self.project_directory.config_path, "lap_time_csv", self.lap_time_csv_path)
        self.lap_times = get_racer_times('EpicX18 GT9', self.lap_time_csv_path)
        set_config_value(self.project_directory.config_path, "lap_time_list", self.lap_times)
        self.lap_time_deltas = best_lap_deltas(self.lap_times)
        
        set_config_value(self.project_directory.config_path, "lap_time_deltas", self.lap_time_deltas)

    def process_and_store_lap_times(self):
        self.process_lap_times()
        self.save_to_lap_times_to_csv()
        self.set_lap_time_data()
        
        


