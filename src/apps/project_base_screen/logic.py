from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import shutil

from .layout import Layout
from src.components import *
from src.modules import *
from src.helper_functions import *

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui

        self.settings = QSettings("TrackFootage", "project_base_screen")
        self.directory = os.path.normpath(self.settings.value("last_dir", ""))  # fallback is empty string

        self.tree_model = QFileSystemModel()
        self.tree_model.setReadOnly(False)
        self.tree_model.setRootPath(os.path.normpath("C:/"))  # Or whatever folder you want
        self.ui.project_tree.setDragDropMode(QAbstractItemView.DragDropMode.DragDrop )
        self.ui.project_tree.setDefaultDropAction(Qt.DropAction.MoveAction)
        self.ui.project_tree.setDragEnabled(True)
        self.ui.project_tree.setAcceptDrops(True)
        
        self.load_folders()
        self.ui.project_list.setCurrentRow(0)
        self.display_project_folder()

    def on_double_click(self, index):
        path = self.tree_model.filePath(index)
        if QFileInfo(path).isFile():
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))


    # Delete currently selected file/folder
    def delete_selected(self):
        index = self.ui.project_tree.currentIndex()
        if not index.isValid():
            return
        path = os.path.normpath(self.tree_model.filePath(index))
        if os.path.isdir(path):
            shutil.rmtree(path)
        else:
            os.remove(path)
        # self.tree_model.refresh()

    # Create new file inside selected directory
    def create_file(self, filename="new_file.txt"):
        index = self.ui.project_tree.currentIndex()
        dir_path = os.path.normpath(self.tree_model.filePath(index))
        if not os.path.isdir(dir_path):
            dir_path = os.path.normpath(os.path.dirname(dir_path))
        full_path = os.path.normpath(os.path.join(dir_path, filename))
        with open(full_path, "w") as f:
            f.write("")
        # self.tree_model.refresh()

    # Create new folder inside selected directory
    def create_folder(self, foldername="New Folder"):
        index = self.ui.project_tree.currentIndex()
        dir_path = os.path.normpath(self.tree_model.filePath(index))
        if not os.path.isdir(dir_path):
            dir_path = os.path.normpath(os.path.dirname(dir_path))
        os.makedirs(os.path.normpath(os.path.join(dir_path, foldername)), exist_ok=True)
        # self.tree_model.refresh()

    # Optional: handle rename events
    def on_renamed(self, path, old_name, new_name):
        print(f"Renamed {old_name} to {new_name} in {path}")


    def select_directory(self):
        
        directory = QFileDialog.getExistingDirectory(self.ui, "Select Directory")
        
        if directory:
            self.directory = os.path.normpath(directory)
            self.load_folders()


    def load_folders(self):
        self.ui.directory_search.logic.setText(self.directory)
        self.settings.setValue("last_dir", self.directory)
        
        self.ui.project_list.clear()
        try:
            for name in os.listdir(self.directory):
                path = os.path.normpath(os.path.join(self.directory, name))
                if os.path.isdir(path):
                    self.ui.project_list.addItem(name)
        except Exception as e:
            print(f"Error reading directory: {e}")



    
    
    def get_project_name(self, date_str: str, run_id: str):
        return f"{date_str}-{run_id}"

    def create_project_structure(self, date_str: str, run_id: str):
        name = self.get_project_name(date_str, run_id)
        path = os.path.normpath(os.path.join(self.directory, name))

        if os.path.exists(path):
            return None, f"Project already exists: {path}"

        try:
            os.makedirs(path)
            subdirs = ["Race Times", "Final Footage", "Raw Footage"] 
            for sub in subdirs:
                os.makedirs(os.path.normpath(os.path.join(path, sub)))
                
            subdirs = ["Table Overlay", "Telemetry Overlay", "Timer Overlay", "Segment Overlay",  ]
            for sub in subdirs:
                main_sub_path = os.path.join(path, sub)
                os.makedirs(main_sub_path)
                os.makedirs(os.path.join(main_sub_path, "assets"))
                os.makedirs(os.path.join(main_sub_path, "rendered"))

            # Create config file: {project_name}.json
            config_filename = f"{name}.json"
            config_path = os.path.normpath(os.path.join(path, config_filename))
            create_config(config_path, initial_data={"project_name": name})

            return path, None
        except Exception as e:
            return None, str(e)


    def open_new_project_dialog(self):
        dialog = NewProjectDialog().layout
        
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

        full_path = os.path.normpath(os.path.join(self.directory, project_name))


        self.ui.project_tree.setModel(self.tree_model)
        self.ui.project_tree.setRootIndex(self.tree_model.index(full_path))  # Or any folder path
