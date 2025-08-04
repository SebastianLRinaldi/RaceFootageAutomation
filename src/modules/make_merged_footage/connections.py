from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.pick_files_btn.clicked.connect(self.logic.pick_files)
        self.ui.change_output_btn.clicked.connect(self.logic.change_output_location)
        self.ui.merge_btn.clicked.connect(self.logic.merge_files)