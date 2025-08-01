from PyQt6.QtCore import *
from PyQt6.QtWidgets import *
from PyQt6.QtGui import *
import os
import sys

from src.apps.ProjectEditor.Functions import Logic as ProjecteditorLogic        
from src.apps.ProjectBaseScreen.Functions import Logic as ProjectbasescreenLogic

from src.apps.ProjectEditor.Layout import Layout as ProjecteditorLayout
from src.apps.ProjectBaseScreen.Layout import Layout as ProjectbasescreenLayout 


from src.functions.fileTree import fileTreeLoader

from typing import TYPE_CHECKING
if TYPE_CHECKING:
    from main import Dashboard

class AppConnector:
    projecteditor_logic: ProjecteditorLogic
    projectbasescreen_logic: ProjectbasescreenLogic

    projecteditor_ui: ProjecteditorLayout
    projectbasescreen_ui: ProjectbasescreenLayout


    def __init__(self, main: 'Dashboard', apps: dict, logic: dict):
        self.main = main
        self.apps = apps
        self.logic = logic

        self.init_connections()
        self.projectbasescreen_ui.open_project_btn.clicked.connect(self.load_project_into_editor)

    """
    This basically just does this part for us:
    
    class AppConnector:
        basic_ui: BasicLayout
        second_logic: SecondLogic

        def __init__(self, apps, logic):
            self.basic_ui = apps["Basic"]
            self.second_logic = logic["Second"]

            self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)
    """
    def init_connections(self):
        for name in self.apps:
            setattr(self, f"{name.lower()}_ui", self.apps[name])
            setattr(self, f"{name.lower()}_logic", self.logic[name])

    def load_path_and_name_into_editor(self):
        selected_items = self.projectbasescreen_ui.project_list.selectedItems()
        if not selected_items:
            return
        project_name = selected_items[0].text()
        full_path = os.path.join(self.projectbasescreen_logic.directory, project_name)

        self.projecteditor_ui.project_name_label.setText(project_name)
        self.projecteditor_ui.project_path_label.setText(full_path)

        return full_path

    def load_project_into_editor(self):
        full_path = self.load_path_and_name_into_editor()

        # self.projecteditor_ui.gatherracetimes.file_tree

        # w1=fileTreeLoader()
        # w2=fileTreeLoader()
        # w3=fileTreeLoader()
        # w4=fileTreeLoader()
        # w5=fileTreeLoader()
        # w6=fileTreeLoader()
        # w7=fileTreeLoader()


        targets = [
            ("gatherracetimes", "Times/"),
            ("makestreamviewer", "Footage/"),
            ("makemergedfootage", "Final/"),
            ("makesegmentoverlay", "Overlay1/"),
            ("maketableoverlay", "Overlay2/"),
            ("maketelemoverlay", "Overlay3/"),
            ("maketimeroverlay", "Overlay4/")
        ]

        for name, subpath in targets:
            sub_ui = getattr(self.projecteditor_ui, name)
            tree = getattr(sub_ui, "file_tree")
            path = os.path.join(full_path , subpath)
            fileTreeLoader(tree, path)

        


        
        self.main.switch_to("ProjectEditor")


