from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


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


from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *


# Configs
# Canvas dimensions and padding
# CANVAS_WIDTH = 1920
# CANVAS_HEIGHT = 1080

# FPS = 59.94
# USE_GPU = True
# START_DURATION = 5
# END_DURATION = 15
# OUTPUT_VIDEO_FILE = "Table_Overlay_(6-20-25)-R2.mp4"



# FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
# FONT_SIZE = 64

# from application.apps.raceStats.functions.racerTimersStats import get_racer_times, best_lap_deltas
# import sys
# sys.path.append("F:/_Small/344 School Python/TrackFootageEditor")
# from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times, best_lap_deltas




# times = get_racer_times("F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv", "EpicX18 GT9")

# LAP_TIMES = best_lap_deltas(times)



# # Dynamic headers and column widths - add more columns here
# HEADERS = ["Lap", "Time", "Best Lap Diff"]  
# COL_WIDTHS = [100, 200, 220]

# ROW_HEIGHT_MIN = 20
# ROW_HEIGHT_MAX = 40

# PADDING = {
#     'top': 10,
#     'bottom': 10,
#     'left': 10,
#     'right': 10
# }

# # Computed constants
# TOTAL_ROWS = len(LAP_TIMES) + 1
# TABLE_WIDTH = sum(COL_WIDTHS)
# FRAME_WIDTH = TABLE_WIDTH + PADDING['left'] + PADDING['right']
# FRAME_HEIGHT = (TOTAL_ROWS * ROW_HEIGHT_MAX) + PADDING['top'] + PADDING['bottom']

# TABLE_X = PADDING['left']
# TABLE_Y = PADDING['top']

# WHITE = (255, 255, 255)


class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic'):
        super().__init__()
        self.logic = logic  # store the Logic instance

    def run(self):
        try:
            self.logic.make_table_overlay()  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()


        self.width = 1920
        self.height = 1080
        self.fps = 59.94
        self.use_gpu = True

        self.start_duration = 5
        self.end_duration = 15


        self.padding_top = 10
        self.padding_bottom = 10
        self.padding_left = 10
        self.padding_right = 10

        self.rendered_name = f"Table_Overlay.mp4"

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
        self.font_size = 64
        self.font = ImageFont.truetype(self.font_path, self.font_size)


        # Dynamic headers and column widths - add more columns here
        self.HEADERS = ["Lap", "Time", "Best Lap Diff"]  
        self.COL_WIDTHS = [100, 200, 220]

        self.ROW_HEIGHT_MIN = 20
        self.ROW_HEIGHT_MAX = 40

        self.PADDING = {
            'top': 10,
            'bottom': 10,
            'left': 10,
            'right': 10
        }

        # Computed constants
        self.TOTAL_ROWS = len(self.project_directory.lap_times) + 1
        self.TABLE_WIDTH = sum(self.COL_WIDTHS)
        self.FRAME_WIDTH = self.TABLE_WIDTH + self.PADDING['left'] + self.PADDING['right']
        self.FRAME_HEIGHT = (self.TOTAL_ROWS * self.ROW_HEIGHT_MAX) + self.PADDING['top'] + self.PADDING['bottom']

        self.TABLE_X = self.PADDING['left']
        self.TABLE_Y = self.PADDING['top']

        self.WHITE = (255, 255, 255)

        


        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, int, self.width),
            ("height", self.ui.height_input, int, self.height),
            ("fps", self.ui.fps_input, float, self.fps),
            ("use_gpu", self.ui.use_gpu_checkbox, bool, self.use_gpu),

            ("padding_top", self.ui.padding_top_input, int, self.padding_top),
            ("padding_bottom", self.ui.padding_bottom_input, int, self.padding_bottom),
            ("padding_left", self.ui.padding_left_input, int, self.padding_left),
            ("padding_right", self.ui.padding_right_input, int, self.padding_right),

            ("start_duration", self.ui.start_duration_input, int, self.start_duration),
            ("end_duration", self.ui.end_duration_input, int, self.end_duration),

            ("rendered_name", self.ui.rendered_file_name, str, self.rendered_name),
            ("font_path", self.ui.font_path_input.layout.line_edit, str, self.font_path ),
            ("font_size", self.ui.font_size_input, int, self.font_size),
        ]

        # In __init__ or setup:
        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, app="make_table_overlay")

    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Table Overlay...")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        self.ui.generate_button.setEnabled(True)

    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.generate_button.setEnabled(True)

    def draw_centered_text_pil(self, img, text, x, y, font_size, color):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        font = self.font
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        position = (int(x - text_w / 2), int(y - text_h / 2))
        draw.text(position, text, font=font, fill=color)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    def draw_table(self, img, x, y, data_rows):
        total_rows = len(data_rows) + 1  # +1 for header
        available_height = img.shape[0] - y - self.PADDING['bottom']
        row_h = max(self.ROW_HEIGHT_MIN, min(self.ROW_HEIGHT_MAX, available_height // total_rows))

        font_size_header = int(row_h * 0.8)
        font_size_row = int(row_h * 0.7)

        # Draw header row
        col_x = x
        for i, header in enumerate(self.HEADERS):
            center_x = col_x + self.COL_WIDTHS[i] // 2
            img = self.draw_centered_text_pil(img, header, center_x, y + row_h // 2, font_size_header, self.WHITE)
            col_x += self.COL_WIDTHS[i]
        cv2.rectangle(img, (x, y), (x + self.TABLE_WIDTH, y + row_h), self.WHITE, 1)
        # Vertical lines in header
        col_x = x
        for width in self.COL_WIDTHS[:-1]:
            col_x += width
            cv2.line(img, (col_x, y), (col_x, y + row_h), self.WHITE, 1)

        # Draw data rows
        for i, row in enumerate(data_rows):
            top = y + row_h * (i + 1)
            cv2.rectangle(img, (x, top), (x + self.TABLE_WIDTH, top + row_h), self.WHITE, 1)
            col_x = x
            for j, cell in enumerate(row):
                center_x = col_x + self.COL_WIDTHS[j] // 2
                text = f"{cell}" if cell is not None else "N/A"
                img = self.draw_centered_text_pil(img, text, center_x, top + row_h // 2, font_size_row, self.WHITE)
                col_x += self.COL_WIDTHS[j]
            # vertical lines
            col_x = x
            for width in self.COL_WIDTHS[:-1]:
                col_x += width
                cv2.line(img, (col_x, top), (col_x, top + row_h), self.WHITE, 1)

        return img

    def create_blank_video(self, duration, filename):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT))
        blank = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
        frame_count = int(self.fps* duration)
        for _ in range(frame_count):
            writer.write(blank)
        writer.release()

    def draw_headers(self):
        # Header only
        img = self.draw_table(
            img=np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8),
            x=self.TABLE_X,
            y=self.TABLE_Y,
            data_rows=[]
        )

        return img

    def create_headers_video(self, duration, filename):
        frame_count = int(duration * self.fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT), True)

        # Create a styled stats frame using PIL
        # img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        # draw = ImageDraw.Draw(img)
        img = self.draw_headers()
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in range(frame_count):
            writer.write(frame_bgr)

        writer.release()

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
            self.project_directory.make_rendered_file_path(self.rendered_name),
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
        concat_txt = os.path.join(os.path.dirname(output_file), "concat_list_table_overlay.txt")
        with open(concat_txt, "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")

        # Usage example:
        cmd = self.get_ffmpeg_cmd(concat_txt=concat_txt)
        subprocess.run(cmd, check=True)

    def create_lap_table(self, lap_number, target_lap, temp_dir):
        current_laps = self.project_directory.lap_time_deltas[:lap_number]
        current_data = []

        for idx, current_lap in enumerate(current_laps):
            lap = idx + 1
            time_str = f"{current_lap[0]}"
            delta = f"{current_lap[1]}"
            current_data.append([lap, time_str, delta])

        duration = float(target_lap[0])
        frame_count = int(duration * self.fps)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT))


        img = self.draw_table(
                img=np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8),
                x=self.TABLE_X,
                y=self.TABLE_Y,
                data_rows=current_data
            )
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
            writer.write(frame_bgr)

        writer.release()
        return filename

    def create_last_lap_table(self, lap_number, temp_dir):
        print(f"lap_number: {lap_number}")
        current_laps = self.project_directory.lap_time_deltas[:lap_number]
        current_data = []

        print(f"current_laps: {current_laps}")
        

        for idx, current_lap in enumerate(current_laps):
            print(current_lap)
            lap = idx + 1
            time_str = f"{current_lap[0]}"
            delta = f"{current_lap[1]}"
            current_data.append([lap, time_str, delta])

        # duration = float(target_lap[0])
        frame_count = int(self.end_duration * self.fps)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT))


        img = self.draw_table(
                img=np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8),
                x=self.TABLE_X,
                y=self.TABLE_Y,
                data_rows=current_data
            )
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
            writer.write(frame_bgr)

        writer.release()
        return filename

    def make_table_overlay(self):

        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create start blank video
            start_blank = os.path.join(temp_dir, "start_blank.mp4")
            print("Creating Blank")
            self.create_blank_video(self.start_duration, start_blank)
            # create_headers_video(END_DURATION, filename)
            
            print(f"lap_timed{self.project_directory.lap_times}")
            print(f"lap_time_deltas{self.project_directory.lap_time_deltas}")

            print(f"len(lap_time_deltas)={len(self.project_directory.lap_time_deltas)} | len(lap_times)={len(self.project_directory.lap_times)}")
            last_lap_video = self.create_last_lap_table(len(self.project_directory.lap_times), temp_dir)
            # 2. Render laps in parallel
            lap_videos = [last_lap_video]

            render_single = False

            # for i, target_lap in enumerate(LAP_TIMES):
            #     lap_videos.append(create_lap_table( i , target_lap, temp_dir))
            
            if render_single:
                lap_video = self.create_lap_table( 1, self.project_directory.lap_time_deltas[1], temp_dir)
                lap_videos.append(lap_video)
            else:
                with ThreadPoolExecutor() as executor:
                    futures = {
                                executor.submit(self.create_lap_table, i , target_lap, temp_dir): i
                                for i, target_lap in enumerate(self.project_directory.lap_time_deltas)
                            }

                    for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                        lap_number = futures[future]
                        lap_videos.append(future.result())

            # Sort videos by lap number (they can complete out of order)
            lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

            # 3. Concatenate all videos: start_blank + lap videos
            self.concat_videos(lap_videos, self.rendered_name)

            # Temp files deleted automatically on context exit
            print(f"✅ Timer Overlay Video saved as {self.rendered_name}")