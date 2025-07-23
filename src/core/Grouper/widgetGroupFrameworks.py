from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class WidgetGroup(QWidget):
    def __init__(self, title=None):
        super().__init__()
        self.title = title

    def add_widgets_to_group(self, *widgets, setlayout:str=None):
        if setlayout == "V" or setlayout == None:
            layout = QVBoxLayout()
            for index, widget in enumerate(widgets):
                layout.addWidget(widget)
            self.setLayout(layout)

        elif setlayout == "H":
            layout = QHBoxLayout()
            for index, widget in enumerate(widgets):
                layout.addWidget(widget)
            self.setLayout(layout)
            
        return self
    