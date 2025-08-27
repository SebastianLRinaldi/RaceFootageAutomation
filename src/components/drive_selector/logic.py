from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
from src.helper_functions import *

import os

class Logic(QObject):
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui

    def browse_directory(self):
        path = QFileDialog.getExistingDirectory(self.ui, "Select Directory")
        if path:
            self.add_directory(path)

    def add_directory(self, path: str):
        if not path.strip():  # ignore empty or whitespace-only
            return
        
        if not os.path.isdir(path):
            QMessageBox.warning(self, "Invalid Directory", f"Path does not exist:\n{path}")
            return

        # avoid duplicates
        if path not in [self.ui.drive_combo.itemText(i) for i in range(self.ui.drive_combo.count())]:
            self.ui.drive_combo.addItem(path)
            
        self.ui.drive_combo.setCurrentText(path)
        
    def delete_selected(self):
        idx = self.ui.drive_combo.currentIndex()
        if idx >= 0:
            self.ui.drive_combo.removeItem(idx)


    def delete_all_directories(self):
        """Remove all saved directories."""
        self.ui.drive_combo.clear()

    def get_current_directory(self) -> str:
        return self.ui.drive_combo.currentText()

    def get_all_directories(self) -> list[str]:
        """Return all saved paths in the combo box."""
        return [self.ui.drive_combo.itemText(i) for i in range(self.ui.drive_combo.count())]
