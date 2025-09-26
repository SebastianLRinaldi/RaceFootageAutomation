from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.components import *

class Blueprint:
    status_label: QLabel
    generate_button: QPushButton
    progress: QProgressBar
    reset_segment_settings: QPushButton

    width_input: QSpinBox  # set max > config WIDTH (e.g. 10000)
    height_input: QSpinBox  # set max > config HEIGHT (e.g. 10000)
    fps_input: QDoubleSpinBox  # range 0.1–120.0, decimals=2

    end_duration_input: QSpinBox  # range 1–600 seconds

    font_path_input: PathInputWidget  # file browse with font file filter (.ttf, .otf)
    font_size_input: QSpinBox  # range 8–72

    bar_file_name_input: QLineEdit  # custom widget with QLineEdit + file browse button (filter for video)
    dot_file_name_input: QLineEdit   # same as above
    dot_avi_file_name_input: QLineEdit   # same
    rendered_file_name_input: QLineEdit   # same

    ffmpeg_bin_input: PathInputWidget  # file browse for executable

    file_tree: FilesView

    def _map_widgets(self, source):
        """
        Copy existing widget instances from source to self.
        """
        # source is some object that already has the widgets as attributes
        for name in self.__annotations__:
            setattr(self, name, getattr(source, name))

    def _init_widgets(self):
        """
        Instantiate all widgets defined in type hints.
        Call this manually when you want actual widget instances.
        """
        for name, typ in self.__annotations__.items():
            setattr(self, name, typ())