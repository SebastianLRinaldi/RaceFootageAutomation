from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import sys
import subprocess
import os
from pathlib import Path
import traceback
import tempfile

from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *

# class MergeThread(QThread):
#     finished = pyqtSignal(str)
#     error = pyqtSignal(str)

#     def __init__(self, files, output_file):
#         super().__init__()
#         self.files = files
#         self.output_file = output_file

#     def run(self):
#         try:
#             with open("files.txt", "w") as f:
#                 for path in self.files:
#                     f.write(f"file '{path}'\n")
#         except Exception as e:
#             self.error.emit(f"Failed to write files.txt: {e}")
#             return

#         cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "files.txt", "-c", "copy", self.output_file]

#         try:
#             process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
#             _, stderr = process.communicate()

#             if process.returncode != 0:
#                 self.error.emit(f"ffmpeg error (code {process.returncode}):\n{stderr}")
#                 return

#             self.finished.emit(self.output_file)
#         except Exception as e:
#             self.error.emit(str(e))


"""
Some code from streamer view for viewing progress
"""
"""
    def run_ffprobe(self, file_path):
        try:
            result = subprocess.run(
                ["ffprobe", "-v", "error", "-show_streams", file_path],
                stdout=subprocess.PIPE,
                stderr=subprocess.PIPE,
                text=True,
                check=True
            )
            self.ui.output.setPlainText(result.stdout)
        except subprocess.CalledProcessError as e:
            self.ui.output.setPlainText(f"ffprobe error:\n{e.stderr}")
"""


class MergeWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic'):
        super().__init__()
        self.logic = logic  # store the Logic instance

    def run(self):
        try:
            self.logic.make_merged_footage()  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)



class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()

        self.use_gpu = True

        self.rendered_name = f"merged_footage.mp4"

        self.last_footage_dir_selected = ""
        self.combox_save = {"items": [""], "index": 0}

        SETTINGS_FIELDS = [
            ("use_gpu", self.ui.use_gpu_checkbox, self.use_gpu),
            ("rendered_name", self.ui.rendered_file_name, self.rendered_name),
            ("last_footage_dir_selected",  self.ui.source_footage_view.logic, self.last_footage_dir_selected),
            ("combox_save", self.ui.drive_selector_input.layout.drive_combo, self.combox_save),
        ]

        self.ui.source_footage_view.layout.files_view.setContextMenuPolicy(
                Qt.ContextMenuPolicy.CustomContextMenu
            )
        
        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, self, app="merge_footage")


    def merge_footage(self):
        self.ui.merge_btn.setEnabled(False)
        self.ui.status_label.setText("Merging Footage...")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.worker = MergeWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        self.ui.merge_btn.setEnabled(True)

    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.merge_btn.setEnabled(True)

    def handle_file_items(self, file_items: list[FileItem]):
        self.ui.choosen_footage_viewer.layout.files_widget.addTopLevelItems(file_items)

    def get_ffmpeg_cmd(self, concat_txt):
        base_cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            # "-fps_mode", "cfr",
            # # "-r", str(self.fps),
            # "-pix_fmt", "yuv420p",
            "-c", "copy",
            self.project_directory.make_rendered_file_path(self.rendered_name)
        ]

        if self.use_gpu:
            gpu_opts = [
                "-c:v", "h264_nvenc",
                "-preset", "fast",   # NVENC presets
                "-rc", "vbr",
                "-cq", "18"
            ]
            # Insert GPU options before output_file
            return base_cmd[:-1] + gpu_opts + [base_cmd[-1]]
        else:
            cpu_opts = [
                "-c:v", "libx264",
                "-crf", "18",
                "-preset", "slow"
            ]
            # Insert CPU options before output_file
            return base_cmd[:-1] + cpu_opts + [base_cmd[-1]]


    def make_merged_footage(self):
        # Create concat text file for ffmpeg
        with tempfile.TemporaryDirectory() as temp_dir:
            concat_txt = os.path.join(os.path.dirname(temp_dir), "concat_list_merged_footage.txt")
            if concat_txt is None:
                raise AttributeError(f"EMPTY CONCAT TEXT")

            file_item_widget: QTreeWidget = self.ui.choosen_footage_viewer.layout.files_widget

            files = []
            for i in range(file_item_widget.topLevelItemCount()):
                item: FileItem = file_item_widget.topLevelItem(i)
                files.append(item.filePath())
                
            with open(concat_txt, "w") as f:
                for file in files:
                    f.write(f"file '{file}'\n")

            # Usage example:
            cmd = self.get_ffmpeg_cmd(concat_txt=concat_txt)
            subprocess.run(cmd, check=True)



    # def make_merged_footage(self):
    #     try:
    #         with open("files.txt", "w") as f:
    #             for path in self.files:
    #                 f.write(f"file '{path}'\n")
    #     except Exception as e:
    #         self.error.emit(f"Failed to write files.txt: {e}")
    #         return

    #     cmd = ["ffmpeg", "-f", "concat", "-safe", "0", "-i", "files.txt", "-c", "copy", self.rendered_name]

        # try:
        #     process = subprocess.Popen(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        #     _, stderr = process.communicate()

        #     if process.returncode != 0:
        #         self.error.emit(f"ffmpeg error (code {process.returncode}):\n{stderr}")
        #         return

        #     self.finished.emit(self.output_file)
        # except Exception as e:
        #     self.error.emit(str(e))


        

    # def pick_files(self):
    #     files, _ = QFileDialog.getOpenFileNames(self.ui, "Select MP4 Files", "", "Video Files (*.mp4)")
    #     for path in files:
    #         self.add_video_item(path)
    #     self.update_default_output_path()

    # def change_output_location(self):
    #     # base_path = Path("F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage")  # ← your preferred default folder

    #     # if not base_path.exists():
    #     #     base_path = Path.home()  # fallback

    #     # default_name = self.output_file_path.name if self.output_file_path else "merged(MM-DD-YY)-R#.mp4"
    #     # file_dialog = QFileDialog(self.ui, "Select Output File")
    #     # file_dialog.setAcceptMode(QFileDialog.AcceptMode.AcceptSave)
    #     # file_dialog.setNameFilter("MP4 Video (*.mp4)")
    #     # file_dialog.setDirectory(str(base_path))
    #     # file_dialog.selectFile(default_name)

    #     if file_dialog.exec():
    #         selected_files = file_dialog.selectedFiles()
    #         if selected_files:
    #             selected = Path(selected_files[0])
    #             if selected.suffix.lower() != ".mp4":
    #                 selected = selected.with_suffix(".mp4")
    #             self.output_file_path = selected
    #             self.ui.output_label.setText(f"Output file: {self.output_file_path}")

    # def merge_files(self):
    #     count = self.ui.list_widget.count()
    #     if count < 2:
    #         QMessageBox.warning(self.ui, "Error", "Add at least 2 videos to merge.")
    #         return


    #     file_paths = [
    #         self.ui.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
    #         for i in range(count)
    #     ]

    #     self.ui.merge_btn.setEnabled(False)
    #     self.ui.progress_bar.setVisible(True)

    #     # self.merge_thread = MergeThread(file_paths, str(self.output_file_path))
    #     # self.merge_thread.finished.connect(self.merge_done)
    #     # self.merge_thread.error.connect(self.merge_error)
    #     # self.merge_thread.start()

    # def merge_done(self, output_file):
    #     self.ui.progress_bar.setVisible(False)
    #     self.ui.merge_btn.setEnabled(True)
    #     QMessageBox.information(self, "Done", f"Merged video saved as:\n{output_file}")

    # def merge_error(self, error_msg):
    #     self.ui.progress_bar.setVisible(False)
    #     self.ui.merge_btn.setEnabled(True)
    #     QMessageBox.critical(self, "Merge Error", error_msg)


    # def update_default_output_path(self):
    #     count = self.ui.list_widget.count()
    #     if count == 0:
    #         self.output_file_path = None
    #         self.ui.output_label.setText("Output file: (none)")
    #         return

    #     file_paths = [
    #         self.ui.list_widget.item(i).data(Qt.ItemDataRole.UserRole)
    #         for i in range(count)
    #     ]

    #     first_path = Path(file_paths[0])
    #     default_name = first_path.stem + "(MM-DD-YY)-R#.mp4"
    #     default_path = first_path.with_name(default_name)

    #     # Only update if user hasn't set a custom output path
    #     if self.output_file_path is None or not self.output_file_path.exists():
    #         self.output_file_path = default_path
    #         self.ui.output_label.setText(f"Output file: {self.output_file_path}")

    def dragEnterEvent(self, event):
        if event.mimeData().hasUrls():
            event.acceptProposedAction()

    def dropEvent(self, event):
        paths = [u.toLocalFile() for u in event.mimeData().urls()]
        mp4s = [p for p in paths if p.lower().endswith(".mp4")]
        for path in mp4s:
            self.add_video_item(path)
        # self.update_default_output_path()