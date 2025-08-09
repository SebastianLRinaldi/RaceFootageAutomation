from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import sys
import subprocess

from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()


    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self, "Open Video File", "", "Video Files (*.mp4 *.mov *.mkv)")
        if file_path:
            self.run_ffprobe(file_path)

    def run_ffprobe(self, file_path):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_streams", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.ui.output.setPlainText(result.stdout)
        except subprocess.CalledProcessError as e:
            self.ui.output.setPlainText(f"ffprobe error:\n{e.stderr}")