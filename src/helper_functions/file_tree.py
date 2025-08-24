
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import sys















class fileTreeLoader():
    def __init__(self, file_tree: QTreeView, directory: str):
        self.file_tree = file_tree
        self.directory = directory

        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath(self.directory)
        self.file_tree.setModel(self.tree_model)
        self.file_tree.setRootIndex(self.tree_model.index(self.directory))
        self.file_tree.setSelectionMode(QAbstractItemView.SelectionMode.ExtendedSelection)

    def set_directory(self, path: str):
        if not path.strip():  # ignore empty or whitespace-only
            self.directory = ""
            self.tree_model.setRootPath(self.directory)
            self.file_tree.setRootIndex(self.tree_model.index(self.directory))
            return

        
        if not os.path.isdir(path):
            QMessageBox.warning(
                self.file_tree,
                "FILETREE: Invalid Directory",
                f"The path does not exist:\n{path}"
            )
            return

        self.directory = path
        self.tree_model.setRootPath(self.directory)
        self.file_tree.setRootIndex(self.tree_model.index(self.directory))


    def get_directory(self):
        return self.directory 

    # def load_folders(self):
    #     self.file_tree.clear()
    #     try:
    #         for name in os.listdir(self.directory):
    #             path = os.path.join(self.directory, name)
    #             if os.path.isdir(path):
    #                 self.file_tree.addItem(name)
    #     except Exception as e:
    #         print(f"Error reading directory: {e}")

    def set_file_filter(self, extensions: list[str]):
        """
        Show only files matching the given extensions.
        Example: loader.set_file_filter(["*.mp4", "*.avi"])
        """
        self.tree_model.setNameFilters(extensions)
        self.tree_model.setNameFilterDisables(False)  # hide everything else


        