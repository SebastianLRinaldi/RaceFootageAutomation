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

        self.width = 1920
        self.height = 120
        self.fps = 59.94
        
        self.end_duration = 15

        self.bar_file_name = "bar_overlay.mp4"
        self.dot_file_name = "dot_overlay.mp4"
        self.dot_avi_file_name = "dot_overlay.avi"
        self.rendered_name = f"Segment_Overlay.mp4"


        self.ffmpeg_bin = "ffmpeg"

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
        self.font_size = 24
        self.font = ImageFont.truetype(self.font_path, self.font_size)

        
        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, self.width),
            ("height", self.ui.height_input, self.height),
            ("fps", self.ui.fps_input, self.fps),

            ("end_duration", self.ui.end_duration_input, self.end_duration),
            ("font_path", self.ui.font_path_input.layout.line_edit, self.font_path ),
            ("font_size", self.ui.font_size_input, self.font_size),
            
            ("bar_file_name", self.ui.bar_file_name, self.bar_file_name),
            ("dot_file_name", self.ui.dot_file_name, self.dot_file_name),
            ("dot_avi_file_name", self.ui.dot_avi_file_name, self.dot_avi_file_name),
            ("rendered_name", self.ui.rendered_file_name, self.rendered_name),

            ("ffmpeg_bin", self.ui.ffmpeg_bin_input.layout.line_edit, self.ffmpeg_bin),
        ]


        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, target=self, app="SegmentOverlayApp")

    def set_project_name(self, project_name):
        self.project_directory.project_name = project_name

    def set_root(self, path):
        self.project_directory.module_path = path
        
    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Segment Overlay...")

        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
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
        file_path = self.project_directory.make_asset_file_path(self.bar_file_name)
        
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
        file_path = self.project_directory.make_asset_file_path(self.dot_avi_file_name)
        
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
        file_path = self.project_directory.make_asset_file_path(self.bar_file_name)
        
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
        file_path = self.project_directory.make_asset_file_path(self.dot_file_name)
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
        bar_file = self.project_directory.make_asset_file_path(self.bar_file_name)
        dot_file = self.project_directory.make_asset_file_path(self.dot_file_name)

        if not os.path.isfile(bar_file):
            print("Creating bar overlay...")
            self.save_bar_video()
        if not os.path.isfile(dot_file):
            print("Creating dot overlay...")
            self.save_dot_video_sync()


    def run_ffmpeg_overlay(self):
        self.make_dot_and_bar()


        # cmd = [
        #     self.ffmpeg_bin, "-y",
        #     "-i", self.project_directory.make_asset_path(self.bar_file_name),
        #     "-i", self.project_directory.make_asset_path(self.dot_file_name),
        #     "-filter_complex", "[1:v]colorkey=0x000000:0.1:0.0[ckout];[0:v][ckout]overlay=shortest=1",
        #     "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        #     # "-c:v", "h264_nvenc",
        #     # "-preset", "fast",   # NVENC presets
            
        #     "-rc", "vbr",
        #     "-cq", "18", 
        #     self.project_directory.make_rendered_path(self.rendered_name),
        # ]

        """CPU ONLY"""
        cmd = [
            self.ffmpeg_bin, "-y",
            "-i", self.project_directory.make_asset_file_path(self.bar_file_name),
            "-i", self.project_directory.make_asset_file_path(self.dot_file_name),
            "-filter_complex", "[1:v]colorkey=0x000000:0.1:0.2[ckout];[0:v][ckout]overlay=shortest=1",
            "-c:v", "libx264",
            "-crf", "18",
            "-preset", "fast",
            "-pix_fmt", "yuv420p",
            self.project_directory.make_rendered_file_path(self.rendered_name),
        ]

        # """GPU ONLY"""

        # filter_complex = (
        #     "[0:v]hwupload_cuda,scale_cuda={width}:{height}[base];"
        #     "[1:v]hwupload_cuda[ckin];"
        #     "[base][ckin]overlay_cuda=shortest=1"
        # ).format(width=self.width, height=self.height)

        # cmd = [
        #     self.ffmpeg_bin, "-y",
        #     "-i", self.project_directory.make_asset_file_path(self.bar_file_name),
        #     "-i", self.project_directory.make_asset_file_path(self.dot_file_name),
        #     # "-filter_complex", filter_complex,
        #     "-filter_complex", "[1:v]colorkey=0x000000:0.1:0.2[ckout];[0:v][ckout]overlay=shortest=1",
        #     "-c:v", "h264_nvenc",
        #     "-preset", "fast",
        #     "-rc", "vbr",
        #     "-cq", "18",
        #     "-pix_fmt", "yuv420p",
        #     self.project_directory.make_rendered_file_path(self.rendered_name),
        # ]



        
        print("Running ffmpeg overlay...")
        subprocess.run(cmd, check=True)
        print(f"✅ Overlay done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")

