from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from .bundle import Bundle

class Layout(UiManager, Bundle):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
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

    def set_widgets(self):
        self.status_label.setText("Drag MP4 files here in the order to merge")
        self.merge_btn.setText("Merge")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
        self.source_footage_view.logic.set_med_icons()
        self.source_footage_view.logic.set_file_filter(["*.mp4"])

        
