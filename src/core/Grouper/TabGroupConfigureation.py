from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.Grouper.widgetGroupFrameworks import WidgetGroup

class TabHolder(QTabWidget):
    def __init__(self, title: str = "",):
        super().__init__()
        
        self.title = title
        self.setTabShape(QTabWidget.TabShape.Triangular)
        self.setMovable(True)
        
    def add_groups_as_tabs(self, *pages: WidgetGroup):
        """Add tabs to the master tab widget for the group of widgets as pages"""
        for page in pages:
            if page.title:
                self.addTab(page, page.title)
            else:
                self.addTab(page, "EMPTY")
        return self
