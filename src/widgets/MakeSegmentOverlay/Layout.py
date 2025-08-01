from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

from .widgets.PathInputWidget import PathInputWidget




class Layout(UiManager):

    width_input: QSpinBox  # set max > config WIDTH (e.g. 10000)
    height_input: QSpinBox  # set max > config HEIGHT (e.g. 10000)
    fps_input: QDoubleSpinBox  # range 0.1–120.0, decimals=2

    output_dir_input: PathInputWidget  # custom widget with QLineEdit + directory browse button
    bar_file_input: PathInputWidget  # custom widget with QLineEdit + file browse button (filter for video)
    dot_file_input: PathInputWidget  # same as above
    dot_avi_file_input: PathInputWidget  # same
    segment_overlay_file_input: PathInputWidget  # same

    end_duration_input: QSpinBox  # range 1–600 seconds

    font_path_input: PathInputWidget  # file browse with font file filter (.ttf, .otf)
    font_size_input: QSpinBox  # range 8–72

    ffmpeg_bin_input: PathInputWidget  # file browse for executable

    

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
            self.tabs(tab_labels=["Segment Creation", "Files", "Settings"], children=[

                self.group("vertical", [
                    "status_label",
                    "generate_button",
                    ]),

                self.box("vertical","Files", ["file_tree"]),

                
                self.scroll([
                    self.group("vertical", [
                            self.box("vertical", "Video Settings", [
                                    self.form([
                                        ("Width", "width_input"),
                                        ("Height", "height_input"),
                                        ("FPS", "fps_input"),
                                        ("End Duration", "end_duration_input"),
                                    ])
                                ]),
                            
                            self.box("vertical", "File Paths", [
                                    self.form([
                                        ("Bar File", "bar_file_input"),
                                        ("Dot File", "dot_file_input"),
                                        ("Dot AVI File", "dot_avi_file_input"),
                                        ("Segment Overlay File", "segment_overlay_file_input"),
                                    ])
                                ]),
                            
                            self.box("vertical", "Output Settings", [
                                    self.form([
                                        ("Output Directory", "output_dir_input"),
                                    ])
                                ]),
                            
                            self.box("vertical", "Font Settings", [
                                    self.form([
                                        ("Font Path", "font_path_input"),
                                        ("Font Size", "font_size_input"),
                                    ])
                                ]),
                            
                            self.box("vertical", "FFmpeg", [
                                    self.form([
                                        ("FFmpeg Binary", "ffmpeg_bin_input"),
                                    ])
                                ]),
                        ])
                    ])
                ]),
    
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
        self.width_input.setMaximum(10000)
        self.height_input.setMaximum(10000)
        self.fps_input.setRange(0.1, 240.0)
        self.fps_input.setDecimals(2)
        self.end_duration_input.setRange(1, 600)
        self.font_size_input.setRange(1, 256)

    def set_widgets(self):
        self.status_label.setText("Click below to generate segment overlay video.")
        self.generate_button.setText("Generate Overlay")

        self.width_input.setValue(1920)
        self.height_input.setValue(120)
        self.fps_input.setValue(59.94)
        self.output_dir_input.setText("SegmentOverlayFiles(MM-DD-YY)")
        self.bar_file_input.setText("bar_overlay.mp4")
        self.dot_file_input.setText("dot_overlay.mp4")
        self.dot_avi_file_input.setText("dot_overlay.avi")
        self.segment_overlay_file_input.setText("SegmentOverlayFiles(MM-DD-YY)/Segment_Overlay_(6-20-25)-R2.mp4")
        self.end_duration_input.setValue(15)
        self.font_path_input.setText("C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF")
        self.font_size_input.setValue(24)
        self.ffmpeg_bin_input.setText("ffmpeg")




