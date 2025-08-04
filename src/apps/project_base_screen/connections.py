from .logic import Logic
from .layout import Layout

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic

        self.ui.directory_search.browse_button.clicked.connect(self.logic.select_directory)
        self.ui.new_project_btn.clicked.connect(self.logic.open_new_project_dialog)
        self.ui.project_list.itemSelectionChanged.connect(self.logic.display_project_folder)


        
        self.ui.project_tree.doubleClicked.connect(self.logic.on_double_click)
        # self.ui.deleteButton.clicked.connect(self.logic.delete_selected)
        # self.ui.newFileButton.clicked.connect(self.logic.create_file)
        # self.ui.newFolderButton.clicked.connect(self.logic.create_folder)
        
