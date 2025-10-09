from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from multiprocessing import Pool
import os
import subprocess
import tempfile
import cv2
import numpy as np
import math
from math import ceil

from PIL import ImageFont, ImageDraw, Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import traceback
import re
import cProfile

from .blueprint import Blueprint
from src.components import *
from src.helper_functions import *
from src.helper_classes import *



class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic'):
        super().__init__()
        self.logic = logic  # store the Logic instance

    def run(self):
        try:
            self.logic.make_chapters()  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)


class Logic(QObject, Blueprint):
    
    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component = component
        self.project_directory = ProjectDirectory()
        self.chapters_text = ""

        self.fps = 59.94

        self.start_duration = 5
        self.end_duration = 15

        SETTINGS_FIELDS = [
            ("start_duration", self.start_duration_input, self.start_duration),
            ("end_duration", self.end_duration_input, self.end_duration),
        ]
        
        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, target=self, app="make_chapters")


    def generate_overlay(self):
        self.generate_button.setEnabled(False)
        self.status_label.setText("Generating Chapters...")
        self.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.status_label.setText(f"✅ Done")
        self.text_area.setText(self.chapters_text)
        self.generate_button.setEnabled(True)

        print(f"✅ Chapters Complete")


    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.component, "Error", msg)
        self.status_label.setText(f"❌ Failed: {err_type}")
        self.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.generate_button.setEnabled(True)



    def format_timestamp(self, seconds: float) -> str:
        sec = int(seconds)  # floor to whole seconds
        m, s = divmod(sec, 60)
        h, m = divmod(m, 60)
        return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"

    def make_chapters(self, buffer=5, cooldown=10):
        chapters = []
        t = 0

        best_time = min(self.project_directory.lap_times)

        # buffer
        chapters.append((t, "Race Start"))
        t += buffer

        # laps
        for idx, duration in enumerate(self.project_directory.lap_times):
            if duration is best_time:
                chapters.append((t, f"Lap {idx+1} - {duration} - Best"))
            else:
                chapters.append((t, f"Lap {idx+1} - {duration}"))
            t += duration

        chapters.append((t, "Race End"))
        t += cooldown

        # print block
        for sec, title in chapters:
            print(f"{self.format_timestamp(sec)} {title}")
            self.chapters_text = self.chapters_text + f"{self.format_timestamp(sec)} {title}" + "\n" 



    # def make_chapters(self):
    #     avg = sum(self.project_directory.lap_times) / len(self.project_directory.lap_times)
    #     best = min(self.project_directory.lap_times)
    #     worst = max(self.project_directory.lap_times)
    #     diff = worst - best


    