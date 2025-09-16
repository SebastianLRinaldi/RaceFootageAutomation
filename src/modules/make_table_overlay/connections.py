from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        self.logic.project_directory.project_updated.connect(self.logic.on_project_updated)
        self.reset_table_settings.clicked.connect(self.logic.settings_handler.reset_settings)
        self.generate_button.clicked.connect(self.logic.generate_overlay)

        # self.logic.thread.finished.connect(self.logic.on_done)
        # self.logic.thread.error.connect(self.logic.on_error)