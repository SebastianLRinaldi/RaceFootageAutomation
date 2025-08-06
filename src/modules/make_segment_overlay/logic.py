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

from .layout import Layout
# from src.components import YourNeededLayoutLogicConnection
from src.helpers import *
from src.components import *


# Config
WIDTH = 1920
HEIGHT = 120
FPS = 59.94
OUTPUT_DIR = "SegmentOverlayFiles(MM-DD-YY)"

"""
python -m MakeSegmentOverlay.SegmentOverlay_v0
"""

# Filenames
BAR_FILE = "bar_overlay.mp4"
DOT_FILE = "dot_overlay.mp4"
DOT_AVI_FILE = "dot_overlay.avi"
os.makedirs(OUTPUT_DIR, exist_ok=True)
BAR_OVERLAY = f"{OUTPUT_DIR}/{BAR_FILE}"
DOT_OVERLAY = f"{OUTPUT_DIR}/{DOT_FILE}"
SEGMENT_OVERLAY = f"{OUTPUT_DIR}/Segment_Overlay_(6-20-25)-R2.mp4"

# ffmpeg exe path if needed
FFMPEG_BIN = "ffmpeg"  # Change if you need an absolute path



END_DURATION = 15  # seconds hold last frame
FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 24
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Lap times
import sys
sys.path.append("F:/_Small/344 School Python/TrackFootageEditor")
# from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times

# LAP_TIMES = get_racer_times("F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv", "EpicX18 GT9")



# --- Bar Overlay ---
def create_bar_overlay_frame(lap_done_idx):
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    y_pos = HEIGHT // 2

    y_top = y_pos - 60
    y_bottom = y_pos + 60

    total_time = sum(LAP_TIMES)
    segment_length = [ (lap / total_time) * WIDTH for lap in LAP_TIMES ]
    
    accum_length = 0
    for i, lap_time in enumerate(LAP_TIMES):
        prev_time = LAP_TIMES[i - 1] if i > 0 else lap_time

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


            bbox = draw.textbbox((0,0), diff_text, font=FONT)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            
            text_x = start_x + (end_x - start_x - text_width) // 2
            text_y = y_pos - text_height // 2

            draw.text((text_x, text_y), diff_text, fill=text_color, font=FONT)



        accum_length += segment_length[i]

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

def save_bar_video(filename, duration_sec):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))

    bar_overlay_imgs = []
    for lap_idx in range(len(LAP_TIMES) + 1):  # +1 to have final frame with all colored
        img = create_bar_overlay_frame(lap_idx)
        bar_overlay_imgs.append(img)

    frame_count = int(FPS * duration_sec)
    lap_cumulative_times = np.cumsum(LAP_TIMES)

    for frame_idx in tqdm(range(frame_count), desc="Saving bar overlay video"):
        current_time_sec = frame_idx / FPS

        # Find current lap index (number of laps finished)
        lap_done_idx = np.searchsorted(lap_cumulative_times, current_time_sec, side='right')

        # Cap index to available images
        lap_done_idx = min(lap_done_idx, len(bar_overlay_imgs) - 1)

        # Write correct overlay image
        writer.write(bar_overlay_imgs[lap_done_idx])

    writer.release()


# --- Dot Overlay ---
def create_dot_overlay_frame_trans(progress):
    radius = 15
    img = Image.new("RGBA", (WIDTH, HEIGHT), (0, 0, 0))  # no alpha channel here
    draw = ImageDraw.Draw(img)
    y_pos = HEIGHT // 2
    x_pos = int(progress * WIDTH)
    bbox = [x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius]
    draw.ellipse(bbox, fill=(255, 255, 255))
    return np.array(img)

def save_dot_video_trans(filename, duration_sec):
    fourcc = cv2.VideoWriter_fourcc(*'RGBA')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    frame_count = int(FPS * duration_sec)
    for f in tqdm(range(frame_count), desc="Saving dot overlay trans video"):
        progress = f / frame_count
        frame_rgb = create_dot_overlay_frame_trans(progress)
        writer.write(frame_rgb)
    writer.release()

def create_dot_overlay_frame_reg(progress):
    radius = 15
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # no alpha channel here
    draw = ImageDraw.Draw(img)
    y_pos = HEIGHT // 2
    x_pos = int(progress * WIDTH)

    # Draw a vertical white line (thickness 3)
    line_width = 2
    draw.line([(x_pos, 0), (x_pos, HEIGHT)], fill=(255, 255, 255), width=line_width)

    return np.array(img)

def save_dot_video_reg(filename, duration_sec):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    frame_count = int(FPS * duration_sec)
    for f in tqdm(range(frame_count), desc="Saving dot overlay reg video"):
        progress = f / frame_count
        frame_rgb = create_dot_overlay_frame_reg(progress)
        writer.write(frame_rgb)
    writer.release()

def time_to_x_pos_frame(frame_idx, total_frames):
    total_time = sum(LAP_TIMES)
    segment_lengths = [(lap / total_time) * WIDTH for lap in LAP_TIMES]
    lap_cumulative_times = np.cumsum(LAP_TIMES)

    progress = frame_idx / total_frames
    t = progress * total_time

    lap_idx = np.searchsorted(lap_cumulative_times, t, side='right')

    x_pos = sum(segment_lengths[:lap_idx])

    if lap_idx < len(LAP_TIMES):
        segment_start_time = lap_cumulative_times[lap_idx - 1] if lap_idx > 0 else 0
        segment_time = LAP_TIMES[lap_idx]
        segment_progress = (t - segment_start_time) / segment_time
        x_pos += segment_progress * segment_lengths[lap_idx]

    return x_pos

def vertical_line_overlay(current_time_sec):
    total_time = sum(LAP_TIMES)
    
    # Calculate accumulated pixel lengths (same as bar)
    segment_length = [ (lap / total_time) * WIDTH for lap in LAP_TIMES ]
    
    accum_length = 0
    for i, lap_time in enumerate(LAP_TIMES):
        start_time = sum(LAP_TIMES[:i])
        end_time = start_time + lap_time

        if current_time_sec <= end_time:
            # Inside this segment, interpolate position
            segment_progress = (current_time_sec - start_time) / lap_time if lap_time > 0 else 0
            x_pos = int(accum_length + segment_progress * segment_length[i])
            break
        accum_length += segment_length[i]
    else:
        # If time exceeds total, put line at the very end
        x_pos = WIDTH - 1
    
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw.line([(x_pos, 0), (x_pos, HEIGHT)], fill=(255, 255, 255), width=2)
    return np.array(img)

def save_dot_video_sync(filename, duration_sec):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    frame_count = int(FPS * duration_sec)
    
    for frame_idx in tqdm(range(frame_count), desc="Saving dot overlay reg video"):
        current_time_sec = frame_idx / FPS  # exact current time
        frame_rgb = vertical_line_overlay(current_time_sec)
        writer.write(frame_rgb)
    writer.release()


# total_duration_sec = sum(LAP_TIMES)+END_DURATION  # Total duration is sum of laps

# bar_file = os.path.join(OUTPUT_DIR, BAR_FILE)
# dot_file_reg = os.path.join(OUTPUT_DIR, DOT_FILE)
# dot_file_trans = os.path.join(OUTPUT_DIR, DOT_AVI_FILE)
# print("Creating bar overlay...")
# save_bar_video(bar_file, total_duration_sec)

# print("Creating dot overlay...")
# save_dot_video_sync(dot_file_reg, total_duration_sec)


def run_ffmpeg_overlay(bar_overlay, dot_overlay, out_file):
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", bar_overlay,
        "-i", dot_overlay,
        "-filter_complex", "[1:v]colorkey=0x000000:0.1:0.0[ckout];[0:v][ckout]overlay=shortest=1",
        # "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        "-c:v", "h264_nvenc",
        "-preset", "fast",   # NVENC presets
        "-rc", "vbr",
        "-cq", "18", 
        out_file
    ]
    print("Running ffmpeg overlay...")
    subprocess.run(cmd, check=True)
    print(f"✅ Overlay done: {out_file}")


class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str)

    def run(self):
        try:
            run_ffmpeg_overlay(BAR_OVERLAY, DOT_OVERLAY, SEGMENT_OVERLAY)
            self.finished.emit()
        except Exception as e:
            self.error.emit(str(e))



class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui

        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, int, 1920),
            ("height", self.ui.height_input, int, 1080),
            ("fps", self.ui.fps_input, float, 59.94),
            ("output_dir", self.ui.output_dir_input.layout.line_edit, str, ""),
            ("bar_file", self.ui.bar_file_input.layout.line_edit, str, ""),
            ("dot_file", self.ui.dot_file_input.layout.line_edit, str, ""),
            ("dot_avi_file", self.ui.dot_avi_file_input.layout.line_edit, str, ""),
            ("segment_overlay_file", self.ui.segment_overlay_file_input.layout.line_edit, str, ""),
            ("end_duration", self.ui.end_duration_input, int, 15),
            ("font_path", self.ui.font_path_input.layout.line_edit, str, ""),
            ("font_size", self.ui.font_size_input, int, 24),
            ("ffmpeg_bin", self.ui.ffmpeg_bin_input.layout.line_edit, str, "ffmpeg"),
        ]


        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, app="SegmentOverlayApp")
        self.settings_handler.load()
        self.settings_handler.connect_autosave()



        
    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Processing...")

        self.worker = OverlayWorker()
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {SEGMENT_OVERLAY}")
        self.ui.generate_button.setEnabled(True)

    def on_error(self, msg):
        QMessageBox.critical(self, "Error", msg)
        self.ui.status_label.setText("❌ Failed")
        self.ui.generate_button.setEnabled(True)

