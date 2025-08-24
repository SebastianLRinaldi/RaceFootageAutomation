from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *


class Layout(UiManager):


    # Main interactions
    drive_selector_input: DriveSelector
    file_selector_input:FileSelector

    merge_btn: QPushButton
    



    # # Indicators
    status_label: QLabel
    progress_bar: QProgressBar

    # Files 
    file_tree: QTreeView

    # Settings
    reset_settings_btn: QPushButton
    use_gpu_checkbox: QCheckBox
    rendered_file_name: QLineEdit



    
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [
            self.tabs(tab_labels=["Footage Merger", "Files", "Settings"], children=[
                # Main tab
                self.group("vertical", [
                    self.status_label,
                    self.drive_selector_input.layout,
                    self.file_selector_input.layout,
                    self.merge_btn
                ]),

                self.box("vertical","Files", ["file_tree"]),

                # Settings tab
                self.scroll([
                    self.reset_settings_btn,
                    self.group("vertical", [
                        self.box("vertical", "Video Settings", [
                            self.form([
                                ("Use GPU", self.use_gpu_checkbox),
                            ])
                        ]),


                        self.box("vertical", "Output Settings", [
                            self.form([
                                ("Output Video File", self.rendered_file_name),
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

    def set_widgets(self):
        self.status_label.setText("Drag MP4 files here in the order to merge")

        self.merge_btn.setText("Merge")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
