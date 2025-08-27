from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *

class Layout(UiManager):
    # Main interactions
    drive_selector_input: DriveSelector
    source_footage_view:FilesView
    choosen_footage_viewer:FilesWidget
    merge_btn: QPushButton

    # # Indicators
    status_label: QLabel
    progress_bar: QProgressBar

    # Files 
    file_tree: FilesView

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
                    
                    self.group("horizontal", [
                        self.drive_selector_input.layout,
                        self.box("vertical", "Merge Files",[
                            self.status_label,
                            self.merge_btn,
                        ]),
                    ]),
                    
                    self.group("horitontal", [                    
                        self.source_footage_view.layout,
                        self.choosen_footage_viewer.layout,])
                ]),

                self.box("vertical","Files", [self.file_tree.layout]),

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
        self.source_footage_view.logic.set_med_icons()
        self.source_footage_view.logic.set_file_filter(["*.mp4"])

        
