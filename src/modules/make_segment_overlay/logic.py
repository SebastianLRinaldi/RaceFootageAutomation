from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *

import os
import subprocess
import cv2
import numpy as np
import math
from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm
import traceback

from src.helper_functions import *
from src.helper_classes import *
from .layout import Layout

from src.components import *


# # Config
# WIDTH = 1920
# HEIGHT = 120
# FPS = 59.94
# OUTPUT_DIR = "SegmentOverlayFiles(MM-DD-YY)"

# """
# python -m MakeSegmentOverlay.SegmentOverlay_v0
# """

# # Filenames
# BAR_FILE = "bar_overlay.mp4"
# DOT_FILE = "dot_overlay.mp4"
# DOT_AVI_FILE = "dot_overlay.avi"
# os.makedirs(OUTPUT_DIR, exist_ok=True)
# BAR_OVERLAY = f"{OUTPUT_DIR}/{BAR_FILE}"
# DOT_OVERLAY = f"{OUTPUT_DIR}/{DOT_FILE}"
# SEGMENT_OVERLAY = f"{OUTPUT_DIR}/Segment_Overlay_(6-20-25)-R2.mp4"

# # ffmpeg exe path if needed
# FFMPEG_BIN = "ffmpeg"  # Change if you need an absolute path



# END_DURATION = 15  # seconds hold last frame
# FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
# FONT_SIZE = 24
# FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# # Lap times
# import sys
# sys.path.append("F:/_Small/344 School Python/TrackFootageEditor")
# from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times

# LAP_TIMES = get_racer_times("F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv", "EpicX18 GT9")






class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic'):
        super().__init__()
        self.logic = logic  # store the Logic instance

    def run(self):
        try:
            self.logic.run_ffmpeg_overlay()  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)


class Logic():
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()


        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, int, 1920),
            ("height", self.ui.height_input, int, 1080),
            ("fps", self.ui.fps_input, float, 59.94),
            ("output_dir", self.ui.output_dir_input.layout.line_edit, str, f"{self.project_directory.module_path}"),

            ("end_duration", self.ui.end_duration_input, int, 15),
            ("font_path", self.ui.font_path_input.layout.line_edit, str, "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"),
            ("font_size", self.ui.font_size_input, int, 24),
            
            ("bar_file_name", self.ui.bar_file_name, str, "bar_overlay.mp4"),
            ("dot_file_name", self.ui.dot_file_name, str, "dot_overlay.mp4"),
            ("dot_avi_file_name", self.ui.dot_avi_file_name, str, "dot_overlay.avi"),
            ("segment_overlay_rendered_name", self.ui.segment_overlay_rendered_name, str, "Segment_Overlay_Project_Name.mp4"),

            ("ffmpeg_bin", self.ui.ffmpeg_bin_input.layout.line_edit, str, "ffmpeg"),
        ]


        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, app="SegmentOverlayApp")



        cfg = read_settings(SETTINGS_FIELDS)

        self.width = int(cfg["width"])
        self.height = int(cfg["height"])
        self.fps = float(cfg["fps"])
        self.project_directory.module_path = cfg["output_dir"]
        

        self.end_duration = int(cfg["end_duration"])
        self.font_path = cfg["font_path"]
        self.font_size = int(cfg["font_size"])
        
        self.bar_file_name = cfg["bar_file_name"]
        self.dot_file_name = cfg["dot_file_name"]
        self.dot_avi_file_name = cfg["dot_avi_file_name"]
        self.rendered_name = cfg["segment_overlay_rendered_name"]


        self.ffmpeg_bin = cfg["ffmpeg_bin"]

        self.font = ImageFont.truetype(self.font_path, self.font_size)

    def set_project_name(self, project_name):
        self.project_directory.project_name = project_name

    def set_root(self, path):
        self.project_directory.module_path = path
        set_widget_value(self.ui.output_dir_input.layout.line_edit, self.project_directory.module_path)
        
    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Segment Overlay...")

        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: RENDER PATH GOES HERE")
        self.ui.generate_button.setEnabled(True)

    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.generate_button.setEnabled(True)


    # --- Bar Overlay ---
    def create_bar_overlay_frame(self, lap_done_idx):
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        y_pos = self.height // 2

        y_top = y_pos - 60
        y_bottom = y_pos + 60

        total_time = sum(self.project_directory.lap_times)
        segment_length = [ (lap / total_time) * self.width for lap in self.project_directory.lap_times ]
        
        accum_length = 0
        for i, lap_time in enumerate(self.project_directory.lap_times):
            prev_time = self.project_directory.lap_times[i - 1] if i > 0 else lap_time

            # Grey if lap not done yet
            if i >= lap_done_idx:
                color = (100, 100, 100)
                text_color = (200, 200, 200)
            else:
                if i == 0:
                    color = (0, 180, 0)
                    text_color = (255, 255, 255)
                else:
                    if lap_time < prev_time:
                        color = (0, 180, 0)
                        text_color = (255, 255, 255)
                    else:
                        color = (200, 0, 0)
                        text_color = (255, 255, 255)

            start_x = int(accum_length)
            end_x = int(accum_length + segment_length[i])

            draw.rectangle([start_x, y_top, end_x, y_bottom], fill=color)


            if i >= lap_done_idx:
                # Draw seperator lines
                draw.line([(start_x, y_top), (start_x, y_bottom)], fill=(255, 255, 0), width=2)
                draw.line([(end_x, y_top), (end_x, y_bottom)], fill=(255, 255, 0), width=2)
            else:

                # Draw seperator lines
                draw.line([(start_x, y_top), (start_x, y_bottom)], fill=(255, 255, 0), width=2)
                draw.line([(end_x, y_top), (end_x, y_bottom)], fill=(255, 255, 0), width=2)

                # Calculate and draw lap time difference text
                diff = 0 if i == 0 else lap_time - prev_time
                diff_text = f"{diff:+.3f}"


                bbox = draw.textbbox((0,0), diff_text, font=self.font)
                text_width = bbox[2] - bbox[0]
                text_height = bbox[3] - bbox[1]
                
                text_x = start_x + (end_x - start_x - text_width) // 2
                text_y = y_pos - text_height // 2

                draw.text((text_x, text_y), diff_text, fill=text_color, font=self.font)



            accum_length += segment_length[i]

        return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    def save_bar_video(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        file_path = self.project_directory.make_asset_path(self.bar_file_name)
        
        writer = cv2.VideoWriter(file_path, fourcc, self.fps, (self.width, self.height))
        total_duration_sec = sum(self.project_directory.lap_times)+self.end_duration  # Total duration is sum of laps

        bar_overlay_imgs = []
        for lap_idx in range(len(self.project_directory.lap_times) + 1):  # +1 to have final frame with all colored
            img = self.create_bar_overlay_frame(lap_idx)
            bar_overlay_imgs.append(img)

        frame_count = int(self.fps * total_duration_sec)
        lap_cumulative_times = np.cumsum(self.project_directory.lap_times)

        for frame_idx in tqdm(range(frame_count), desc="Saving bar overlay video"):
            current_time_sec = frame_idx / self.fps

            # Find current lap index (number of laps finished)
            lap_done_idx = np.searchsorted(lap_cumulative_times, current_time_sec, side='right')

            # Cap index to available images
            lap_done_idx = min(lap_done_idx, len(bar_overlay_imgs) - 1)

            # Write correct overlay image
            writer.write(bar_overlay_imgs[lap_done_idx])

        writer.release()


    # --- Dot Overlay ---
    def create_dot_overlay_frame_trans(self, progress):
        radius = 15
        img = Image.new("RGBA", (self.width, self.height), (0, 0, 0))  # no alpha channel here
        draw = ImageDraw.Draw(img)
        y_pos = self.height // 2
        x_pos = int(progress * self.width)
        bbox = [x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius]
        draw.ellipse(bbox, fill=(255, 255, 255))
        return np.array(img)

    def save_dot_video_trans(self):
        total_duration_sec = sum(self.project_directory.lap_times) + self.end_duration  # Total duration is sum of laps
        file_path = self.project_directory.make_asset_path(self.dot_avi_file_name)
        
        fourcc = cv2.VideoWriter_fourcc(*'RGBA')
        writer = cv2.VideoWriter(file_path, fourcc, self.fps, (self.width, self.height))
        
        frame_count = int(self.fps * total_duration_sec)
        for f in tqdm(range(frame_count), desc="Saving dot overlay trans video"):
            progress = f / frame_count
            frame_rgb = self.create_dot_overlay_frame_trans(progress)
            writer.write(frame_rgb)
        writer.release()

    def create_dot_overlay_frame_reg(self,progress):
        radius = 15
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))  # no alpha channel here
        draw = ImageDraw.Draw(img)
        y_pos = self.height // 2
        x_pos = int(progress * self.width)

        # Draw a vertical white line (thickness 3)
        line_width = 2
        draw.line([(x_pos, 0), (x_pos, self.height)], fill=(255, 255, 255), width=line_width)

        return np.array(img)

    def save_dot_video_reg(self):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        file_path = self.project_directory.make_asset_path(self.bar_file_name)
        
        writer = cv2.VideoWriter(file_path, fourcc, self.fps, (self.width, self.height))
        total_duration_sec = sum(self.project_directory.lap_times)+self.end_duration  # Total duration is sum of laps
        
        frame_count = int(self.fps * total_duration_sec)
        for f in tqdm(range(frame_count), desc="Saving dot overlay reg video"):
            progress = f / frame_count
            frame_rgb = self.create_dot_overlay_frame_reg(progress)
            writer.write(frame_rgb)
        writer.release()

    def time_to_x_pos_frame(self, frame_idx, total_frames):
        total_time = sum(self.project_directory.lap_times)
        segment_lengths = [(lap / total_time) * self.width for lap in self.project_directory.lap_times]
        lap_cumulative_times = np.cumsum(self.project_directory.lap_times)

        progress = frame_idx / total_frames
        t = progress * total_time

        lap_idx = np.searchsorted(lap_cumulative_times, t, side='right')

        x_pos = sum(segment_lengths[:lap_idx])

        if lap_idx < len(self.project_directory.lap_times):
            segment_start_time = lap_cumulative_times[lap_idx - 1] if lap_idx > 0 else 0
            segment_time = self.project_directory.lap_times[lap_idx]
            segment_progress = (t - segment_start_time) / segment_time
            x_pos += segment_progress * segment_lengths[lap_idx]

        return x_pos

    def vertical_line_overlay(self, current_time_sec):
        total_time = sum(self.project_directory.lap_times)
        
        # Calculate accumulated pixel lengths (same as bar)
        segment_length = [ (lap / total_time) * self.width for lap in self.project_directory.lap_times ]
        
        accum_length = 0
        for i, lap_time in enumerate(self.project_directory.lap_times):
            start_time = sum(self.project_directory.lap_times[:i])
            end_time = start_time + lap_time

            if current_time_sec <= end_time:
                # Inside this segment, interpolate position
                segment_progress = (current_time_sec - start_time) / lap_time if lap_time > 0 else 0
                x_pos = int(accum_length + segment_progress * segment_length[i])
                break
            accum_length += segment_length[i]
        else:
            # If time exceeds total, put line at the very end
            x_pos = self.width - 1
        
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.line([(x_pos, 0), (x_pos, self.height)], fill=(255, 255, 255), width=2)
        return np.array(img)

    def save_dot_video_sync(self ):
        file_path = self.project_directory.make_asset_path(self.dot_file_name)
        total_duration_sec = sum(self.project_directory.lap_times)+self.end_duration  # Total duration is sum of laps
        
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(file_path, fourcc, self.fps, (self.width, self.height))

        frame_count = int(self.fps * total_duration_sec)
        for frame_idx in tqdm(range(frame_count), desc="Saving dot overlay reg video"):
            current_time_sec = frame_idx / self.fps  # exact current time
            frame_rgb = self.vertical_line_overlay(current_time_sec)
            writer.write(frame_rgb)
        writer.release()

    def make_dot_and_bar(self):

        print("Creating bar overlay...")
        self.save_bar_video()

        print("Creating dot overlay...")
        self.save_dot_video_sync()


    def run_ffmpeg_overlay(self):
        print(f"TIMES: {self.project_directory.lap_times}")
        self.make_dot_and_bar()
        
        cmd = [
            self.ffmpeg_bin, "-y",
            "-i", self.project_directory.make_asset_path(self.bar_file_name),
            "-i", self.project_directory.make_asset_path(self.dot_file_name),
            "-filter_complex", "[1:v]colorkey=0x000000:0.1:0.0[ckout];[0:v][ckout]overlay=shortest=1",
            "-c:v", "libx264", "-crf", "18", "-preset", "fast",
            # "-c:v", "h264_nvenc",
            # "-preset", "fast",   # NVENC presets
            
            "-rc", "vbr",
            "-cq", "18", 
            self.project_directory.module_path
        ]
        print("Running ffmpeg overlay...")
        subprocess.run(cmd, check=True)
        print(f"✅ Overlay done: {self.project_directory.module_path}")

