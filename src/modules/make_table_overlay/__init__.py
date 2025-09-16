from .layout import Layout
from .logic import Logic
from .connections import Connections
from .bundle import Bundle

class Component(Bundle):
    def __init__(self):
        self._init_widgets()

        self.layout = Layout(self)
        self.logic = Logic(self)
        self.connection = Connections(self, self.logic)