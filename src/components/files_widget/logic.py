from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os

from .layout import Layout
from src.helper_functions import *
from src.helper_classes import *




class Logic(QObject):

    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui





        
        


    # def update_directory(self, path: str):
    #     if path != self.last_path: 
    #         self.last_path = path
    #         self.file_tree_loader.set_directory(self.last_path)
    #         self.valueChanged.emit(self.last_path)

    # def value(self):
    #     return self.last_path

    # def setValue(self, path):
    #     self.update_directory(path)

    # def on_selection_changed(self):
    #     tree = self.file_tree_loader.file_tree
    #     model = self.file_tree_loader.tree_model
    #     indexes = [i for i in tree.selectionModel().selectedIndexes() if i.column() == 0]

    #     if not indexes:
    #         return

    #     selected_items = []
    #     for i in indexes:
    #         path = model.filePath(i)
    #         icon = model.fileIcon(i)
    #         selected_items.append(FileItem(path, icon))  # create a FileItem here
    #     self.filesItemsSelected.emit(selected_items)



    # # def open_menu(self, position):
    # #     indexes = self.file_tree_loader.file_tree.selectionModel().selectedIndexes()
    # #     paths = [self.file_tree_loader.file_tree.model().filePath(i) for i in indexes if i.column() == 0]

    # #     if not paths:
    # #         return

    # #     menu = QMenu()
    # #     act_send = QAction("Send Paths", self.ui)
    # #     act_send.triggered.connect(lambda: self.pathsSelected.emit(paths))  # <--- emit
    # #     menu.addAction(act_send)
    # #     menu.exec(self.file_tree_loader.file_tree.viewport().mapToGlobal(position))

    # def open_menu(self, position):
    #     tree = self.file_tree_loader.file_tree
    #     model = self.file_tree_loader.tree_model
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



