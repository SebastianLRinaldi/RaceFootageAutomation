from .logic import Logic
from .bundle import Bundle

class Connections(Bundle):
    def __init__(self, component, logic: Logic):
        super().__init__()
        self._map_widgets(component)
        self.logic = logic

        self.directory_search.browse_button.clicked.connect(self.logic.select_directory)
        self.new_project_btn.clicked.connect(self.logic.open_new_project_dialog)
        self.project_list.itemSelectionChanged.connect(self.logic.display_project_folder)


        
        self.project_tree.doubleClicked.connect(self.logic.on_double_click)
        # self.ui.deleteButton.clicked.connect(self.logic.delete_selected)
        # self.ui.newFileButton.clicked.connect(self.logic.create_file)
        # self.ui.newFolderButton.clicked.connect(self.logic.create_folder)
        
