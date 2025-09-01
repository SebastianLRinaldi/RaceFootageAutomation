import os
import sys
import re

from main import Dashboard
from src.apps import * 
from src.components import *
from src.helper_functions import *

class AppConnector:
    
    project_base_screen: ProjectBaseScreen
    project_editor: ProjectEditor

    
    def __init__(self, main: Dashboard, apps: dict[str, object]):
        self.main = main
        self.apps = apps

        self.init_connections()
        self.project_base_screen.layout.open_project_btn.clicked.connect(self.load_project_into_editor)
        self.project_editor.layout.gatherracetimes.layout.save_button.clicked.connect(self.load_project_into_editor)
    
    def init_connections(self):
        for name, wrapper in self.apps.items():
            setattr(self, name.lower(), wrapper)

    def set_project_path_and_name_into_editor(self):
        selected_items = self.project_base_screen.layout.project_list.selectedItems()
        if not selected_items:
            return
        project_name = selected_items[0].text()
        project_path = os.path.join(self.project_base_screen.logic.directory, project_name)

        self.project_editor.layout.project_name_label.setText(project_name)
        self.project_editor.layout.project_path_label.setText(project_path)

        return project_name, project_path



    def load_project_into_editor(self):
        project_name, project_path = self.set_project_path_and_name_into_editor()


        targets = [
            ("gatherracetimes", "Race Times"),
            # ("makestreamviewer", "Raw Footage"),
            # ("makemergedfootage", "Raw Footage"),
            ("makesegmentoverlay", "Segment Overlay"),
            ("maketableoverlay", "Table Overlay"),
            ("maketelemoverlay", "Telemetry Overlay"),
            ("maketimeroverlay", "Timer Overlay")
        ]

        for name, module_name in targets:
            module = getattr(self.project_editor.layout, name)

            module_path = os.path.join(project_path, module_name)

            tree = getattr(module.layout, "file_tree")
            tree.logic.set_directory(module_path)
            tree.logic.set_med_icons()


            # fileTreeLoader(tree, module_path)

            if hasattr(module, "logic") and hasattr(module.logic, "project_directory"):

                module.logic.project_directory.set_up_directory(project_name, project_path, module_path)


        self.main.switch_to("project_editor")

