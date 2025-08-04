from .layout import Layout
from .logic import Logic
from .connections import Connections

class Component():
    def __init__(self):
        super().__init__()
        self.layout = Layout()
        self.logic = Logic(self.layout)
        self.connection = Connections(self.layout, self.logic)