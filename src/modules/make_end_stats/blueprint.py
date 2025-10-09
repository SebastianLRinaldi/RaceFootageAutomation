from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.components import *

class Blueprint:
    status_label: QLabel
    generate_button: QPushButton
    progress: QProgressBar

    reset_settings_btn: QPushButton

    # Video settings
    width_input: QSpinBox
    height_input: QSpinBox
    fps_input: QDoubleSpinBox
    use_gpu_checkbox: QCheckBox
    

    # Timing settings
    start_duration_input: QDoubleSpinBox
    end_duration_input: QDoubleSpinBox

    rendered_file_name: QLineEdit

    # Font/text settings
    font_path_input: PathInputWidget
    font_size_input: QSpinBox
    

    max_time_input: QDoubleSpinBox
    center_offset_input: QSpinBox
    spacing_input : QSpinBox

    stats_fill_color_input : ColorSelector

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