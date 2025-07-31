from .Functions import Logic
from .Layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

