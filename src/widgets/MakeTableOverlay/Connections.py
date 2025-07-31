from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.pick_button.clicked.connect(self.logic.pick_output_file)
        self.ui.generate_button.clicked.connect(self.logic.generate_overlay)
        # self.logic.thread.finished.connect(self.logic.on_done)
        # self.logic.thread.error.connect(self.logic.on_error)