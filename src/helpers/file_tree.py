
from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import sys

class fileTreeLoader():
    def __init__(self, file_tree: QListWidget, directory: str):
        self.file_tree = file_tree
        self.directory = directory

        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath(self.directory)
        self.file_tree.setModel(self.tree_model)
        self.file_tree.setRootIndex(self.tree_model.index(self.directory))

    def set_directory(self, path):
        self.directory = path

    # def load_folders(self):
    #     self.file_tree.clear()
    #     try:
    #         for name in os.listdir(self.directory):
    #             path = os.path.join(self.directory, name)
    #             if os.path.isdir(path):
    #                 self.file_tree.addItem(name)
    #     except Exception as e:
    #         print(f"Error reading directory: {e}")