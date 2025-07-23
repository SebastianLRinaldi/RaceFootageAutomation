from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.GUI.UiManager import *

from .widgets.DraggableListWidget import DraggableListWidget

class Layout(UiManager):

    order_label: QLabel
    list_widget: DraggableListWidget
    pick_files_btn: QPushButton
    output_label: QLabel
    change_output_btn: QPushButton
    merge_btn: QPushButton
    progress_bar: QProgressBar
    
    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.setup_stylesheets()
        self.set_widgets()

        layout_data = [
            self.group(orientation="vertical", children=[
                "order_label",
                "list_widget",
                "pick_files_btn",
                self.group(orientation="horizontal", children=[
                    "output_label",
                    "change_output_btn"
                ]),
                "merge_btn",
                "progress_bar"
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
        self.order_label.setText("Drag MP4 files here in the order to merge")
        self.list_widget.setMaximumHeight(180)
        self.pick_files_btn.setText("Pick Files")
        self.output_label.setText("Output file: (none)")
        self.change_output_btn.setText("Change Output Location")
        self.merge_btn.setText("Merge")
        self.progress_bar.setRange(0, 0)
        self.progress_bar.setVisible(False)
