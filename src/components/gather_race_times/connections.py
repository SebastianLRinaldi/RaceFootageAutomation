from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.save_button.clicked.connect(lambda: self.logic.process_and_save(self.ui.text_area.toHtml()))