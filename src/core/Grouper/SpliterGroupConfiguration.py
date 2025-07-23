from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class MasterSpliterGroup(QSplitter):
    def __init__(self, orientation=Qt.Orientation.Horizontal):
        super().__init__(orientation)
        
        self.setOpaqueResize(True)  # Enable smooth resizing
        self.setChildrenCollapsible(True)  # Prevent widgets from being collapsed
        self.setHandleWidth(5)  # Set handle width for better visibility
        
        # Style the handles
        self.setStyleSheet("""
            QSplitter::handle::Vertical {
                background-color: #2196F3;  /* Blue handle */
                width: 5px;
                margin: 2px;
            }
        """)
        
    def add_widgets_to_spliter(self, *widgets):
        if not all(isinstance(widget, QWidget) for widget in widgets):
            raise TypeError("All items must be instances of QWidget.")
        
        for wiget in widgets:
            self.addWidget(wiget)
        return self