from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        # connections
        self.ui.browse_btn.clicked.connect(self.logic.browse_directory)
        self.ui.delete_btn.clicked.connect(self.logic.delete_selected)
       