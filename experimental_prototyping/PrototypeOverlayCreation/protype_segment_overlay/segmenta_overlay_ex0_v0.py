import os
import cv2
import numpy as np
import math
from PIL import ImageFont, ImageDraw, Image
from tqdm import tqdm

# Config
WIDTH = 800
HEIGHT = 200
FPS = 59.94
OUTPUT_DIR = "overlays"
os.makedirs(OUTPUT_DIR, exist_ok=True)

FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 32
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)

# Lap times
LAP_TIMES = [23.715, 22.728, 22.784, 22.75, 23.901, 23.076, 22.719, 22.742, 23.345,
             22.614, 22.423, 23.725, 22.988, 22.766, 22.386, 22.592, 22.322, 22.796,
             22.49, 22.315, 22.473, 22.187, 22.221]

# --- Bar Overlay ---
def create_bar_overlay():
    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    y_pos = HEIGHT // 2

    total_time = sum(LAP_TIMES)
    segment_length = [ (lap / total_time) * WIDTH for lap in LAP_TIMES ]
    

    accum_length = 0
    for i, lap_time in enumerate(LAP_TIMES):
        prev_time = LAP_TIMES[i - 1] if i > 0 else lap_time
        color = (0, 255, 0) if lap_time < prev_time else (255, 0, 0)
        start_x = int(accum_length)
        end_x = int(accum_length + segment_length[i])
        draw.rectangle([start_x, y_pos - 20, end_x, y_pos + 20], fill=color)

        # Draw cyan lines at start and end
        draw.line([(start_x, 0), (start_x, HEIGHT)], fill=(0, 255, 255), width=2)
        draw.line([(end_x, 0), (end_x, HEIGHT)], fill=(0, 255, 255), width=2)

        
        accum_length += segment_length[i]

    return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# def create_bar_overlay():
#     img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
#     draw = ImageDraw.Draw(img)
#     y_pos = HEIGHT // 2
#     segment_length = WIDTH / len(LAP_TIMES)

#     for i, lap_time in enumerate(LAP_TIMES):
#         prev_time = LAP_TIMES[i - 1] if i > 0 else lap_time
#         color = (0, 255, 0) if lap_time < prev_time else (255, 0, 0)
#         start_x = i * segment_length
#         end_x = (i + 1) * segment_length
#         draw.rectangle([start_x, y_pos - 20, end_x, y_pos + 20], fill=color)

#         # Draw cyan lines at start and end
#         draw.line([(start_x, 0), (start_x, HEIGHT)], fill=(0, 255, 255), width=2)
#         draw.line([(end_x, 0), (end_x, HEIGHT)], fill=(0, 255, 255), width=2)

#     return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


def save_bar_video(filename, duration_sec):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    bar_overlay = create_bar_overlay()
    frame_count = int(FPS * duration_sec)
    for _ in tqdm(range(frame_count), desc="Saving bar overlay video"):
        writer.write(bar_overlay)
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


    
    # bbox = [x_pos - radius, y_pos - radius, x_pos + radius, y_pos + radius]
    # draw.ellipse(bbox, fill=(255, 255, 255))
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





"""
Because AVI with 'RGBA' FourCC is basically uncompressed raw frames, 
it just dumps pixel data straight to disk with minimal CPU overhead. 
No compression means less CPU time spent encoding, so it's faster.

Meanwhile, 'mp4v' (MPEG-4) is a compressed codec. 
Compression is CPU-intensive — encoding each frame takes time, 
which slows down the saving process.

So:

AVI + RGBA: Fast, heavy on disk space, minimal CPU usage.

MP4 + mp4v: Slow(er), saves disk space, heavy CPU encoding load.

If speed matters and you have enough disk space, uncompressed AVI is often faster. 
If you want smaller files and can afford the encoding time, MP4 is better.
"""
total_duration_sec = sum(LAP_TIMES)  # Total duration is sum of laps

bar_file = os.path.join(OUTPUT_DIR, "bar_overlay.mp4")
dot_file_reg = os.path.join(OUTPUT_DIR, "dot_overlay.mp4")
dot_file_trans = os.path.join(OUTPUT_DIR, "dot_overlay.avi")
print("Creating bar overlay...")
save_bar_video(bar_file, total_duration_sec)

# print("Creating dot overlay...")
# save_dot_video_reg(dot_file_reg, total_duration_sec)
# save_dot_video_trans(dot_file_trans, total_duration_sec)
# print("✅ Done — overlays saved to:", OUTPUT_DIR)


import os
import subprocess

# Filenames
START_BLANK = "start_blank.mp4"
BAR_OVERLAY = "overlays/bar_overlay.mp4"
DOT_OVERLAY = "overlays/dot_overlay.mp4"
SEGMENT_OVERLAY = "overlays/segment_overlay.mp4"
END_STATS = "end_stats.mp4"
FINAL_OUTPUT = "final_full_video.mp4"
CONCAT_LIST_TXT = "overlays/concat_list.txt"

# ffmpeg exe path if needed
FFMPEG_BIN = "ffmpeg"  # Change if you need an absolute path

def run_ffmpeg_overlay(bar_overlay, dot_overlay, out_file):
    cmd = [
        FFMPEG_BIN, "-y",
        "-i", bar_overlay,
        "-i", dot_overlay,
        "-filter_complex", "[1:v]colorkey=0x000000:0.1:0.0[ckout];[0:v][ckout]overlay=shortest=1",
        "-c:v", "libx264", "-crf", "18", "-preset", "fast",
        out_file
    ]
    print("Running ffmpeg overlay...")
    subprocess.run(cmd, check=True)
    print(f"✅ Overlay done: {out_file}")

def create_concat_list_file(file_list, concat_txt):
    concat_dir = os.path.dirname(concat_txt)
    with open(concat_txt, "w") as f:
        for file in file_list:
            relative_path = os.path.relpath(file, start=concat_dir)
            f.write(f"file '{relative_path}'\n")
    print(f"✅ Wrote concat list: {concat_txt}")

def run_ffmpeg_concat(concat_txt, out_file):
    cmd = [
        FFMPEG_BIN, "-y",
        "-f", "concat", "-safe", "0",
        "-i", concat_txt,
        "-c:v", "libx264", "-crf", "18", "-preset", "slow",
        out_file
    ]
    print("Running ffmpeg concat...")
    subprocess.run(cmd, check=True)
    print(f"✅ Final video saved: {out_file}")

def main():
    # 1️⃣ Step: Overlay bar + dot → segment_overlay.mp4
    run_ffmpeg_overlay(BAR_OVERLAY, DOT_OVERLAY, SEGMENT_OVERLAY)

    # # 2️⃣ Step: Write concat_list.txt
    # file_list = [
    #     SEGMENT_OVERLAY,
    # ]
    # create_concat_list_file(file_list, CONCAT_LIST_TXT)

    # # 3️⃣ Step: Run concat → final_full_video.mp4
    # run_ffmpeg_concat(CONCAT_LIST_TXT, FINAL_OUTPUT)

if __name__ == "__main__":
    main()


