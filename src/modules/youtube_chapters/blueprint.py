from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

class Blueprint:
    # label1: QLabel
    # btn1: QPushButton

    def _map_widgets(self, source):
        """
        Copy existing widget instances from source to self.
        """
        # source is some object that already has the widgets as attributes
        for name in self.__annotations__:
            setattr(self, name, getattr(source, name))

    def _init_widgets(self):
        """
        Instantiate all widgets defined in type hints.
        Call this manually when you want actual widget instances.
        """
        for name, typ in self.__annotations__.items():
            setattr(self, name, typ())