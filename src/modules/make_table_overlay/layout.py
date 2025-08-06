from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *


class Layout(UiManager):

    status_label: QLabel
    pick_button: QPushButton
    generate_button: QPushButton
    progress: QProgressBar

    canvas_width_input: QSpinBox
    canvas_height_input: QSpinBox

    padding_top_input: QSpinBox
    padding_bottom_input: QSpinBox
    padding_left_input: QSpinBox
    padding_right_input: QSpinBox

    fps_input: QDoubleSpinBox
    use_gpu_checkbox: QCheckBox

    start_duration_input: QSpinBox
    end_duration_input: QSpinBox

    output_video_file_input: PathInputWidget

    font_path_input: PathInputWidget
    font_size_input: QSpinBox

    status_label: QLabel
    generate_button: QPushButton

    file_tree: QTreeView
    
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
                "pick_button",
                "generate_button",
                "progress"
            ]),

            self.box("vertical","Files", ["file_tree"]),

            self.scroll([
                    self.group("vertical", [
                        self.box("vertical", "Canvas Settings", [
                            self.form([
                                ("Canvas Width", "canvas_width_input"),
                                ("Canvas Height", "canvas_height_input"),
                                ("FPS", "fps_input"),
                                ("Use GPU", "use_gpu_checkbox"),
                                ("Start Duration", "start_duration_input"),
                                ("End Duration", "end_duration_input"),
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
                                ("Output Video File", self.output_video_file_input.layout),
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
        self.canvas_width_input.setMaximum(10000)
        self.canvas_height_input.setMaximum(10000)

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
        self.pick_button.setText("Set Output File")
        self.generate_button.setText("Generate Overlay")
        self.generate_button.setEnabled(False)
        self.progress.setRange(0, 0)
        self.progress.setVisible(False)

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

