from .logic import Logic
from .blueprint import Blueprint

class Connections(Blueprint):
    def __init__(self, component, logic: Logic):
        self._map_widgets(component)
        self.logic = logic

        self.logic.valueChanged.connect(self.logic.update_label_color)
        self.button.clicked.connect(self.logic.open_dialog)

