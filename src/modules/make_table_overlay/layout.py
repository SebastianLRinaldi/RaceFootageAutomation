from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *


class Layout(UiManager):

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
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_properties()
        self.set_widgets()

        layout_data = [
            self.tabs(tab_labels=["Table Creation", "Files","Settings"], children=[

            
            self.group(orientation="vertical", children=[
                "status_label",
                "progress",
                "generate_button",
            ]),

            self.box("vertical","Files", [self.file_tree.layout]),

            self.scroll([
                self.reset_table_settings,
                    self.group("vertical", [
                        self.box("vertical", "Canvas Settings", [
                            self.form([
                                ("Width", "width_input"),
                                ("Height", "height_input"),
                                ("FPS", "fps_input"),
                                ("Start Duration", "start_duration_input"),
                                ("End Duration", "end_duration_input"),
                                ("Use GPU", "use_gpu_checkbox"),

                            ])
                        ]),

                        self.box("vertical", "Padding Settings", [
                            self.form([
                                ("Top", "padding_top_input"),
                                ("Bottom", "padding_bottom_input"),
                                ("Left", "padding_left_input"),
                                ("Right", "padding_right_input"),
                            ])
                        ]),

                        self.box("vertical", "Output Settings", [
                            self.form([
                                ("Output Video File", self.rendered_file_name),
                            ])
                        ]),

                        self.box("vertical", "Font Settings", [
                            self.form([
                                ("Font Path", self.font_path_input.layout),
                                ("Font Size", "font_size_input"),
                            ])
                        ]),
                    ]),
                ])
            ])
    
        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        annotations = getattr(self.__class__, "__annotations__", {})
        for name, widget_type in annotations.items():
            widget = widget_type()
            setattr(self, name, widget)
            
    def setup_stylesheets(self):
        self.setStyleSheet(""" """)

    def set_properties(self):
        # Reasonable ranges from your config or assumptions
        self.width_input.setMaximum(10000)
        self.height_input.setMaximum(10000)

        self.padding_top_input.setRange(0, 100)
        self.padding_bottom_input.setRange(0, 100)
        self.padding_left_input.setRange(0, 100)
        self.padding_right_input.setRange(0, 100)

        self.fps_input.setRange(0.1, 240.0)
        self.fps_input.setDecimals(2)

        self.start_duration_input.setRange(0, 600)
        self.end_duration_input.setRange(1, 600)

        self.font_size_input.setRange(8, 128)

    def set_widgets(self):
        self.status_label.setText("Ready")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generate_button.setText("Generate Overlay")
        
        self.progress.setFormat("Ready") 
        self.progress.setRange(0, 0)
        self.progress.setVisible(True)
        self.progress.setMinimum(0)
        self.progress.setMaximum(100)  # Percent scale
        self.progress.setValue(0)
        self.progress.setSizePolicy(QSizePolicy.Policy.Expanding, QSizePolicy.Policy.Fixed)
        self.progress.setAlignment(Qt.AlignmentFlag.AlignCenter)
        

        # self.canvas_width_input.setValue(1920)
        # self.canvas_height_input.setValue(1080)

        # self.padding_top_input.setValue(10)
        # self.padding_bottom_input.setValue(10)
        # self.padding_left_input.setValue(10)
        # self.padding_right_input.setValue(10)

        # self.fps_input.setValue(59.94)
        # self.use_gpu_checkbox.setChecked(True)

        # self.start_duration_input.setValue(5)
        # self.end_duration_input.setValue(15)

        # self.output_video_file_input.logic.setText("Table_Overlay_(6-20-25)-R2.mp4")
        # self.font_path_input.logic.setText("C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF")
        # self.font_size_input.setValue(64)

