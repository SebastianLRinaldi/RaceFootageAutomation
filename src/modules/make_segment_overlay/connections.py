from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.generate_button.clicked.connect(self.logic.generate_overlay)
        self.ui.reset_segment_settings.clicked.connect(self.logic.settings_handler.reset_settings)
        # self.logic.worker.finished.connect(self.logic.on_finished)
        # self.logic.worker.error.connect(self.logic.on_error)