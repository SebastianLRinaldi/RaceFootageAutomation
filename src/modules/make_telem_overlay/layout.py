from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *



class Layout(UiManager):


    fps_input: QDoubleSpinBox

    # Overlay appearance
    width_input: QSpinBox
    height_input: QSpinBox

    rendered_file_name: QLineEdit
    scale_input: QSpinBox
    radius_input: QSpinBox

    max_val_input: QDoubleSpinBox

    # UI
    status_label: QLabel

    button_add: QPushButton
    generate_button: QPushButton

    file_tree: FilesView
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_properties()
        self.set_widgets()

        layout_data = [
            self.tabs(tab_labels=["GPX Generator", "Files", "Settings"], children=[
                self.group("vertical", [
                    "status_label",
                    "button_add",
                    "generate_button"
                ]),

                self.box("vertical","Files", [self.file_tree.layout]),

                self.scroll([
                    self.group("vertical", [

                        self.box("vertical", "General", [
                            self.form([
                                ("FPS", "fps_input"),
                            ])
                        ]),

                        self.box("vertical", "Video Frame", [
                            self.form([
                                ("Frame Width", "width_input"),
                                ("Frame Height", "height_input"),
                            ])
                        ]),

                        self.box("vertical", "Output Settings", [
                            self.form([
                                ("Output Video File", self.rendered_file_name),
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

        self.width_input.setMaximum(10000)
        self.height_input.setMaximum(10000)

        self.scale_input.setMaximum(10000)
        self.radius_input.setMaximum(10000)

        self.max_val_input.setRange(0.1, 10.0)
        self.max_val_input.setDecimals(2)

    def set_widgets(self):
        # Main UI
        self.status_label.setText("Queued files:")
        self.button_add.setText("Add GPX File")
        self.generate_button.setText("Generate All Overlays")

        # # Config values from your logic
        # self.gpx_dir_input.logic.setText("F:/_Small/344 School Python/TrackFootageEditor/RaceStorage/(6-20-25)-R2")
        # self.fps_input.setValue(59.94)
        # self.duration_input.setValue(0)  # leave 0 = auto from file

        # self.frame_width_input.setValue(640)
        # self.frame_height_input.setValue(480)

        # self.radius_input.setValue(200)
        # self.scale_input.setValue(200)

        # self.max_val_input.setValue(2.0)
