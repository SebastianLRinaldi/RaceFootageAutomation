from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        # connections
        self.browse_btn.clicked.connect(self.logic.browse_directory)
        self.delete_btn.clicked.connect(self.logic.delete_selected)