from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from src.components import *


class Layout(UiManager):


    # Main interactions
    merge_btn: QPushButton
    # generate_button: QPushButton
    pick_files_btn: QPushButton
    list_widget: DraggableListWidget
    # order_label: QLabel


    # # Indicators
    status_label: QLabel
    progress_bar: QProgressBar
    # output_label: QLabel


    # Files 
    file_tree: QTreeView


    # Settings
    reset_settings_btn: QPushButton
    
    use_gpu_checkbox: QCheckBox
    external_source_dirs_input: QLineEdit

    rendered_file_name: QLineEdit



    
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        # layout_data = [
        #     # self.group(orientation="vertical", children=[
        #     #     "order_label",
        #     #     self.list_widget.layout,
        #     #     "pick_files_btn",
        #     #     self.box("vertical","Files", ["file_tree"]),
        #     #     self.group(orientation="horizontal", children=[
        #     #         "output_label",
        #     #         "change_output_btn"
        #     #     ]),
        #     #     "merge_btn",
        #     #     "progress_bar"
        #     # ])
        # ]


        layout_data = [
            self.tabs(tab_labels=["Footage Merger", "Files", "Settings"], children=[
                # Main tab
                self.group("vertical", [
                    self.status_label,
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

                        self.box("vertical", "External Footage Settings", [
                            self.form([
                                ("External Footage Paths", self.external_source_dirs_input),
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
        pass
        self.status_label.setText("Drag MP4 files here in the order to merge")
        self.list_widget.layout.setMaximumHeight(180)
        self.pick_files_btn.setText("Pick Files")
        # self.output_label.setText("Output file: (none)")
        # self.change_output_btn.setText("Change Output Location")
        self.merge_btn.setText("Merge")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
