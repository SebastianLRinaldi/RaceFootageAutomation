from .logic import Logic
from .bundle import Bundle

class Connections(Bundle):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        self.save_button.clicked.connect(self.logic.process_and_store_lap_times)