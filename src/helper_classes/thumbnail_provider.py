from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
import os
import subprocess

class ThumbnailWorkerSignals(QObject):
    finished = pyqtSignal(str, QIcon)  # file path, icon

class ThumbnailWorker(QRunnable):
    def __init__(self, file_path, signals):
        super().__init__()
        self.file_path = file_path
        self.signals = signals

    def run(self):
        thumb_path = self.file_path + "_thumb.png"
        if not os.path.exists(thumb_path):
            subprocess.run([
                "ffmpeg", "-y", "-i", self.file_path,
                "-vf", "thumbnail,scale=256:144", "-frames:v", "1", thumb_path
            ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
        if os.path.exists(thumb_path):
            icon = QIcon(QPixmap(thumb_path))
            self.signals.finished.emit(self.file_path, icon)


class ThumbnailProvider(QFileIconProvider):
    def __init__(self, view: QTreeView):
        super().__init__()
        self._cache = {}  # path -> QPixmap

    def create_thumbnail(self, file_path):
        if file_path in self._cache:
            return self._cache[file_path]

        cmd = [
            "ffmpeg",
            "-i", file_path,
            "-vf", "thumbnail,scale=256:144",
            "-frames:v", "1",
            "-f", "image2pipe",
            "pipe:1"
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            pixmap = QPixmap()
            if pixmap.loadFromData(result.stdout):
                self._cache[file_path] = pixmap
                return pixmap
        except subprocess.CalledProcessError:
            return None

    def icon(self, file_info):
        path = file_info.absoluteFilePath()
        ext = path.lower().split('.')[-1]

        if ext in ("mp4", "mov", "avi", "mkv"):
            pixmap = self.create_thumbnail(path)
            if pixmap:
                return QIcon(pixmap)

        elif ext in ("png", "jpg", "jpeg", "bmp", "gif"):
            if path not in self._cache:
                pixmap = QPixmap(path)
                if not pixmap.isNull():
                    self._cache[path] = pixmap.scaled(256, 144)
            return QIcon(self._cache.get(path, QPixmap()))

        return super().icon(file_info)



#"""
# OLD - not threaded
# class ThumbnailProvider(QFileIconProvider):
#     def __init__(self, view: QTreeView):
#         super().__init__()

#     def create_thumbnail(self, file_path):
#         thumb = file_path + "_thumb.png"
#         if not os.path.exists(thumb):
#             subprocess.run([
#                 "ffmpeg", "-y", "-i", file_path, "-vf", "thumbnail,scale=256:144", "-frames:v", "1", thumb
#             ], stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
#         return thumb
        

#     def icon(self, file_info):
#         path = file_info.absoluteFilePath()
#         ext = path.lower().split('.')[-1]

#         # Video thumbnails
#         if ext in ("mp4", "mov", "avi", "mkv"):
#             thumb_path = self.create_thumbnail(path)
#             if os.path.exists(thumb_path):
#                 return QIcon(QPixmap(thumb_path))

#         # Image thumbnails
#         elif ext in ("png", "jpg", "jpeg", "bmp", "gif"):
#             pixmap = QPixmap(path)
#             if not pixmap.isNull():
#                 thumb = pixmap.scaled(256, 144)  # size of thumbnail
#                 return QIcon(thumb)

#         # fallback default icon
#         return super().icon(file_info)
#"""