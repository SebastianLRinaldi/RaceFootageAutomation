from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from src.core.gui.ui_manager import *
from .bundle import Bundle


class Layout(UiManager, Bundle):
    """
    Where you arrange and decorate the widgets
    """

    def __init__(self, component):
        super().__init__()
        
        self._map_widgets(component)
        self.set_widgets()

        layout_data = [

            self.splitter(
                "horizontal",
                [
                    self.box("vertical", "Projects",[
                        "project_list",
                        "new_project_btn",
                        "open_project_btn",
                        self.box("horizontal", "Current Directory",[self.directory_search.layout]),
                        
                    ]),

                    self.box("vertical", "Project", ["project_tree"]),
                ]),
        ]
        self.apply_layout(layout_data)



    def set_widgets(self):
        # widget.setFlow(QListWidget.Flow.TopToBottom)
        self.new_project_btn.setText("New Project")
        self.open_project_btn.setText("Open Project")





