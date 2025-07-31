from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.generate_button.clicked.connect(self.logic.generate_overlay)
        # self.logic.worker.finished.connect(self.logic.on_finished)
        # self.logic.worker.error.connect(self.logic.on_error)