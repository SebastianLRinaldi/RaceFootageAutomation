from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
from src.helper_functions import *

class Logic(QObject):
    valueChanged = pyqtSignal(tuple)  # Emits (R, G, B)
    
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui

    def open_dialog(self):
            dialog = QColorDialog(self.ui)
            if self.rgb:  # if you have a saved color
                dialog.setCurrentColor(QColor(*self.rgb))
            dialog.colorSelected.connect(self._color_selected)
            dialog.exec()

    def _color_selected(self, color):
        self.rgb = (color.red(), color.green(), color.blue())
        self.valueChanged.emit(self.rgb)


    def update_label_color(self, rgb):
        self.ui.label.setStyleSheet(f"background-color: rgb{rgb};")

    def value(self):
        return self.rgb

    def setValue(self, rgb):
        self.rgb = rgb
        self.update_label_color(rgb)
