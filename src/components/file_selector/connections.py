from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        # connect combo change directly
        # self.ui.drive_selector.drive_combo.currentTextChanged.connect(self.logic.update_directory)
                # connect once here
        # self.ui.drive_selector.drive_combo.currentTextChanged.connect(self.logic.update_directory)
