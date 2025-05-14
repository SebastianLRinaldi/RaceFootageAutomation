from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from application.apps.mySecondWindow.mySecondWindowLayout import My_Second_Page

class SecondPageLogic:
    def __init__(self, ui: My_Second_Page):
        self.ui = ui

    def update_widget(self) -> None:
        self.ui.name_label.setText("Set Some Random Text")

    def reset_widget(self) -> None:
        self.ui.name_label.setText("Reset to default")

    
