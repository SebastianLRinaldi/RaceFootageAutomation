from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

from .widgets.PathInputWidget import PathInputWidget

class Layout(UiManager):

    # GPX settings
    gpx_dir_input: PathInputWidget  # folder picker for GPX file directory

    fps_input: QDoubleSpinBox
    duration_input: QDoubleSpinBox

    # Overlay appearance
    frame_width_input: QSpinBox
    frame_height_input: QSpinBox
    scale_input: QSpinBox
    radius_input: QSpinBox

    max_val_input: QDoubleSpinBox

    # UI
    label: QLabel
    file_list: QListWidget
    button_add: QPushButton
    button_generate: QPushButton

    file_tree: QTreeView
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_properties()
        self.set_widgets()

        layout_data = [
            self.tabs(tab_labels=["GPX Generator", "Files", "Settings"], children=[
                self.group("vertical", [
                    "label",
                    "file_list",
                    "button_add",
                    "button_generate"
                ]),

                self.box("vertical","Files", ["file_tree"]),

                self.scroll([
                    self.group("vertical", [

                        self.box("vertical", "General", [
                            self.form([
                                ("GPX Directory", "gpx_dir_input"),
                                ("FPS", "fps_input"),
                                ("Duration (sec)", "duration_input"),
                            ])
                        ]),

                        self.box("vertical", "Video Frame", [
                            self.form([
                                ("Frame Width", "frame_width_input"),
                                ("Frame Height", "frame_height_input"),
                            ])
                        ]),

                        self.box("vertical", "Overlay Visuals", [
                            self.form([
                                ("Radius", "radius_input"),
                                ("G-Scale", "scale_input"),
                                ("Max G-force", "max_val_input"),
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
        self.fps_input.setRange(0.1, 240.0)
        self.fps_input.setDecimals(2)
        self.duration_input.setRange(0.0, 600.0)
        self.duration_input.setDecimals(2)

        self.frame_width_input.setMaximum(10000)
        self.frame_height_input.setMaximum(10000)

        self.scale_input.setMaximum(10000)
        self.radius_input.setMaximum(10000)

        self.max_val_input.setRange(0.1, 10.0)
        self.max_val_input.setDecimals(2)

    def set_widgets(self):
        # Main UI
        self.label.setText("Queued files:")
        self.button_add.setText("Add GPX File")
        self.button_generate.setText("Generate All Overlays")

        # Config values from your logic
        self.gpx_dir_input.setText("F:/_Small/344 School Python/TrackFootageEditor/RaceStorage/(6-20-25)-R2")
        self.fps_input.setValue(59.94)
        self.duration_input.setValue(0)  # leave 0 = auto from file

        self.frame_width_input.setValue(640)
        self.frame_height_input.setValue(480)

        self.radius_input.setValue(200)
        self.scale_input.setValue(200)

        self.max_val_input.setValue(2.0)
