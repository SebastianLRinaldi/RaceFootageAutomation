from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.btn.clicked.connect(self.logic.open_file_dialog)