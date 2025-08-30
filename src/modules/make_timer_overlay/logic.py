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

import cProfile

from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *

# # Config
# WIDTH = 800
# HEIGHT = 600
# MAX_TIME = 25.000  # seconds

# FPS = 59.94
# USE_GPU = True
# START_DURATION = 5  # seconds blank start screen
# END_DURATION = 15  # seconds hold last frame
# OUTPUT_VIDEO_FILE = "Timer_Overlay_(6-20-25)-R2.mp4"
# OUTPUT_COUNTUP_TIMER = "timer_temp.mp4"

# FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
# FONT_SIZE = 64


# import sys
# sys.path.append("F:/_Small/344 School Python/TrackFootageEditor")
# from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times, best_lap_deltas

# LAP_TIMES = get_racer_times("F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv", "EpicX18 GT9")


# FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# DISTANCE_FROM_CENTER = 80


# TEXT_POSITIONS = {
#     "lap": {"x": WIDTH // 2, "y": HEIGHT // 2 - DISTANCE_FROM_CENTER, "fill": (255, 255, 255)},
#     "timer": {"x": WIDTH // 2, "y": HEIGHT // 2 , "fill": (0, 255, 0)},
#     "stats": {"start_y": HEIGHT // 2-DISTANCE_FROM_CENTER, "spacing": 70, "fill": (0, 255, 0)},
# }

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


class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()

        self.width = 800
        self.height  = 600
        self.fps = 59.94
        self.use_gpu = True

        self.start_duration = 5
        self.end_duration = 15

        self.rendered_name = f"Timer_Overlay.mp4"
        self.asset_name = f"timer_temp.mp4"

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
        self.font_size = 64
        self.font = ImageFont.truetype(self.font_path, self.font_size)


        self.max_time = 25.000
        self.distance_from_center = 80
        self.spacing = 70
        self.lap_fill_color = (255, 255, 255)
        self.timer_fill_color = (0, 255, 0)
        self.stats_fill_color = (0, 255, 0)


        # self.text_positions = {
        #     "lap": {"x": self.width // 2, "y": self.width  // 2 - self.distance_from_center, "fill": self.lap_fill_color},
        #     "timer": {"x": self.width  // 2, "y": self.width  // 2 , "fill": self.timer_fill_color},
        #     "stats": {"start_y": self.width  // 2-self.distance_from_center, "spacing": 70, "fill": self.stats_fill_color},
        # }



        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, self.width),
            ("height", self.ui.height_input, self.height),
            ("fps", self.ui.fps_input, self.fps),
            ("use_gpu", self.ui.use_gpu_checkbox,self.use_gpu),

            ("start_duration", self.ui.start_duration_input, self.start_duration),
            ("end_duration", self.ui.end_duration_input, self.end_duration),

            ("rendered_name", self.ui.rendered_file_name, self.rendered_name),
            
            ("font_path", self.ui.font_path_input.layout.line_edit, self.font_path ),
            ("font_size", self.ui.font_size_input, self.font_size),
            

            ("max_time", self.ui.max_time_input, self.max_time),
            ("distance_from_center", self.ui.center_offset_input, self.distance_from_center),
            ("spacing", self.ui.spacing_input, self.spacing),
            ("lap_fill_color", self.ui.lap_fill_color_input.logic, self.lap_fill_color),
            ("timer_fill_color", self.ui.timer_fill_color_input.logic, self.timer_fill_color),
            ("stats_fill_color", self.ui.stats_fill_color_input.logic, self.stats_fill_color),
        ]
        
        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, target=self, app="make_timer_overlay")

    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Timer Overlay...")
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

    def draw_centered_text(self, draw, text, pos):
        fill = pos["fill"]
        x = pos.get("x", self.width // 2)
        
        if isinstance(text, list):
            start_y = pos["start_y"]
            spacing = pos["spacing"]
            for i, text in enumerate(text):
                text_bbox = self.font.getbbox(text)
                text_w = text_bbox[2] - text_bbox[0]
                text_h = text_bbox[3] - text_bbox[1]
                y = start_y + i * spacing
                draw.text((x - text_w // 2, y), text, font=self.font, fill=fill)
        else:
            text_bbox = self.font.getbbox(text)
            text_w = text_bbox[2] - text_bbox[0]
            y = pos["y"]
            draw.text((x - text_w // 2, y), text, font=self.font, fill=fill)

    def draw_center_cross_hair(self, draw):
        # Red crosshair lines
        red = (255, 0, 0)
        center_x = self.width // 2
        center_y = self.height // 2
        # Horizontal line
        draw.line([(0, center_y), (self.width, center_y)], fill=red, width=5)

        # Vertical line
        draw.line([(center_x, 0), (center_x, self.height)], fill=red, width=5)

        # Middle dot
        dot_radius = 5
        draw.ellipse([
            (center_x - dot_radius, center_y - dot_radius),
            (center_x + dot_radius, center_y + dot_radius)
        ], fill=red)



    def generate_timer_video(self):
        total_frames = int(self.max_time * self.fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(self.asset_name, fourcc, self.fps, (self.width, self.height), True)

        for frame in tqdm(range(total_frames), desc="Rendering timer video"):
            time_elapsed = frame / self.fps
            time_text = f"{time_elapsed:.3f} sec"
            # time_text = f"{time_elapsed:06.3f} sec"

            img = Image.new("RGB", (self.width, self.height), (0, 0, 0))  # Black background
            draw = ImageDraw.Draw(img)

            txt_pos = {"x": self.width  // 2, "y": self.width  // 2 , "fill": self.timer_fill_color}

            self.draw_centered_text(draw, time_text, txt_pos)

            frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
            out.write(frame_bgr)

        out.release()

    def preload_timer_frames(self):
        cap = cv2.VideoCapture(self.asset_name)
        frames = []
        while True:
            ret, frame = cap.read()
            if not ret:
                break
            frames.append(frame)
        cap.release()
        return frames


    """
    v3 7-20sec
    """
    def create_lap_overlay(self, lap_number):
        lap_text = f"Lap {lap_number:02}"

        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))  # black bg
        draw = ImageDraw.Draw(img)

        txt_info = {"x": self.width // 2, "y": self.width  // 2 - self.distance_from_center, "fill": self.lap_fill_color}

        self.draw_centered_text(draw, lap_text, txt_info)
        
        # Convert once to numpy BGR for direct overlay
        overlay = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        return overlay



    def create_lap_overlay_and_mask(self, lap_number):
        lap_overlay = self.create_lap_overlay(lap_number)
        lap_mask = np.any(lap_overlay != 0, axis=2).astype(np.uint8) * 255  # mask 0 or 255 for OpenCV
        return lap_overlay, lap_mask

    def render_frame(self, lap_overlay, lap_mask, time_elapsed, timer_frames):
        frame_idx = int(time_elapsed * self.fps)
        if frame_idx >= len(timer_frames):
            frame_idx = len(timer_frames) - 1

        base_frame = timer_frames[frame_idx].copy()

        # Use OpenCV copyTo with mask - much faster than numpy boolean indexing
        cv2.copyTo(lap_overlay, lap_mask, base_frame)

        return base_frame

    def render_lap_video(self, lap_number, lap_time, temp_dir, timer_frames):
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))

        lap_overlay, lap_mask = self.create_lap_overlay_and_mask(lap_number)

        frame_count = math.floor(self.fps * lap_time) + 1
        for f in tqdm(range(frame_count), desc=f"Rendering Lap {lap_number}"):
            t = f / self.fps
            frame = self.render_frame(lap_overlay, lap_mask, t, timer_frames)
            writer.write(frame)

        writer.release()
        return filename


    def create_end_stats(self, duration, filename):
        frame_count = int(duration * self.fps)
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height), True)

        # Create a styled stats frame using PIL
        img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        self.draw_stats(draw)

        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

        for _ in range(frame_count):
            writer.write(frame_bgr)

        writer.release()


    def draw_stats(self, draw):
        avg = sum(self.project_directory.lap_times) / len(self.project_directory.lap_times)
        best = min(self.project_directory.lap_times)
        worst = max(self.project_directory.lap_times)
        diff = worst - best

        stats = [
            f"Avg:   {avg:.3f} sec",
            f"Best:  {best:.3f} sec",
            f"Worst: {worst:.3f} sec",
            f"Δ:     {diff:.3f} sec"
        ]

        txt_pos = {"start_y": self.width  // 2-self.distance_from_center, "spacing": self.spacing, "fill": self.stats_fill_color}

        self.draw_centered_text(draw, stats, txt_pos)



    def create_blank_video(self, duration, filename):
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height))
        blank = np.zeros((self.height, self.width, 3), dtype=np.uint8)
        frame_count = int(self.fps* duration)
        for _ in range(frame_count):
            writer.write(blank)
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
        if concat_txt is None:
            raise AttributeError(f"EMPTY CONCAT TEXT")

        
        with open(concat_txt, "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")

        # Usage example:
        cmd = self.get_ffmpeg_cmd(concat_txt=concat_txt)
        subprocess.run(cmd, check=True)


    def make_timer_overlay(self):
        # rerender_input = input("Rerender: Timer Counter? [Y/n]: ")
        # if rerender_input.strip().lower() in ('y', 'yes', ''):
        print(self)
        
        self.generate_timer_video()

        # Setup once
        timer_frames = self.preload_timer_frames()

        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create start blank video
            start_blank = os.path.join(temp_dir, "start_blank.mp4")
            print("Creating Blank")
            self.create_blank_video(self.start_duration, start_blank)

            end_stats = os.path.join(temp_dir, "end_stats.mp4")
            print("Creating STATS")
            self.create_end_stats(self.end_duration, end_stats)

            # 2. Render laps in parallel
            lap_videos = []
            render_single = False
            
            if render_single:
                lap_video = self.render_lap_video(1, self.project_directory.lap_times[1], temp_dir, timer_frames)
                lap_videos.append(lap_video)
            else:
                with ThreadPoolExecutor() as executor:
                    futures = {
                                executor.submit(self.render_lap_video, i + 1, lap_time, temp_dir, timer_frames): i + 1
                                for i, lap_time in enumerate(self.project_directory.lap_times)
                            }

                    for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                        lap_number = futures[future]
                        lap_videos.append(future.result())



            # Sort videos by lap number (they can complete out of order)
            lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

            # 3. Concatenate all videos: start_blank + lap videos
            self.concat_videos(lap_videos + [end_stats], self.rendered_name)

            # Temp files deleted automatically on context exit
            print(f"✅ Timer Overlay Video saved as {self.rendered_name}")


    # def run_overlay_generation(self):
    #     self.ui.label.setText("Generating... Please wait.")
    #     self.ui.generate_button.setEnabled(False)
    #     try:
    #         main()
    #         self.ui.label.setText("✅ Done. Overlay saved.")
    #     except Exception as e:
    #         self.ui.label.setText(f"❌ Error: {str(e)}")
    #     finally:
    #         self.ui.generate_button.setEnabled(True)