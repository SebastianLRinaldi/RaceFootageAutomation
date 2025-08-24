from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from .layout import Layout
from src.helper_functions import *

class Logic(QObject):
    valueChanged = pyqtSignal(str)
    pathsSelected = pyqtSignal(list)   # <--- signal
    
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui
        self.last_path = ""

        self.file_tree_loader = fileTreeLoader(self.ui.drive_file_tree, "")
        self.file_tree_loader.set_file_filter(["*.mp4"])
        self.file_tree_loader.file_tree.setContextMenuPolicy(Qt.ContextMenuPolicy.CustomContextMenu)
        self.file_tree_loader.file_tree.customContextMenuRequested.connect(self.open_menu)
        


    def update_directory(self, path: str):
        if path != self.last_path: 
            self.last_path = path
            self.file_tree_loader.set_directory(self.last_path)
            self.valueChanged.emit(self.last_path)

    def value(self):
        return self.last_path

    def setValue(self, path):
        self.update_directory(path)



    def open_menu(self, position):
        indexes = self.file_tree_loader.file_tree.selectionModel().selectedIndexes()
        paths = [self.file_tree_loader.file_tree.model().filePath(i) for i in indexes if i.column() == 0]

        if not paths:
            return

        menu = QMenu()
        act_send = QAction("Send Paths", self.ui)
        act_send.triggered.connect(lambda: self.pathsSelected.emit(paths))  # <--- emit
        menu.addAction(act_send)
        menu.exec(self.file_tree_loader.file_tree.viewport().mapToGlobal(position))

    # def get_selected_files(self):
    #     indexes = self.file_tree.selectionModel().selectedIndexes()
    #     # QFileSystemModel repeats columns, so filter only column 0 (the name col)
    #     paths = []
    #     for index in indexes:
    #         if index.column() == 0:
    #             paths.append(self.tree_model.filePath(index))
    #     return paths

    # def on_selection_changed(self, selected, deselected):
    #     indexes = self.file_tree.selectionModel().selectedIndexes()
    #     paths = [
    #         self.tree_model.filePath(idx)
    #         for idx in indexes
    #         if idx.column() == 0
    #     ]
    #     print("Now selected:", paths)


    # def open_menu(self, position):
    #     index = self.file_tree.indexAt(position)
    #     if not index.isValid():
    #         return

    #     path = self.tree_model.filePath(index)

    #     menu = QMenu()
    #     action_preview = QAction("My Custom Action", self.file_tree)
    #     action_preview.triggered.connect(lambda: self.my_action(path))
    #     menu.addAction(action_preview)

    #     # add more actions if you want
    #     action_other = QAction("Do Something Else", self.file_tree)
    #     action_other.triggered.connect(lambda: self.other_action(path))
    #     menu.addAction(action_other)

    #     menu.exec(self.file_tree.viewport().mapToGlobal(position))

    # def my_action(self, path):
    #     print("Custom action on:", path)

    # def other_action(self, path):
    #     print("Other action on:", path)



