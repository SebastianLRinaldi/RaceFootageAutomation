from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import subprocess
import os
import sys



class ThumbnailProvider(QFileIconProvider):
    def __init__(self):
        super().__init__()

    def create_thumbnail(self, file_path):
        thumb = file_path + "_thumb.png"
        if not os.path.exists(thumb):
            subprocess.run([
                "ffmpeg", "-y", "-i", file_path, "-vf", "thumbnail,scale=256:144", "-frames:v", "1", thumb
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return thumb
        

    def icon(self, file_info):
        path = file_info.absoluteFilePath()
        ext = path.lower().split('.')[-1]

        # Video thumbnails
        if ext in ("mp4", "mov", "avi", "mkv"):
            thumb_path = self.create_thumbnail(path)
            if os.path.exists(thumb_path):
                return QIcon(QPixmap(thumb_path))

        # Image thumbnails
        elif ext in ("png", "jpg", "jpeg", "bmp", "gif"):
            pixmap = QPixmap(path)
            if not pixmap.isNull():
                thumb = pixmap.scaled(256, 144)  # size of thumbnail
                return QIcon(thumb)

        # fallback default icon
        return super().icon(file_info)









class fileTreeLoader():
    def __init__(self, file_tree: QTreeView, directory: str):
        self.file_tree = file_tree
        self.directory = directory

        self.tree_model = QFileSystemModel()
        self.tree_model.setRootPath(self.directory)
        self.file_tree.setModel(self.tree_model)
        self.file_tree.setRootIndex(self.tree_model.index(self.directory))
        self.tree_model.setIconProvider(ThumbnailProvider())
        self.file_tree.setIconSize(QSize(256, 144))
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

    def preview_file(self, index):
        path = self.file_tree.model().filePath(index)
        if os.path.isfile(path):
            QDesktopServices.openUrl(QUrl.fromLocalFile(path))

    def set_file_filter(self, extensions: list[str]):
        """
        Show only files matching the given extensions.
        Example: loader.set_file_filter(["*.mp4", "*.avi"])
        """
        self.tree_model.setNameFilters(extensions)
        self.tree_model.setNameFilterDisables(False)  # hide everything else
