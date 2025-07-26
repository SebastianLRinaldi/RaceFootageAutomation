from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic


        self.ui.button_add.clicked.connect(self.logic.add_file)
        self.ui.button_generate.clicked.connect(self.logic.generate_all)
        # self.logic.thread.finished.connect(self.logic.on_finished)