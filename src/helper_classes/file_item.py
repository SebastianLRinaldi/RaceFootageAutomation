from PyQt6.QtCore import Qt
from PyQt6.QtWidgets import QListWidgetItem, QTreeWidgetItem
from PyQt6.QtGui import QIcon

import os

# class FileItem(QListWidgetItem):
#     def __init__(self, file_path, icon=None):
#         super().__init__(os.path.basename(file_path))
#         if icon:
#             # if icon is a QIcon, set it directly; if string path, wrap it
#             self.setIcon(icon if isinstance(icon, QIcon) else QIcon(icon))
#         # store path in UserRole
#         self.setData(Qt.ItemDataRole.UserRole, file_path)

#     def filePath(self):
#         return self.data(Qt.ItemDataRole.UserRole)

class FileItem(QTreeWidgetItem):
    def __init__(self, file_path:str, icon=None):
        super().__init__([os.path.basename(file_path), file_path])  # two columns
        if icon:
            self.setIcon(0, icon if isinstance(icon, QIcon) else QIcon(icon))
        self._file_path = file_path

    def filePath(self) -> str:
        return self._file_path