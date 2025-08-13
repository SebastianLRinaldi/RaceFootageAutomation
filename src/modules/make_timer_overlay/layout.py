from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *


class Layout(UiManager):

    status_label: QLabel
    generate_button: QPushButton

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
    lap_fill_color_input : ColorSelector
    timer_fill_color_input : ColorSelector
    stats_fill_color_input : ColorSelector

    file_tree: QTreeView
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_properties()
        self.set_widgets()


        layout_data = [
            self.tabs(tab_labels=["Timer Creation", "Files", "Settings"], children=[
                # Main tab
                self.group("vertical", [
                    "status_label",
                    "generate_button"
                ]),

                self.box("vertical","Files", ["file_tree"]),

                # Settings tab
                self.scroll([
                    self.group("vertical", [
                        self.box("vertical", "Video Settings", [
                            self.form([
                                ("Width", "width_input"),
                                ("Height", "height_input"),
                                ("FPS", "fps_input"),
                                ("Use GPU", "use_gpu_checkbox"),
                            ])
                        ]),
                        self.box("vertical", "Timing Settings", [
                            self.form([
                                ("Start Duration", "start_duration_input"),
                                ("End Duration", "end_duration_input"),
                            ])
                        ]),
                        self.box("vertical", "Text Style Settings", [
                            self.form([
                                ("Max Time (sec)", self.max_time_input),
                                ("Center Offset", self.center_offset_input),
                                ("Text Spacing", self.spacing_input),
                                ("Lap Fill Color", self.lap_fill_color_input.layout),
                                ("Timer Fill Color", self.timer_fill_color_input.layout),
                                ("Status Fill Color", self.stats_fill_color_input.layout),
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
                    ])
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
        self.width_input.setRange(1, 10000)
        self.height_input.setRange(1, 10000)
        self.fps_input.setRange(1, 240)
        self.fps_input.setDecimals(2)

        self.max_time_input.setRange(0.1, 600)
        self.start_duration_input.setRange(0.0, 120)
        self.end_duration_input.setRange(0.0, 120)

        self.font_size_input.setRange(1, 200)
        self.center_offset_input.setRange(0, 1000)

    def set_widgets(self):
        self.status_label.setText("Click to generate timer overlay")
        self.status_label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.generate_button.setText("Generate Timer Overlay")

        # # Defaults from your logic
        # self.width_input.setValue(800)
        # self.height_input.setValue(600)
        # self.fps_input.setValue(59.94)
        # self.use_gpu_input.setChecked(True)

        # self.max_time_input.setValue(25.0)
        # self.start_duration_input.setValue(5)
        # self.end_duration_input.setValue(15)

        # self.font_path_input.logic.setText("C:/Users/epics/AppData/Local/Microsoft/Windows/Fonts/NIS-Heisei-Mincho-W9-Condensed.TTF")
        # self.font_size_input.setValue(64)
        # self.center_offset_input.setValue(80)

        # self.output_video_input.setText("Timer_Overlay_(6-20-25)-R2.mp4")

