from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import sys
import time
import subprocess

from .layout import Layout
from src.helper_functions import *
from src.helper_classes import *


class Logic(QObject):
    valueChanged = pyqtSignal(str)  # emits the directory path whenever it changes
    
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui

        self.tree_directory = ""

        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath(self.tree_directory)
        self.ui.files_view.setModel(self.tree_model)
        self.ui.files_view.setRootIndex(self.tree_model.index(self.tree_directory))
        self.tree_model.setIconProvider(ThumbnailProvider(self.ui.files_view))

        self.tree_model.rootPathChanged.connect(self.valueChanged)

    def set_directory(self, path: str):
        print(f"SET = {path} | self.tree_directory = {self.tree_directory} ")
        if path != self.tree_directory: 
            if not path.strip():  # ignore empty or whitespace-only
                self.tree_directory = ""
                self.tree_model.setRootPath(self.tree_directory)
                self.ui.files_view.setRootIndex(self.tree_model.index(self.tree_directory))
                return

            if not os.path.isdir(path):
                QMessageBox.warning(
                    self.ui,
                    "FILETREE: Invalid Directory",
                    f"The path does not exist:\n{path}"
                )
                return

            self.tree_directory = path
            self.tree_model.setRootPath(self.tree_directory)
            self.ui.files_view.setRootIndex(self.tree_model.index(self.tree_directory))


    def get_directory(self):
        return self.tree_directory 

    def set_large_icons(self):
        self.ui.files_view.setIconSize(QSize(256, 144))
        
    def set_med_icons(self):
        self.ui.files_view.setIconSize(QSize(128, 72))
        
    def set_small_icons(self):
        self.ui.files_view.setIconSize(QSize(64, 36))

    def set_tiny_icons(self):
        self.ui.files_view.setIconSize(QSize(32, 18))

    def preview_file(self, index):
        path = self.ui.files_view.model().filePath(index)
        if os.path.isfile(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def set_file_filter(self, extensions: list[str]):
        """
        Show only files matching the given extensions.
        Example: loader.set_file_filter(["*.mp4", "*.avi"])
        """
        self.tree_model.setNameFilters(extensions)
        self.tree_model.setNameFilterDisables(False)  # hide everything else

    def value(self):
        return self.tree_directory

    def setValue(self, path):
        self.set_directory(path)
        self.valueChanged.emit(self.tree_directory)

    def collect_selected_items(self):
        tree = self.ui.files_view
        model = self.tree_model
        indexes = [i for i in tree.selectionModel().selectedIndexes() if i.column() == 0]

        if not indexes:
            return

        selected_items = []
        for i in indexes:
            path = model.filePath(i)
            icon = model.fileIcon(i)
            selected_items.append(FileItem(path, icon))  # create a FileItem here
            print("GIT ITEM")
        return selected_items


    # def open_menu(self, position):
    #     tree = self.ui.files_view
    #     model =self.tree_model 
    #     indexes = [i for i in tree.selectionModel().selectedIndexes() if i.column() == 0]

    #     if not indexes:
    #         return

    #     items = []
    #     for i in indexes:
    #         path = model.filePath(i)
    #         icon = model.fileIcon(i)
    #         items.append(FileItem(path, icon))  # create a FileItem here

    #     menu = QMenu()
    #     act_send = QAction("Send Items", self.ui)
    #     act_send.triggered.connect(lambda: self.filesItemsSelected.emit(items))  # send the objects
    #     menu.addAction(act_send)
    #     menu.exec(tree.viewport().mapToGlobal(position))