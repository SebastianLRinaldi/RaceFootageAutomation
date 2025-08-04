from main import Dashboard
from src.apps import * 
from src.helpers import *

class AppConnector:
    projectbasescreen: ProjectBaseScreen

    def __init__(self, main: Dashboard, apps: dict[str, object]):
        self.main = main
        self.apps = apps
        self.init_connections()

        # self.app0.layout.another_widget.btn1.clicked.connect(lambda:print("HELLO"))
        # self.app0.layout.btn1.clicked.connect(lambda:print("HI"))

    def init_connections(self):
        for name, wrapper in self.apps.items():
            setattr(self, name.lower(), wrapper)