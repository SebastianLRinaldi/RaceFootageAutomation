from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *


from src.core.GUI.UiManager import *

class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setViewMode(QListWidget.ViewMode.ListMode)
        self.setIconSize(QPixmap(128, 128).size())
        self.setSpacing(5)
        self.setMovement(QListView.Movement.Snap)
        self.setDragDropMode(QListWidget.DragDropMode.InternalMove)
        self.setSelectionMode(QListWidget.SelectionMode.SingleSelection)
        self.setDragEnabled(True)
        self.setAcceptDrops(True)
        self.setDropIndicatorShown(True)
        self.drag_start_pos = None

    def mousePressEvent(self, event):
        if event.button() == Qt.MouseButton.LeftButton:
            self.drag_start_pos = event.position().toPoint()
        super().mousePressEvent(event)

    def mouseMoveEvent(self, event):
        if self.drag_start_pos is None:
            return
        if (event.position().toPoint() - self.drag_start_pos).manhattanLength() >= QApplication.startDragDistance():
            drag_item = self.currentItem()
            if drag_item:
                drag = QDrag(self)
                mime_data = self.model().mimeData(self.selectedIndexes())
                drag.setMimeData(mime_data)
                drag.exec(Qt.DropAction.MoveAction)
        super().mouseMoveEvent(event)