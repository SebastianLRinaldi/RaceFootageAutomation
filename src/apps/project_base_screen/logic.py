from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os

from .layout import Layout
from src.components import *

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.directory = None
        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath('C:/')  # Or whatever folder you want

    def select_directory(self):
        directory = QFileDialog.getExistingDirectory(self.ui, "Select Directory")
        if directory:
            self.directory = directory
            self.ui.project_root_input.setText(directory)
            self.load_folders()


    def load_folders(self):
        self.ui.project_list.clear()
        try:
            for name in os.listdir(self.directory ):
                path = os.path.join(self.directory, name)
                if os.path.isdir(path):
                    self.ui.project_list.addItem(name)
        except Exception as e:
            print(f"Error reading directory: {e}")



    
    
    def get_project_name(self, date_str: str, run_id: str):
        return f"{date_str}-{run_id}"

    def create_project_structure(self, date_str: str, run_id: str):
        name = self.get_project_name(date_str, run_id)
        path = os.path.join(self.directory, name)

        if os.path.exists(path):
            return None, f"Project already exists: {path}"

        try:
            os.makedirs(path)
            subdirs = ["Race Times", "Table Overlay", "Telemetry Overlay", "Timer Overlay", "Segment Overlay", "Final Footage", "Raw Footage", ]
            for sub in subdirs:
                os.makedirs(os.path.join(path, sub))
            return path, None
        except Exception as e:
            return None, str(e)


    def open_new_project_dialog(self):
        dialog = NewProjectDialogLayout(self.ui)
        
        def on_create_clicked():
            date = dialog.date_input.text().strip()
            run = dialog.run_input.text().strip()

            if not date or not run:
                QMessageBox.warning(dialog, "Missing Info", "Date and Run ID are required.")
                return

            path, error = self.create_project_structure( date, run)
            if error:
                QMessageBox.critical(dialog, "Error", error)
            else:
                dialog.accept()
                QMessageBox.information(dialog, "Success", f"Project created at:\n{path}")

        dialog.create_btn.clicked.connect(on_create_clicked)
        dialog.cancel_btn.clicked.connect(dialog.reject)

        if dialog.exec():
            self.load_folders()
            return True
        return False

    def display_project_folder(self):
        selected_items = self.ui.project_list.selectedItems()
        if not selected_items:
            return
        project_name = selected_items[0].text()
        full_path = os.path.join(self.directory, project_name)

        self.ui.project_tree.setModel(self.tree_model)
        self.ui.project_tree.setRootIndex(self.tree_model.index(full_path))  # Or any folder path
