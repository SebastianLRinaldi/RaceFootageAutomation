from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

from multiprocessing import Pool
import os
import subprocess
import tempfile
import cv2
import numpy as np
import math
from math import ceil

from PIL import ImageFont, ImageDraw, Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import traceback
import re
import cProfile

from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *



class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic'):
        super().__init__()
        self.logic = logic  # store the Logic instance

    def run(self):
        try:
            self.logic.make_timer_overlay()  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)


class Logic(QObject):
    # lap_started = pyqtSignal(int)
    # lap_progress = pyqtSignal(int, int)  # lap_number, percent
    # lap_finished = pyqtSignal(int)
    
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui
        self.project_directory = ProjectDirectory()
        self.lap_labels = {}
        # self.lap_started.connect(self.create_lap_label)
        # self.lap_progress.connect(self.update_lap_table)
        # self.lap_finished.connect(self.remove_lap_label)

        self.FRAME_WIDTH = 310
        self.FRAME_HEIGHT = 150
        self.fps = 59.94
        self.use_gpu = True

        self.end_duration = 15

        self.rendered_name = f"Timer_Overlay.mp4"
        self.asset_name = f"timer_temp.mp4"

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
        self.font_size = 64
        self.font = ImageFont.truetype(self.font_path, self.font_size)

        # self.max_time = 25.000
        # self.distance_from_center = 80
        # self.spacing = 70
        self.lap_fill_color = (255, 255, 255)
        self.timer_fill_color = (0, 255, 0)
        self.stats_fill_color = (0, 255, 0)


        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, self.FRAME_WIDTH),
            ("height", self.ui.height_input, self.FRAME_HEIGHT),
            ("fps", self.ui.fps_input, self.fps),
            ("use_gpu", self.ui.use_gpu_checkbox,self.use_gpu),

            ("end_duration", self.ui.end_duration_input, self.end_duration),

            ("rendered_name", self.ui.rendered_file_name, self.rendered_name),
            
            ("font_path", self.ui.font_path_input.layout.line_edit, self.font_path ),
            ("font_size", self.ui.font_size_input, self.font_size),
            

            # ("max_time", self.ui.max_time_input, self.max_time),
            # ("distance_from_center", self.ui.center_offset_input, self.distance_from_center),
            # ("spacing", self.ui.spacing_input, self.spacing),
            ("lap_fill_color", self.ui.lap_fill_color_input.logic, self.lap_fill_color),
            ("timer_fill_color", self.ui.timer_fill_color_input.logic, self.timer_fill_color),
            ("stats_fill_color", self.ui.stats_fill_color_input.logic, self.stats_fill_color),
        ]
        
        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, target=self, app="make_timer_overlay")

    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Timer Overlay...")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.progress.setFormat("Rendering... 0%")
        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        self.ui.generate_button.setEnabled(True)

        print(f"✅ Timer Overlay Video saved as {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        print(f'File "{self.project_directory.make_rendered_file_path(self.rendered_name)}"')
        self.ui.progress.setFormat("Ready")
        self.ui.progress.setValue(0)

    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.generate_button.setEnabled(True)
        self.ui.progress.setValue(0)

    def get_ffmpeg_cmd(self, concat_txt):
        base_cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-fps_mode", "cfr",
            "-r", str(self.fps),
            "-pix_fmt", "yuv420p",
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

    def concat_videos(self, file_list, output_file):
        # Create concat text file for ffmpeg
        concat_txt = os.path.join(os.path.dirname(output_file), "concat_list_timer_overlay.txt")
        with open(concat_txt, "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")

        # Usage example:
        cmd = self.get_ffmpeg_cmd(concat_txt=concat_txt)
        
        # subprocess.run(cmd, check=True)

        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)


        total_duration = sum(float(lap[1]) for lap in self.project_directory.lap_time_deltas)

        total_frames = int(float(total_duration) * self.fps)

        for line in process.stderr:
            QMetaObject.invokeMethod(
                self,
                "update_frame_status",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(str, line.strip())
            )

            frame_pattern = re.compile(r"frame=\s*(\d+)")  # matches "frame=12345"
            match = frame_pattern.search(line)
            if match:
                current_frame = int(match.group(1))
                QMetaObject.invokeMethod(
                    self,
                    "update_frame_progress",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(int, current_frame),
                    Q_ARG(int, total_frames)
                )
            
            QApplication.processEvents()  # make sure QLabel updates immediately

        process.wait()



    def create_timer_section(self, lap_number, temp_dir):
        """
                # time_elapsed = frame / self.fps
                # frame_idx = int(time_elapsed * self.fps)
                # if frame_idx >= len(timer_frames):
                #     frame_idx = len(timer_frames) - 1


            for frame in tqdm(range(total_frames), desc="Rendering timer video"):
                time_elapsed = frame / self.fps
                time_text = f"{time_elapsed:.3f} sec"
        """
        target_duration = self.project_directory.lap_time_deltas[lap_number][1]
        duration = target_duration
        
        frame_count = int(float(duration) * self.fps)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT))

        font = ImageFont.truetype(self.font_path, 64)
        text_color = (255,255,255)
        center_x = self.FRAME_WIDTH // 2
        center_y = self.FRAME_HEIGHT // 2
        
        try:
            # for frame in tqdm(range(frame_count), desc="Rendering timer video"):

            for frame in range(frame_count):
                time_elapsed = frame / self.fps
                text1 = f"Lap:{lap_number+1}"
                text2 = f"{time_elapsed:.3f} sec"

                # Create blank image for this frame
                img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
                pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
                draw = ImageDraw.Draw(pil_img)

                draw.text((center_x, center_y), text1 , font=font, fill=text_color, anchor="md")
                draw.text((center_x, center_y), text2, font=font, fill=text_color, anchor="ma")


                # Write frame to video
                frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
                writer.write(frame_bgr)
                
                percent = int(((frame + 1) / frame_count) * 100)

                QMetaObject.invokeMethod(
                    self,
                    "update_lap_table",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(int, lap_number),
                    Q_ARG(int, percent)
                )

        finally:
            writer.release()  # Ensure it's always released
            del writer


        return filename



    def make_timer_overlay(self):
        # Temp files deleted automatically on context exit
        with tempfile.TemporaryDirectory() as temp_dir:
            render_single = False
            
            lap_videos = []

            num_laps = len(self.project_directory.lap_time_deltas)

            # --- CREATE LAP TABLE ONCE ---
            QMetaObject.invokeMethod(
                self,
                "create_lap_table",
                Qt.ConnectionType.QueuedConnection,
                Q_ARG(int, num_laps)
            )

            
            if render_single:
                lap_video = self.create_timer_section( 3, temp_dir)
                lap_videos.append(lap_video)
            else:
                with ThreadPoolExecutor() as executor:
                    futures = {
                                executor.submit(self.create_timer_section, i , temp_dir): i
                                for i in range(len(self.project_directory.lap_time_deltas))
                            }

                    # for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                    #     lap_number = futures[future]
                    #     lap_videos.append(future.result())
                    

                    total = len(futures)
                    done = 0
                    for future in as_completed(futures):
                        lap_number = futures[future]
                        lap_videos.append(future.result())
                        done += 1
                        percent = int((done / total) * 100)
                        
                        # # update QWidgets from worker thread safely
                        QMetaObject.invokeMethod(
                            self,  # where `update_render_progress` is defined
                            "update_render_progress",
                            Qt.ConnectionType.QueuedConnection,
                            Q_ARG(int, percent)
                        )

            # Sort videos by lap number (they can complete out of order)
            lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

            # 3. Concatenate all videos: start_blank + lap videos
            self.concat_videos(lap_videos, self.rendered_name)

            # --- REMOVE LAP TABLE ---
            QMetaObject.invokeMethod(
                self,
                "remove_lap_table",
                Qt.ConnectionType.QueuedConnection
            )

    @pyqtSlot(int, int)
    def update_frame_progress(self, current:int, total:int):
        percent = int((current / total) * 100)
        self.ui.progress.setValue(percent)
        self.ui.progress.setFormat(f"Frame {current}/{total}")

    @pyqtSlot(str)
    def update_frame_status(self, text:str):
        self.ui.status_label.setText(text)
            
    @pyqtSlot(int)
    def update_render_progress(self, percent:int):
        self.ui.progress.setValue(percent)
        self.ui.progress.setFormat(f"Rendering... {percent:>3d}%")

    @pyqtSlot(int)
    def create_lap_table(self, num_laps):
        table = QTableWidget(num_laps, 2)  # 2 columns now
        table.setHorizontalHeaderLabels(["Lap", "Progress"])
        self.ui.layout().addWidget(table)
        self.lap_table = table

        # initialize rows
        for i in range(num_laps):
            table.setItem(i, 0, QTableWidgetItem(f"Lap {i+1}"))   # name column
            table.setItem(i, 1, QTableWidgetItem("0%"))            # progress column

    @pyqtSlot(int, int)
    def update_lap_table(self, lap_number, percent):
        item = self.lap_table.item(lap_number, 1)  # second column
        if item:
            item.setText(f"{percent}%")

    @pyqtSlot()
    def remove_lap_table(self):
        if hasattr(self, "lap_table") and self.lap_table is not None:
            self.ui.layout().removeWidget(self.lap_table)  # remove from layout
            self.lap_table.deleteLater()                    # schedule for deletion
            self.lap_table = None    