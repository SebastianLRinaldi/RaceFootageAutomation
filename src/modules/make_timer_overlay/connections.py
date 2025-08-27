from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic
        
        self.ui.reset_settings_btn.clicked.connect(self.logic.settings_handler.reset_settings)

        self.ui.generate_button.clicked.connect(self.logic.generate_overlay)