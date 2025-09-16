from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import sys
import subprocess

from .bundle import Bundle
from src.components import *
from src.helper_functions import *
from src.helper_classes import *

class Logic(Bundle):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component_window = component.layout
        self.project_directory = ProjectDirectory()


    def open_file_dialog(self):
        file_path, _ = QFileDialog.getOpenFileName(self.component_window, "Open Video File", "", "Video Files (*.mp4 *.mov *.mkv)")
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
            self.output.setPlainText(result.stdout)
        except subprocess.CalledProcessError as e:
            self.output.setPlainText(f"ffprobe error:\n{e.stderr}")