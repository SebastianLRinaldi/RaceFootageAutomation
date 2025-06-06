import os
import subprocess
import tempfile
import cv2
import numpy as np
import math

from PIL import ImageFont, ImageDraw, Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm

# Config

WIDTH, HEIGHT = 1920, 1080

FPS = 59.94
START_DURATION = 5  # seconds blank start screen
LAST_HOLD_DURATION = 5  # seconds hold last frame
OUTPUT_VIDEO = "timer_overlay_test_3.mp4"

FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 64

LAP_TIMES = [23.715, 22.728, 22.784, 22.75, 23.901, 23.076, 22.719, 22.742, 23.345,
             22.614, 22.423, 23.725, 22.988, 22.766, 22.386, 22.592, 22.322, 22.796,
             22.49, 22.315, 22.473, 22.187, 22.221]


font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
lap_label_cache = {}

def render_frame(lap_number, time_elapsed):
    lap_text = f"Lap {lap_number:02}"
    time_text = f"{time_elapsed:.3f} sec"

    lap_bbox = font.getbbox(lap_text)
    lap_w = lap_bbox[2] - lap_bbox[0]
    lap_h = lap_bbox[3] - lap_bbox[1]

    time_bbox = font.getbbox(time_text)
    time_w = time_bbox[2] - time_bbox[0]
    time_h = time_bbox[3] - time_bbox[1]

    center_x = WIDTH // 2
    lap_x = center_x - lap_w // 2
    time_x = center_x - time_w // 2

    if lap_number not in lap_label_cache:
        img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
        draw = ImageDraw.Draw(img)
        draw.text((lap_x, HEIGHT // 3 - 80), lap_text, font=font, fill=(255, 255, 255))
        lap_label_cache[lap_number] = img.copy()

    base = lap_label_cache[lap_number].copy()
    draw = ImageDraw.Draw(base)
    draw.text((time_x, HEIGHT // 3 + 40), time_text, font=font, fill=(0, 255, 0))
    return cv2.cvtColor(np.array(base), cv2.COLOR_RGB2BGR)


def render_lap_video(lap_number, lap_time, temp_dir):
    filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))

    frame_count = math.ceil(FPS * lap_time)
    for f in range(frame_count):
        t = f / FPS
        frame = render_frame(lap_number, t)
        writer.write(frame)

    writer.release()
    return filename


def create_blank_video(duration, filename):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    blank = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame_count = int(FPS * duration)
    for _ in range(frame_count):
        writer.write(blank)
    writer.release()


def concat_videos(file_list, output_file):
    # Create concat text file for ffmpeg
    concat_txt = os.path.join(os.path.dirname(output_file), "concat_list.txt")
    with open(concat_txt, "w") as f:
        for file in file_list:
            f.write(f"file '{file}'\n")

    # cmd = [
    #     "ffmpeg", "-y",
    #     "-f", "concat",
    #     "-safe", "0",
    #     "-i", concat_txt,
    #     "-c", "copy",
    #     output_file
    # ]
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-fps_mode", "cfr",
        "-c:v", "libx264",
        "-r", FPS,
        "-crf", "18",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        output_file
    ]
    subprocess.run(cmd, check=True)
    os.remove(concat_txt)


def main():
    with tempfile.TemporaryDirectory() as temp_dir:
        # 1. Create start blank video
        start_blank = os.path.join(temp_dir, "start_blank.mp4")
        create_blank_video(START_DURATION, start_blank)

        # 2. Render laps in parallel
        lap_videos = []
        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(render_lap_video, i+1, lap_time, temp_dir): i+1 for i, lap_time in enumerate(LAP_TIMES)}
            for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                lap_number = futures[future]
                lap_videos.append(future.result())

        # Sort videos by lap number (they can complete out of order)
        lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

        # 3. Concatenate all videos: start_blank + lap videos
        concat_videos([start_blank] + lap_videos, OUTPUT_VIDEO)

        # Temp files deleted automatically on context exit


if __name__ == "__main__":
    main()
