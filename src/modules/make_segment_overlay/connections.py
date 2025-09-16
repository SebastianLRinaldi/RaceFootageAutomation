from .logic import Logic
from .bundle import Bundle

class Connections(Bundle):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic


        self.generate_button.clicked.connect(self.logic.generate_overlay)
        self.reset_segment_settings.clicked.connect(self.logic.settings_handler.reset_settings)
        # self.logic.worker.finished.connect(self.logic.on_finished)
        # self.logic.worker.error.connect(self.logic.on_error)