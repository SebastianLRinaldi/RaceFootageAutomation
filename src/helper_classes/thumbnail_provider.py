from PyQt6.QtCore import *
from PyQt6 import QtCore
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
import os
import subprocess
from concurrent.futures import ThreadPoolExecutor
import traceback
from pymediainfo import MediaInfo
from typing import Optional
import base64

class ThumbnailWorkerSignals(QObject):
    finished = pyqtSignal(str, QIcon)  # file path, icon


class ThumbnailWorker(QThread):
    finished = pyqtSignal(str, QPixmap)  # path, pixmap
    error = pyqtSignal(str, str)

    def __init__(self, file_path, cache):
        super().__init__()
        self.file_path = file_path
        self.cache = cache

    def run(self):
        cmd = [
            "ffmpeg",
            "-i", self.file_path,
            "-vf", "thumbnail,scale=256:144",
            "-frames:v", "1",
            "-f", "image2pipe",
            "pipe:1"
        ]
        try:
            result = subprocess.run(cmd, capture_output=True, check=True)
            pixmap = QPixmap()

            print(f"if pixmap.loadFromData(result.stdout): {pixmap.loadFromData(result.stdout)} : result.stdout:{result.stdout}")
            if pixmap.loadFromData(result.stdout):
                self.cache[self.file_path] = pixmap
                self.finished.emit(self.file_path, pixmap)  # notify
        except subprocess.CalledProcessError as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)




# class ThumbnailProvider(QFileIconProvider):
#     def __init__(self, view: QTreeView):
#         super().__init__()
#         self.cache = {}  # path -> QPixmap
#         self.workers = {}  # path -> worker, to keep alive
#         self.view = view

#     def create_thumbnail(self, file_path):
#         worker = ThumbnailWorker(file_path, self.cache)
#         worker.finished.connect(self.on_finished)  # connect signal
#         worker.error.connect(self.on_error)
#         self.workers[file_path] = worker
#         worker.start()

#     def on_finished(self, file_path, pixmap):
#         self.cache[file_path] = pixmap
#         model = self.view.model()
#         # model.modelReset.emit()
#         # # model.layoutChanged.emit()

#             # Find index of the file_path
#         for row in range(model.rowCount()):
#             index = model.index(row, 0)
#             file_info = index.data(Qt.ItemDataRole.UserRole)
#             if isinstance(file_info, QFileInfo) and file_info.absoluteFilePath() == file_path:
#                 model.dataChanged.emit(index, index, [Qt.ItemDataRole.DecorationRole])
    


#     def on_error(self, err_type: str, tb_str: str):
#         msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
#         print(f"Icon Error: {msg}")


#     def icon(self, file_info):
#         if isinstance(file_info, QFileInfo):
#             path = file_info.absoluteFilePath()
#             ext = path.lower().split('.')[-1]

#             if ext in ("mp4", "mov", "avi", "mkv"):
#                 if path in self.cache:
#                     print(f"Cache : pixmap:{self.cache[path]}")
#                     return QIcon(self.cache[path])
                

#                 self.create_thumbnail(path)
                

#             elif ext in ("png", "jpg", "jpeg", "bmp", "gif"):
#                 if path not in self.cache:
#                     pixmap = QPixmap(path)
#                     if not pixmap.isNull():
#                         self.cache[path] = pixmap.scaled(256, 144)
#                 return QIcon(self.cache.get(path, QPixmap()))

#         return super().icon(file_info)




"""
Get from image_btyes
"""
# def get_embedded_cover_bytes(file_path: str) -> Optional[bytes]:
#     media_info = MediaInfo.parse(file_path)
#     result: Optional[bytes] = None
#     print(f"TRACKS: {media_info.tracks}")
#     for track in media_info.tracks:
#         # Only consider video tracks
#         is_video_track = track.track_type == "Video"
#         has_cover = hasattr(track, "cover_data") and track.cover_data is not None

#         # Only assign if result not yet set
#         if result is None and is_video_track and has_cover:
#             result = base64.b64decode(track.cover_data)

#     return result



# class ThumbnailProvider(QFileIconProvider):
#     def __init__(self, view: QTreeView):
#         super().__init__()
#         self._cache = {}  # path -> QPixmap

#     def create_thumbnail(self, file_path):
#         if file_path in self._cache:
#             return self._cache[file_path]
#         else:
#             pixmap = QPixmap()
#             cover_bytes = get_embedded_cover_bytes(file_path)
#             if pixmap.loadFromData(cover_bytes):
#                 self._cache[file_path] = pixmap
#                 return pixmap                



#         # cmd = [
#         #     "ffmpeg",
#         #     "-i", file_path,
#         #     "-vf", "thumbnail,scale=256:144",
#         #     "-frames:v", "1",
#         #     "-f", "image2pipe",
#         #     "pipe:1"
#         # ]
#         # try:
#         #     result = subprocess.run(cmd, capture_output=True, check=True)
#         #     pixmap = QPixmap()
#         #     if pixmap.loadFromData(result.stdout):
#         #         self._cache[file_path] = pixmap
#         #         return pixmap
#         # except subprocess.CalledProcessError:
#         #     return None

#     def icon(self, file_info):
#         path = file_info.absoluteFilePath()
#         ext = path.lower().split('.')[-1]

#         if ext in ("mp4", "mov", "avi", "mkv"):
#             pixmap = self.create_thumbnail(path)
#             if pixmap:
#                 return QIcon(pixmap)

#         elif ext in ("png", "jpg", "jpeg", "bmp", "gif"):
#             if path not in self._cache:
#                 pixmap = QPixmap(path)
#                 if not pixmap.isNull():
#                     self._cache[path] = pixmap.scaled(256, 144)
#             return QIcon(self._cache.get(path, QPixmap()))

#         return super().icon(file_info)


























# # --- thread pool ---
# executor = ThreadPoolExecutor(max_workers=4)


# def generate_thumbnail(file_path: str):
#     """Run ffmpeg and return QPixmap (blocking)."""
#     cmd = [
#         "ffmpeg",
#         "-i", file_path,
#         "-vf", "thumbnail,scale=256:144",
#         "-frames:v", "1",
#         "-f", "image2pipe",
#         "pipe:1"
#     ]
#     try:
#         result = subprocess.run(cmd, capture_output=True, check=True)
#         pixmap = QPixmap()
#         if pixmap.loadFromData(result.stdout):
#             return pixmap
#     except subprocess.CalledProcessError:
#         return None
#     return None















# def submit_thumbnail_job(file_path: str):
#     """Submit to executor, returns Future[QPixmap|None]."""
#     return executor.submit(generate_thumbnail, file_path)


# class ThumbnailProvider(QFileIconProvider):
#     def __init__(self):
#         super().__init__()
#         self._cache = {}          # path -> QPixmap
#         self._futures = {}        # path -> Future

#     def icon(self, file_info):
#         path = file_info.absoluteFilePath()
#         ext = path.lower().split('.')[-1]

#         if ext in ("mp4", "mov", "avi", "mkv"):
#             if path in self._cache:
#                 return QIcon(self._cache[path])

#             # start background job if not already started
#             if path not in self._futures:
#                 self._futures[path] = submit_thumbnail_job(path)

#             # if job finished, move into cache
#             future = self._futures[path]
#             if future.done():
#                 pixmap = future.result()
#                 if pixmap:
#                     self._cache[path] = pixmap
#                     return QIcon(pixmap)

#             # fallback: default icon until future completes
#             return super().icon(file_info)

#         elif ext in ("png", "jpg", "jpeg", "bmp", "gif"):
#             if path not in self._cache:
#                 pm = QPixmap(path)
#                 if not pm.isNull():
#                     self._cache[path] = pm.scaled(256, 144)
#             return QIcon(self._cache.get(path, QPixmap()))

#         return super().icon(file_info)









"""
WORKING JUST PAUSES GUI
"""
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