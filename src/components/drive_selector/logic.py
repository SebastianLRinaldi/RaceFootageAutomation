from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .bundle import Bundle
from src.helper_functions import *

import os

class Logic(Bundle):

    def __init__(self, component):
        super().__init__()
        self._map_widgets(component)
        self.component_window = component.layout

    def browse_directory(self):
        path = QFileDialog.getExistingDirectory(self.component_window, "Select Directory")
        if path:
            self.add_directory(path)

    def add_directory(self, path: str):
        if not path.strip():  # ignore empty or whitespace-only
            return
        
        if not os.path.isdir(path):
            QMessageBox.warning(self.component_window, "Invalid Directory", f"Path does not exist:\n{path}")
            return

        # avoid duplicates
        if path not in [self.drive_combo.itemText(i) for i in range(self.drive_combo.count())]:
            self.drive_combo.addItem(path)
            
        self.drive_combo.setCurrentText(path)
        
    def delete_selected(self):
        idx = self.drive_combo.currentIndex()
        if idx >= 0:
            self.drive_combo.removeItem(idx)


    def delete_all_directories(self):
        """Remove all saved directories."""
        self.drive_combo.clear()

    def get_current_directory(self) -> str:
        return self.drive_combo.currentText()

    def get_all_directories(self) -> list[str]:
        """Return all saved paths in the combo box."""
        return [self.drive_combo.itemText(i) for i in range(self.drive_combo.count())]
