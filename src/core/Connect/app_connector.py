import os
import sys

from main import Dashboard
from src.apps import * 
from src.helpers import *

class AppConnector:
    
    project_base_screen: ProjectBaseScreen
    project_editor: ProjectEditor

    
    def __init__(self, main: Dashboard, apps: dict[str, object]):
        self.main = main
        self.apps = apps

        self.init_connections()
        self.project_base_screen.layout.open_project_btn.clicked.connect(self.load_project_into_editor)
    
    def init_connections(self):
        for name, wrapper in self.apps.items():
            setattr(self, name.lower(), wrapper)

    def load_path_and_name_into_editor(self):
        selected_items = self.project_base_screen.layout.project_list.selectedItems()
        if not selected_items:
            return
        project_name = selected_items[0].text()
        full_path = os.path.join(self.project_base_screen.logic.directory, project_name)

        self.project_editor.layout.project_name_label.setText(project_name)
        self.project_editor.layout.project_path_label.setText(full_path)

        return full_path

    def load_project_into_editor(self):
        full_path = self.load_path_and_name_into_editor()

        targets = [
            ("gatherracetimes", "Race Times/"),
            ("makestreamviewer", "Raw Footage/"),
            ("makemergedfootage", "Raw Footage/"),
            ("makesegmentoverlay", "Segment Overlay/"),
            ("maketableoverlay", "Table Overlay/"),
            ("maketelemoverlay", "Telemetry Overlay/"),
            ("maketimeroverlay", "Timer Overlay/")
        ]

        for name, subpath in targets:
            sub_ui = getattr(self.project_editor.layout, name)
            tree = getattr(sub_ui.layout, "file_tree")
            path = os.path.join(full_path, subpath)
            fileTreeLoader(tree, path)

        self.main.switch_to("project_editor")



