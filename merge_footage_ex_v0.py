import sys
import subprocess
import os
from PyQt6.QtWidgets import (
    QApplication, QWidget, QVBoxLayout, QLabel, QListWidgetItem,
    QPushButton, QFileDialog, QMessageBox, QListWidget, QListView
)
from PyQt6.QtGui import QPixmap, QIcon, QDrag
from PyQt6.QtCore import Qt


class DraggableListWidget(QListWidget):
    def __init__(self):
        super().__init__()
        self.setViewMode(QListWidget.ViewMode.ListMode)
        self.setFlow(QListView.Flow.LeftToRight)
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


class VideoMerger(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Drag-and-Drop MP4 Merger")
        self.resize(500, 300)

        layout = QVBoxLayout()

        # Label
        self.order_label = QLabel("Drag 2 MP4 files here in the order to merge")
        layout.addWidget(self.order_label)

        # Drag-and-drop list
        self.list_widget = DraggableListWidget()
        self.list_widget.setMaximumHeight(150)
        layout.addWidget(self.list_widget)

        # Pick files manually
        file_btn = QPushButton("Pick Files")
        file_btn.clicked.connect(self.pick_files)
        layout.addWidget(file_btn)

        # Merge
        merge_btn = QPushButton("Merge")
        merge_btn.clicked.connect(self.merge_files)
        layout.addWidget(merge_btn)

        self.setLayout(layout)
        self.setAcceptDrops(True)

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [u.toLocalFile() for u in event.mimeData().urls()]
        mp4s = [p for p in paths if p.endswith(".mp4")]
        for path in mp4s:
            self.add_video_item(path)

    def pick_files(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select MP4 Files", "", "Video Files (*.mp4)")
        for path in files:
            self.add_video_item(path)

    def add_video_item(self, file_path):
        if self.list_widget.count() >= 2:
            return  # Only allow two videos
        thumb_path = self.create_thumbnail(file_path)
        item = QListWidgetItem(QIcon(thumb_path), os.path.basename(file_path))
        item.setData(Qt.ItemDataRole.UserRole, file_path)
        self.list_widget.addItem(item)

    def create_thumbnail(self, file_path):
        thumb = file_path + "_thumb.png"
        if not os.path.exists(thumb):
            subprocess.run([
                "ffmpeg", "-y", "-i", file_path, "-vf", "thumbnail", "-frames:v", "1", thumb
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        return thumb

    def merge_files(self):
        if self.list_widget.count() != 2:
            QMessageBox.warning(self, "Error", "Add exactly 2 videos.")
            return

        file_paths = [
            self.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
            for i in range(2)
        ]

        with open("files.txt", "w") as f:
            for path in file_paths:
                f.write(f"file '{path}'\n")

        out = "merged_output(M-DD-YY)-R#.mp4"
        # Race_2_MainCam_(5-30-25).mp4
        # MainCam_Race_2_(5-30-25).mp4
        cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "files.txt", "-c", "copy", out]

        try:
            subprocess.run(cmd, check=True)
            QMessageBox.information(self, "Done", f"Merged video saved as {out}")
        except subprocess.CalledProcessError as e:
            QMessageBox.critical(self, "ffmpeg Error", str(e))

"""
Need to add rename merged file when you hit submit
Need to make the merge in another thread so that the GUI doesn't stall
Need to add progress bar in the GUI so you can see it
"""
if __name__ == "__main__":
    app = QApplication(sys.argv)
    win = VideoMerger()
    win.show()
    sys.exit(app.exec())
