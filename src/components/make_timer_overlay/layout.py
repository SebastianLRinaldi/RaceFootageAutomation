from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *

class Layout(UiManager):

    label: QLabel
    button: QPushButton

    # Video settings
    width_input: QSpinBox
    height_input: QSpinBox
    fps_input: QDoubleSpinBox
    use_gpu_input: QCheckBox

    # Timing settings
    max_time_input: QDoubleSpinBox
    start_duration_input: QDoubleSpinBox
    end_duration_input: QDoubleSpinBox

    # Font/text settings
    font_path_input: PathInputWidgetLayout
    font_size_input: QSpinBox
    center_offset_input: QSpinBox

    # Output settings
    output_video_input: QLineEdit
    output_temp_input: QLineEdit

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
                    "label",
                    "button"
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
                                ("Use GPU", "use_gpu_input"),
                            ])
                        ]),
                        self.box("vertical", "Timing Settings", [
                            self.form([
                                ("Max Time (sec)", "max_time_input"),
                                ("Start Duration", "start_duration_input"),
                                ("End Duration", "end_duration_input"),
                            ])
                        ]),
                        self.box("vertical", "Text Style Settings", [
                            self.form([
                                ("Font Path", "font_path_input"),
                                ("Font Size", "font_size_input"),
                                ("Center Offset", "center_offset_input"),
                            ])
                        ]),
                        self.box("vertical", "Output Settings", [
                            self.form([
                                ("Final Output Video", "output_video_input"),
                                ("Timer Temp File", "output_temp_input"),
                            ])
                        ])
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
        self.label.setText("Click to generate timer overlay")
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.button.setText("Generate Timer Overlay")

        # Defaults from your logic
        self.width_input.setValue(800)
        self.height_input.setValue(600)
        self.fps_input.setValue(59.94)
        self.use_gpu_input.setChecked(True)

        self.max_time_input.setValue(25.0)
        self.start_duration_input.setValue(5)
        self.end_duration_input.setValue(15)

        self.font_path_input.setText("C:/Users/epics/AppData/Local/Microsoft/Windows/Fonts/NIS-Heisei-Mincho-W9-Condensed.TTF")
        self.font_size_input.setValue(64)
        self.center_offset_input.setValue(80)

        self.output_video_input.setText("Timer_Overlay_(6-20-25)-R2.mp4")
        self.output_temp_input.setText("timer_temp.mp4")
