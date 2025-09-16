from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.components import *

class Blueprint:
    status_label: QLabel
    generate_button: QPushButton
    progress: QProgressBar

    width_input: QSpinBox
    height_input: QSpinBox

    padding_top_input: QSpinBox
    padding_bottom_input: QSpinBox
    padding_left_input: QSpinBox
    padding_right_input: QSpinBox

    fps_input: QDoubleSpinBox
    use_gpu_checkbox: QCheckBox

    start_duration_input: QSpinBox
    end_duration_input: QSpinBox

    rendered_file_name: QLineEdit

    font_path_input: PathInputWidget
    font_size_input: QSpinBox

    status_label: QLabel
    generate_button: QPushButton
    reset_table_settings: QPushButton

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