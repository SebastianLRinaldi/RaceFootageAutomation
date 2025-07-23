import os
import sys
import time
import re

import threading
from threading import Thread
from enum import Enum
from queue import Queue
from typing import List
from datetime import timedelta

from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

# from src.core.Grouper.SpliterGroupConfiguration import *
# from src.core.Grouper.TabGroupConfigureation import *
# from src.core.Grouper.widgetGroupFrameworks import *


from src.core.GUI.UiManager import *

# class SecondLayout(LayoutManager):
#     def __init__(self):
#         super().__init__()
#         self.list_widget = QListWidget()
#         self.name_label = QLabel(text="Enter your name:")
#         self.text_edit = QTextEdit("This is a multi-line text editor")
        
#         self.radio_button = QRadioButton(text="Select this option")
#         self.check_box = QCheckBox(text="Accept terms and conditions")
        
#         middleSplit = MasterSpliterGroup(orientation=Qt.Orientation.Vertical)
#         labelsGroup = WidgetGroup(title="Random Labels")
#         btnsGroup = WidgetGroup(title="Random Btns")
        
#         self.add_widgets_to_window(
#             middleSplit.add_widgets_to_spliter(
#                 labelsGroup.add_widgets_to_group(
#                     self.name_label,
#                     self.text_edit,
#                     self.list_widget,
#                 ),

#                 btnsGroup.add_widgets_to_group(
#                     self.radio_button,
#                     self.check_box,
#                 )
#             )
#         )

class Layout(UiManager):
    # HEADER
    title_label: QLabel
    status_label: QLabel
    user_label: QLabel
    logout_btn: QPushButton
    search_bar: QLineEdit
    search_btn: QPushButton

    # SIDEBAR
    nav_list: QListWidget

    # DASHBOARD TAB
    graph1: QLabel
    graph2: QLabel
    counter1: QLCDNumber
    counter2: QLCDNumber
    activity_table: QTableWidget

    # JOBS TAB
    job_list: QListWidget
    job_details: QTextEdit
    job_form_label: QLabel
    job_start_btn: QPushButton

    # LOGS TAB
    filter_input: QLineEdit
    log_level_combo: QComboBox
    date_filter: QDateTimeEdit
    logs_table: QTableView
    export_logs_btn: QPushButton

    # SETTINGS TAB
    theme_dark: QRadioButton
    theme_light: QRadioButton
    enable_notifications: QCheckBox
    language_selector: QComboBox
    save_settings_btn: QPushButton
    reset_settings_btn: QPushButton

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.box("horizontal", title="Header", children=[
                self.group("horizontal", ["title_label", "status_label"]),
                self.group("horizontal", ["search_bar", "search_btn"]),
                self.group("horizontal", ["user_label", "logout_btn"])
            ]),
            self.splitter("horizontal", children=[
                self.box("vertical", title="Navigation", children=["nav_list"]),
                self.tabs(tab_labels=["Dashboard", "Jobs", "Logs", "Settings"], children=[
                    self.grid([
                        "graph1", "graph2", 
                        "counter1", "counter2", 
                        "activity_table"
                    ], rows=3, columns=2),

                    self.splitter("horizontal", children=[
                        self.box("vertical", title="Job List", children=["job_list"]),
                        self.box("vertical", title="Job Details", children=[
                            "job_form_label", "job_details", "job_start_btn"])
                    ]),

                    self.group("vertical", [
                        self.group("horizontal", ["filter_input", "log_level_combo", "date_filter"]),
                        "logs_table", "export_logs_btn"
                    ]),

                    self.group("vertical", [
                        self.box("horizontal", title="Theme", children=["theme_dark", "theme_light"]),
                        self.box("vertical", title="Preferences", children=[
                            "enable_notifications", "language_selector"
                        ]),
                        self.group("horizontal", ["save_settings_btn", "reset_settings_btn"])
                    ])
                ])
            ])
        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()

            match widget:
                case QTableWidget():
                    widget.setRowCount(5)
                    widget.setColumnCount(3)
                case QTableView():
                    widget.setModel(QStandardItemModel())
                case QListWidget():
                    widget.addItems([f"Item {i}" for i in range(10)])

            setattr(self, name, widget)

    def set_widgets(self):
        self.title_label.setText("Data Dashboard")
        self.status_label.setText("Status: OK")
        self.user_label.setText("User: Admin")
        self.logout_btn.setText("Logout")
        self.search_btn.setText("Search")

        self.graph1.setText("Graph 1")
        self.graph2.setText("Graph 2")

        self.job_form_label.setText("Job Details")
        self.job_start_btn.setText("Start Job")

        self.export_logs_btn.setText("Export Logs")

        self.theme_dark.setText("Dark")
        self.theme_light.setText("Light")
        self.enable_notifications.setText("Enable Notifications")
        self.save_settings_btn.setText("Save")
        self.reset_settings_btn.setText("Reset")


