from .logic import Logic
from .bundle import Bundle

class Connections(Bundle):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic


        self.button_add.clicked.connect(self.logic.add_file)
        self.generate_button.clicked.connect(self.logic.generate_all)
        # self.logic.thread.finished.connect(self.logic.on_finished)