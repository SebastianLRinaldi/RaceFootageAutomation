from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.gatherracetimes.layout.save_button.clicked.connect(self.logic.update_modules_lap_times)

