from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic
        
        self.reset_settings_btn.clicked.connect(self.logic.settings_handler.reset_settings)

        self.generate_button.clicked.connect(self.logic.generate_overlay)