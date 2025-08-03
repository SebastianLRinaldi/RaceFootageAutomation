from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.pathinputwidget.browse_button.clicked.connect(self.logic.select_directory)
        self.ui.new_project_btn.clicked.connect(self.logic.open_new_project_dialog)
        self.ui.project_list.itemSelectionChanged.connect(self.logic.display_project_folder)
