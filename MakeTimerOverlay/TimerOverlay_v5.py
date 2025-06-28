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

import cProfile

# Config
WIDTH = 800
HEIGHT = 600
MAX_TIME = 25.000  # seconds

FPS = 59.94
USE_GPU = True
START_DURATION = 5  # seconds blank start screen
END_DURATION = 15  # seconds hold last frame
OUTPUT_VIDEO_FILE = "Timer_Overlay_(6-20-25)-R2.mp4"
OUTPUT_COUNTUP_TIMER = "timer_temp.mp4"

FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 64


import sys
sys.path.append("F:/_Small/344 School Python/TrackFootageEditor")
from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times, best_lap_deltas

LAP_TIMES = get_racer_times("F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv", "EpicX18 GT9")


FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

DISTANCE_FROM_CENTER = 80


TEXT_POSITIONS = {
    "lap": {"x": WIDTH // 2, "y": HEIGHT // 2 - DISTANCE_FROM_CENTER, "fill": (255, 255, 255)},
    "timer": {"x": WIDTH // 2, "y": HEIGHT // 2 , "fill": (0, 255, 0)},
    "stats": {"start_y": HEIGHT // 2-DISTANCE_FROM_CENTER, "spacing": 70, "fill": (0, 255, 0)},
}


def draw_centered_text(draw, text, pos=TEXT_POSITIONS):
    fill = pos["fill"]
    x = pos.get("x", WIDTH // 2)
    
    if isinstance(text, list):
        start_y = pos["start_y"]
        spacing = pos["spacing"]
        for i, text in enumerate(text):
            text_bbox = FONT.getbbox(text)
            text_w = text_bbox[2] - text_bbox[0]
            text_h = text_bbox[3] - text_bbox[1]
            y = start_y + i * spacing
            draw.text((x - text_w // 2, y), text, font=FONT, fill=fill)
    else:
        text_bbox = FONT.getbbox(text)
        text_w = text_bbox[2] - text_bbox[0]
        y = pos["y"]
        draw.text((x - text_w // 2, y), text, font=FONT, fill=fill)

def draw_center_cross_hair(draw):
    # Red crosshair lines
    red = (255, 0, 0)
    center_x = WIDTH // 2
    center_y = HEIGHT // 2
    # Horizontal line
    draw.line([(0, center_y), (WIDTH, center_y)], fill=red, width=5)

    # Vertical line
    draw.line([(center_x, 0), (center_x, HEIGHT)], fill=red, width=5)

    # Middle dot
    dot_radius = 5
    draw.ellipse([
        (center_x - dot_radius, center_y - dot_radius),
        (center_x + dot_radius, center_y + dot_radius)
    ], fill=red)



def generate_timer_video():
    total_frames = int(MAX_TIME * FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(OUTPUT_COUNTUP_TIMER, fourcc, FPS, (WIDTH, HEIGHT), True)

    for frame in tqdm(range(total_frames), desc="Rendering timer video"):
        time_elapsed = frame / FPS
        time_text = f"{time_elapsed:.3f} sec"
        # time_text = f"{time_elapsed:06.3f} sec"

        img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)

        draw_centered_text(draw, time_text, TEXT_POSITIONS["timer"])

        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()

def preload_timer_frames():
    cap = cv2.VideoCapture(OUTPUT_COUNTUP_TIMER)
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
def create_lap_overlay(lap_number):
    lap_text = f"Lap {lap_number:02}"

    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # black bg
    draw = ImageDraw.Draw(img)

    draw_centered_text(draw, lap_text, TEXT_POSITIONS["lap"])
    
    # Convert once to numpy BGR for direct overlay
    overlay = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return overlay



def create_lap_overlay_and_mask(lap_number):
    lap_overlay = create_lap_overlay(lap_number)
    lap_mask = np.any(lap_overlay != 0, axis=2).astype(np.uint8) * 255  # mask 0 or 255 for OpenCV
    return lap_overlay, lap_mask

def render_frame(lap_overlay, lap_mask, time_elapsed, timer_frames):
    frame_idx = int(time_elapsed * FPS)
    if frame_idx >= len(timer_frames):
        frame_idx = len(timer_frames) - 1

    base_frame = timer_frames[frame_idx].copy()

    # Use OpenCV copyTo with mask - much faster than numpy boolean indexing
    cv2.copyTo(lap_overlay, lap_mask, base_frame)

    return base_frame

def render_lap_video(lap_number, lap_time, temp_dir, timer_frames):
    filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))

    lap_overlay, lap_mask = create_lap_overlay_and_mask(lap_number)

    frame_count = math.floor(FPS * lap_time) + 1
    for f in tqdm(range(frame_count), desc=f"Rendering Lap {lap_number}"):
        t = f / FPS
        frame = render_frame(lap_overlay, lap_mask, t, timer_frames)
        writer.write(frame)

    writer.release()
    return filename


def create_end_stats(duration, filename):
    frame_count = int(duration * FPS)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT), True)

    # Create a styled stats frame using PIL
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    draw_stats(draw)

    frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    for _ in range(frame_count):
        writer.write(frame_bgr)

    writer.release()


def draw_stats(draw):
    avg = sum(LAP_TIMES) / len(LAP_TIMES)
    best = min(LAP_TIMES)
    worst = max(LAP_TIMES)
    diff = worst - best

    stats = [
        f"Avg:   {avg:.3f} sec",
        f"Best:  {best:.3f} sec",
        f"Worst: {worst:.3f} sec",
        f"Δ:     {diff:.3f} sec"
    ]

    draw_centered_text(draw, stats, TEXT_POSITIONS["stats"])



def create_blank_video(duration, filename):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    blank = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame_count = int(FPS* duration)
    for _ in range(frame_count):
        writer.write(blank)
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
    concat_txt = os.path.join(os.path.dirname(output_file), "concat_list_timer_overlay.txt")
    with open(concat_txt, "w") as f:
        for file in file_list:
            f.write(f"file '{file}'\n")

    # Usage example:
    cmd = get_ffmpeg_cmd(concat_txt=concat_txt)
    subprocess.run(cmd, check=True)


def main():
    # rerender_input = input("Rerender: Timer Counter? [Y/n]: ")
    # if rerender_input.strip().lower() in ('y', 'yes', ''):
    generate_timer_video()

    # Setup once
    timer_frames = preload_timer_frames()

    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Create start blank video
        start_blank = os.path.join(temp_dir, "start_blank.mp4")
        print("Creating Blank")
        create_blank_video(START_DURATION, start_blank)

        end_stats = os.path.join(temp_dir, "end_stats.mp4")
        print("Creating STATS")
        create_end_stats(END_DURATION, end_stats)

        # 2. Render laps in parallel
        lap_videos = []
        render_single = False
        
        if render_single:
            lap_video = render_lap_video(1, LAP_TIMES[1], temp_dir, timer_frames)
            lap_videos.append(lap_video)
        else:
            with ThreadPoolExecutor() as executor:
                futures = {
                            executor.submit(render_lap_video, i + 1, lap_time, temp_dir, timer_frames): i + 1
                            for i, lap_time in enumerate(LAP_TIMES)
                        }

                for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                    lap_number = futures[future]
                    lap_videos.append(future.result())



        # Sort videos by lap number (they can complete out of order)
        lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

        # 3. Concatenate all videos: start_blank + lap videos
        concat_videos(lap_videos + [end_stats], OUTPUT_VIDEO_FILE)

        # Temp files deleted automatically on context exit
        print(f"✅ Timer Overlay Video saved as {OUTPUT_VIDEO_FILE}")


# if __name__ == "__main__":
#     main()
#     # cProfile.run('main()')


from PyQt6.QtWidgets import QApplication, QPushButton, QVBoxLayout, QWidget, QLabel
from PyQt6.QtCore import Qt
import sys



class TimerOverlayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Timer Overlay Generator")
        self.setGeometry(100, 100, 400, 200)

        self.label = QLabel("Click to generate timer overlay", self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.button = QPushButton("Generate Timer Overlay", self)
        self.button.clicked.connect(self.run_overlay_generation)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.button)
        self.setLayout(layout)

    def run_overlay_generation(self):
        self.label.setText("Generating... Please wait.")
        self.button.setEnabled(False)
        try:
            main()
            self.label.setText("✅ Done. Overlay saved.")
        except Exception as e:
            self.label.setText(f"❌ Error: {str(e)}")
        finally:
            self.button.setEnabled(True)

if __name__ == '__main__':
    app = QApplication(sys.argv)
    window = TimerOverlayApp()
    window.show()
    sys.exit(app.exec())
