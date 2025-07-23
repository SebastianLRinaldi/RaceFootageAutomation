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
from PyQt6.QtWebEngineWidgets import *
from PyQt6.QtWebEngineCore import *

from src.core.Grouper.SpliterGroupConfiguration import *
from src.core.Grouper.TabGroupConfigureation import *
from src.core.Grouper.widgetGroupFrameworks import *

from src.core.GUI.UiManager import *

# class WebLayout(UiManager):
#     def __init__(self):
#         super().__init__()

#         self.eWebPage = QWebEngineView()
#         self.eWebPage.setUrl(QUrl("chrome://gpu"))
#         self.start_page_btn = QPushButton(text="Start WebPage")
#         self.disable_element_btn = QPushButton(text="Disable Element")
#         self.inject_css_btn = QPushButton(text="Inject Blue")
#         self.highlight_elm_btn = QPushButton(text="Highlight Element")
#         self.design_mode_btn = QPushButton(text="Activate Design Mode")
#         self.devtools_btn =  QPushButton(text="Activate Dev Tools")

#         self.url_input = QLineEdit(text="URL GOES HERE")
#         self.change_url_btn = QPushButton(text="Change to Entered URL")

#         # DevTools view
#         self.devtools_view = QWebEngineView()
#         self.devtools_view.setWindowTitle("DevTools")

#         WebToolsTab = TabHolder(title="Web Tool Tabs")

#         exploreGroup = WidgetGroup(title="Web Explore")
#         manipluateGroup = WidgetGroup(title="Web Editor")
#         searchGroup = WidgetGroup(title="Search Tools")

#         split = MasterSpliterGroup(orientation=Qt.Orientation.Vertical)

#         self.add_widgets_to_window(
#             split.add_widgets_to_spliter(

#                 self.eWebPage,

#                 WebToolsTab.add_groups_as_tabs(
#                     exploreGroup.add_widgets_to_group(
#                         self.start_page_btn,
#                         self.design_mode_btn,
#                         self.devtools_btn,
#                     ),
#                     manipluateGroup.add_widgets_to_group(
#                         self.disable_element_btn,
#                         self.inject_css_btn,
#                         self.highlight_elm_btn,
#                     ),
#                     searchGroup.add_widgets_to_group(
#                         self.url_input,
#                         self.change_url_btn,
#                         setlayout="H"
#                     )
#                 )
#             )
#         )

class Layout(UiManager):
    eWebPage: QWebEngineView
    start_page_btn: QPushButton
    disable_element_btn: QPushButton
    inject_css_btn: QPushButton
    highlight_elm_btn: QPushButton
    design_mode_btn: QPushButton
    devtools_btn: QPushButton
    url_input: QLineEdit
    change_url_btn: QPushButton
    devtools_view: QWebEngineView

    def __init__(self):
        super().__init__()
        self.init_widgets()
        self.set_widgets()

        layout_data = [
            self.splitter("vertical", [
                "eWebPage",
                self.tabs(tab_labels=["Web Explore", "Web Editor", "Search Tools"], children=[
                    self.group("vertical", [
                        "start_page_btn",
                        "design_mode_btn",
                        "devtools_btn"
                    ]),
                    self.group("vertical", [
                        "disable_element_btn",
                        "inject_css_btn",
                        "highlight_elm_btn"
                    ]),
                    self.group("horizontal", [
                        "url_input",
                        "change_url_btn"
                    ])
                ])
            ])
        ]

        self.apply_layout(layout_data)

    def init_widgets(self):
        for name, widget_type in self.__annotations__.items():
            widget = widget_type()
            setattr(self, name, widget)

    def set_widgets(self):
        self.eWebPage.setUrl(QUrl("chrome://gpu"))
        self.start_page_btn.setText("Start WebPage")
        self.disable_element_btn.setText("Disable Element")
        self.inject_css_btn.setText("Inject Blue")
        self.highlight_elm_btn.setText("Highlight Element")
        self.design_mode_btn.setText("Activate Design Mode")
        self.devtools_btn.setText("Activate Dev Tools")
        self.url_input.setText("URL GOES HERE")
        self.change_url_btn.setText("Change to Entered URL")
        self.devtools_view.setWindowTitle("DevTools")