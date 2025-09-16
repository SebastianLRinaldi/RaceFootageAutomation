from .logic import Logic
from .structure import Structure

class Connections:
    def __init__(self, ui: Structure, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.gatherracetimes.save_button.clicked.connect(self.logic.update_modules_lap_times)

