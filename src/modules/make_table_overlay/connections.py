from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.logic.project_directory.project_updated.connect(self.logic.on_project_updated)
        self.ui.reset_table_settings.clicked.connect(self.logic.settings_handler.reset_settings)
        self.ui.generate_button.clicked.connect(self.logic.generate_overlay)

        # self.logic.thread.finished.connect(self.logic.on_done)
        # self.logic.thread.error.connect(self.logic.on_error)