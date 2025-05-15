from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from application.FrontEnd.C_Grouper.widgetGroupFrameworks import WidgetGroup

class TabHolder(QTabWidget):
    def __init__(
        self,
        title: str = "",
    ):
        super().__init__()
        self.title = title
        self.setTabShape(QTabWidget.TabShape.Triangular)
        self.setMovable(True)
        
    
    def add_groups_as_tabs(self, *pages: WidgetGroup):
        """Add tabs to the master tab widget for the group of widgets as pages"""
        for page in pages:
            title = getattr(page, 'title', None) or page.windowTitle() or "EMPTY"
            self.addTab(page, title)
        return self
