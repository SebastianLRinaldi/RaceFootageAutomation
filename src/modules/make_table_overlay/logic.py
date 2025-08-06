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



from .layout import Layout
from src.components import *
from src.helpers import *


# Configs
# Canvas dimensions and padding
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

FPS = 59.94
USE_GPU = True
START_DURATION = 5
END_DURATION = 15
OUTPUT_VIDEO_FILE = "Table_Overlay_(6-20-25)-R2.mp4"



FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 64

# from application.apps.raceStats.functions.racerTimersStats import get_racer_times, best_lap_deltas
import sys
sys.path.append("F:/_Small/344 School Python/TrackFootageEditor")
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










class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui


        SETTINGS_FIELDS = [
            ("canvas_width", self.ui.canvas_width_input, int, 1920),
            ("canvas_height", self.ui.canvas_height_input, int, 1080),

            ("padding_top", self.ui.padding_top_input, int, 10),
            ("padding_bottom", self.ui.padding_bottom_input, int, 10),
            ("padding_left", self.ui.padding_left_input, int, 10),
            ("padding_right", self.ui.padding_right_input, int, 10),

            ("fps", self.ui.fps_input, float, 59.94),
            ("use_gpu", self.ui.use_gpu_checkbox, bool, True),

            ("start_duration", self.ui.start_duration_input, int, 5),
            ("end_duration", self.ui.end_duration_input, int, 15),

            ("output_video_file", self.ui.output_video_file_input.logic, str, "Table_Overlay_(6-20-25)-R2.mp4"),
            ("font_path", self.ui.font_path_input.logic, str, r"C:\Users\epics\AppData\Local\Microsoft\Windows\Fonts\NIS-Heisei-Mincho-W9-Condensed.TTF"),
            ("font_size", self.ui.font_size_input, int, 64),
        ]

        # In __init__ or setup:
        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, app="make_table_overlay")
        self.settings_handler.load()
        self.settings_handler.connect_autosave()



    def pick_output_file(self):
        suggested_path = Path("F:/GoProExports")
        default_name = "LapOverlay.mp4"

        path, _ = QFileDialog.getSaveFileName(self, "Choose Output File", str(suggested_path / default_name), "MP4 files (*.mp4)")
        if path:
            if not path.lower().endswith(".mp4"):
                path += ".mp4"
            self.output_file = path
            self.status_label.setText(f"Output: {path}")
            self.generate_button.setEnabled(True)

    def generate_overlay(self):
        self.status_label.setText("Rendering overlay...")
        self.generate_button.setEnabled(False)
        self.progress.setVisible(True)

        self.thread = OverlayThread(self.output_file)
        self.thread.finished.connect(self.on_done)
        self.thread.error.connect(self.on_error)
        self.thread.start()

    def on_done(self, file):
        self.status_label.setText(f"Done: {file}")
        self.progress.setVisible(False)
        self.generate_button.setEnabled(True)
        QMessageBox.information(self, "Success", f"Overlay saved to: {file}")

    def on_error(self, msg):
        self.status_label.setText("Error")
        self.progress.setVisible(False)
        self.generate_button.setEnabled(True)
        QMessageBox.critical(self, "Failed", msg)

    font_cache = {}
    def get_font(font_size):
        if font_size not in font_cache:
            font_cache[font_size] = ImageFont.truetype(FONTPATH, font_size)
        return font_cache[font_size]

    def draw_centered_text_pil(img, text, x, y, font_size, color):
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        font = get_font(font_size)
        bbox = draw.textbbox((0, 0), text, font=font)
        text_w = bbox[2] - bbox[0]
        text_h = bbox[3] - bbox[1]
        position = (int(x - text_w / 2), int(y - text_h / 2))
        draw.text(position, text, font=font, fill=color)
        return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    def draw_table(img, x, y, data_rows):
        total_rows = len(data_rows) + 1  # +1 for header
        available_height = img.shape[0] - y - PADDING['bottom']
        row_h = max(ROW_HEIGHT_MIN, min(ROW_HEIGHT_MAX, available_height // total_rows))

        font_size_header = int(row_h * 0.8)
        font_size_row = int(row_h * 0.7)

        # Draw header row
        col_x = x
        for i, header in enumerate(HEADERS):
            center_x = col_x + COL_WIDTHS[i] // 2
            img = draw_centered_text_pil(img, header, center_x, y + row_h // 2, font_size_header, WHITE)
            col_x += COL_WIDTHS[i]
        cv2.rectangle(img, (x, y), (x + TABLE_WIDTH, y + row_h), WHITE, 1)
        # Vertical lines in header
        col_x = x
        for width in COL_WIDTHS[:-1]:
            col_x += width
            cv2.line(img, (col_x, y), (col_x, y + row_h), WHITE, 1)

        # Draw data rows
        for i, row in enumerate(data_rows):
            top = y + row_h * (i + 1)
            cv2.rectangle(img, (x, top), (x + TABLE_WIDTH, top + row_h), WHITE, 1)
            col_x = x
            for j, cell in enumerate(row):
                center_x = col_x + COL_WIDTHS[j] // 2
                text = f"{cell}" if cell is not None else "N/A"
                img = draw_centered_text_pil(img, text, center_x, top + row_h // 2, font_size_row, WHITE)
                col_x += COL_WIDTHS[j]
            # vertical lines
            col_x = x
            for width in COL_WIDTHS[:-1]:
                col_x += width
                cv2.line(img, (col_x, top), (col_x, top + row_h), WHITE, 1)

        return img


    def create_blank_video(duration, filename):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))
        blank = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
        frame_count = int(FPS* duration)
        for _ in range(frame_count):
            writer.write(blank)
        writer.release()





    def draw_headers():
        # Header only
        img = draw_table(
            img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
            x=TABLE_X,
            y=TABLE_Y,
            data_rows=[]
        )

        return img

    def create_headers_video(duration, filename):
        frame_count = int(duration * FPS)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT), True)

        # Create a styled stats frame using PIL
        # img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        # draw = ImageDraw.Draw(img)
        img = draw_headers()
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in range(frame_count):
            writer.write(frame_bgr)

        writer.release()








    def get_ffmpeg_cmd(concat_txt):
        base_cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-fps_mode", "cfr",
            "-r", str(FPS),
            "-pix_fmt", "yuv420p",
            OUTPUT_VIDEO_FILE
        ]

        if USE_GPU:
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






    def concat_videos(file_list, output_file):
        # Create concat text file for ffmpeg
        concat_txt = os.path.join(os.path.dirname(output_file), "concat_list_table_overlay.txt")
        with open(concat_txt, "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")

        # Usage example:
        cmd = get_ffmpeg_cmd(concat_txt=concat_txt)
        subprocess.run(cmd, check=True)









    def create_lap_table(lap_number, target_lap, temp_dir):
        current_laps = LAP_TIMES[:lap_number]
        current_data = []

        for idx, current_lap in enumerate(current_laps):
            lap = idx + 1
            time_str = f"{current_lap[0]}"
            delta = f"{current_lap[1]}"
            current_data.append([lap, time_str, delta])

        duration = float(target_lap[0])
        frame_count = int(duration * FPS)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))


        img = draw_table(
                img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
                x=TABLE_X,
                y=TABLE_Y,
                data_rows=current_data
            )
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
            writer.write(frame_bgr)

        writer.release()
        return filename



    def create_last_lap_table(lap_number, temp_dir):
        current_laps = LAP_TIMES[:lap_number]
        current_data = []

        for idx, current_lap in enumerate(current_laps):
            lap = idx + 1
            time_str = f"{current_lap[0]}"
            delta = f"{current_lap[1]}"
            current_data.append([lap, time_str, delta])

        # duration = float(target_lap[0])
        frame_count = int(END_DURATION * FPS)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, FPS, (FRAME_WIDTH, FRAME_HEIGHT))


        img = draw_table(
                img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
                x=TABLE_X,
                y=TABLE_Y,
                data_rows=current_data
            )
        
        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
            writer.write(frame_bgr)

        writer.release()
        return filename













    def main():


        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create start blank video
            start_blank = os.path.join(temp_dir, "start_blank.mp4")
            print("Creating Blank")
            create_blank_video(START_DURATION, start_blank)
            # create_headers_video(END_DURATION, filename)
            last_lap_video = create_last_lap_table(len(LAP_TIMES), temp_dir)
            # 2. Render laps in parallel
            lap_videos = [last_lap_video]

            render_single = False


            # for i, target_lap in enumerate(LAP_TIMES):
            #     lap_videos.append(create_lap_table( i , target_lap, temp_dir))
            
            if render_single:
                lap_video = create_lap_table( 1, LAP_TIMES[1], temp_dir)
                lap_videos.append(lap_video)
            else:
                with ThreadPoolExecutor() as executor:
                    futures = {
                                executor.submit(create_lap_table, i , target_lap, temp_dir): i
                                for i, target_lap in enumerate(LAP_TIMES)
                            }

                    for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                        lap_number = futures[future]
                        lap_videos.append(future.result())



            # Sort videos by lap number (they can complete out of order)
            lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

            # 3. Concatenate all videos: start_blank + lap videos
            concat_videos(lap_videos, OUTPUT_VIDEO_FILE)

            # Temp files deleted automatically on context exit
            print(f"✅ Timer Overlay Video saved as {OUTPUT_VIDEO_FILE}")