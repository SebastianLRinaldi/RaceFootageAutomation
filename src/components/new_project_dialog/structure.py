from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.layout_builder import *
from .blueprint import Blueprint


class Structure(QDialog):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("Create New Project")

        layout = QVBoxLayout()
        layout.addWidget(QLabel("Date (MM-DD-YY):"))
        layout.addWidget(self.date_input)
        layout.addWidget(QLabel("Run ID (e.g. R1, R2, Enduro):"))
        layout.addWidget(self.run_input)

        btns = QHBoxLayout()
        btns.addWidget(self.create_btn)
        btns.addWidget(self.cancel_btn)
        layout.addLayout(btns)

        self.setLayout(layout)


class Structure(LayoutBuilder, Blueprint):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()
        
        self.layout_data = [
            self.form([(self.date_format_label, self.date_input)]),
            self.form([(self.race_format_label, self.race_format_input)]),
            self.group("horizontal", [self.create_btn, self.cancel_btn])
        ]

        self.apply_layout(component, self)


    def set_widgets(self):
        self.date_input.setPlaceholderText("(MM-DD-YY)")
        self.race_format_input.setPlaceholderText("R1, R2, R#, Enduro")
        self.date_format_label.setText("Date:")
        self.race_format_label.setText("Race Number/Format):")
        self.create_btn.setText("Create")
        self.cancel_btn.setText("Cancel")






