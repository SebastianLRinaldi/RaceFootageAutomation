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

FPS = "100"
FPS_NUM = 100
START_DURATION = 5  # seconds blank start screen
LAST_HOLD_DURATION = 5  # seconds hold last frame
OUTPUT_VIDEO = "timer_overlay_test_3.mp4"

FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 64

LAP_TIMES = [23.715, 22.728, 22.784, 22.75, 23.901, 23.076, 22.719, 22.742, 23.345,
             22.614, 22.423, 23.725, 22.988, 22.766, 22.386, 22.592, 22.322, 22.796,
             22.49, 22.315, 22.473, 22.187, 22.221]
FONT = ImageFont.truetype(FONT_PATH, FONT_SIZE)
lap_label_cache = {}




def generate_timer_video(output_path):
    
    total_frames = int(MAX_TIME * FPS_NUM)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_path, fourcc, FPS_NUM, (WIDTH, HEIGHT), True)

    for frame in tqdm(range(total_frames), desc="Rendering timer video"):
        time_elapsed = frame / FPS_NUM
        time_text = f"{time_elapsed:.3f} sec"
        # time_text = f"{time_elapsed:06.3f} sec"

        img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # Black background
        draw = ImageDraw.Draw(img)

        text_bbox = FONT.getbbox(time_text)
        text_w = text_bbox[2] - text_bbox[0]
        text_x = (WIDTH // 2) - (text_w // 2)

        draw.text((text_x, HEIGHT // 3 + 40), time_text, font=FONT, fill=(0, 255, 0))

        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()




rerender_input = input("Rerender: Timer Counter? [Y/n]: ")

if rerender_input.strip().lower() in ('y', 'yes', ''):
    generate_timer_video("timer_overlay.mp4")






def preload_timer_frames(path):
    cap = cv2.VideoCapture(path)
    frames = []
    while True:
        ret, frame = cap.read()
        if not ret:
            break
        frames.append(frame)
    cap.release()
    return frames


# Setup once
timer_frames = preload_timer_frames("timer_overlay.mp4")
"""
v1 1:40-2:00Min
"""
# def render_frame(lap_number, time_elapsed, timer_frames):
#     lap_text = f"Lap {lap_number:02}"

#     lap_bbox = font.getbbox(lap_text)
#     lap_w = lap_bbox[2] - lap_bbox[0]
#     lap_x = (WIDTH // 2) - (lap_w // 2)

#     if lap_number not in lap_label_cache:
#         img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
#         draw = ImageDraw.Draw(img)
#         draw.text((lap_x, HEIGHT // 3 - 80), lap_text, font=font, fill=(255, 255, 255))
#         lap_label_cache[lap_number] = img.copy()

#     base = lap_label_cache[lap_number].copy()
#     base_bgr = cv2.cvtColor(np.array(base), cv2.COLOR_RGB2BGR)

#     frame_idx = int(time_elapsed * FPS_NUM)
#     if frame_idx >= len(timer_frames):
#         raise IndexError(f"Frame index {frame_idx} out of range")
#     timer_frame = timer_frames[frame_idx]

#     combined = cv2.addWeighted(base_bgr, 1.0, timer_frame, 1.0, 0)

#     return combined



# def render_lap_video(lap_number, lap_time, temp_dir, timer_frames):
    
#     filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     writer = cv2.VideoWriter(filename, fourcc, FPS_NUM, (WIDTH, HEIGHT))

#     # frame_count = math.ceil(FPS_NUM* lap_time)
#     frame_count = math.floor(FPS_NUM * lap_time) + 1
#     # for f in range(frame_count):
#     for f in tqdm(range(frame_count), desc=f"Rendering Lap {lap_number}"):
#         t = f / FPS_NUM
#         frame = render_frame(lap_number, t, timer_frames)
#         writer.write(frame)

#     writer.release()
#     return filename


"""
V2 - 1:20-1:40MIN
"""
# def create_lap_overlay(lap_number):
#     lap_text = f"Lap {lap_number:02}"
#     lap_bbox = font.getbbox(lap_text)
#     lap_w = lap_bbox[2] - lap_bbox[0]
#     lap_h = lap_bbox[3] - lap_bbox[1]
#     lap_x = (WIDTH // 2) - (lap_w // 2)
#     lap_y = HEIGHT // 3 - 80

#     img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # black bg
#     draw = ImageDraw.Draw(img)
#     draw.text((lap_x, lap_y), lap_text, font=font, fill=(255, 255, 255))

#     # Convert once to numpy BGR for direct overlay
#     overlay = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
#     return overlay


# def render_frame(lap_overlay, time_elapsed, timer_frames):
#     frame_idx = int(time_elapsed * FPS_NUM)
#     if frame_idx >= len(timer_frames):
#         frame_idx = len(timer_frames) - 1

#     base_frame = timer_frames[frame_idx].copy()  # copy because we’ll modify

#     # Use mask to copy only non-black pixels from lap_overlay
#     mask = np.any(lap_overlay != 0, axis=2)
#     base_frame[mask] = lap_overlay[mask]

#     return base_frame


# def render_lap_video(lap_number, lap_time, temp_dir, timer_frames):
#     filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     writer = cv2.VideoWriter(filename, fourcc, FPS_NUM, (WIDTH, HEIGHT))

#     lap_overlay = create_lap_overlay(lap_number)

#     frame_count = math.floor(FPS_NUM * lap_time) + 1
#     for f in tqdm(range(frame_count), desc=f"Rendering Lap {lap_number}"):
#         t = f / FPS_NUM
#         frame = render_frame(lap_overlay, t, timer_frames)
#         writer.write(frame)

#     writer.release()
#     return filename

"""
v3 7-20sec
"""
def create_lap_overlay(lap_number):
    lap_text = f"Lap {lap_number:02}"
    lap_bbox = FONT.getbbox(lap_text)
    lap_w = lap_bbox[2] - lap_bbox[0]
    lap_h = lap_bbox[3] - lap_bbox[1]
    lap_x = (WIDTH // 2) - (lap_w // 2)
    lap_y = HEIGHT // 3 - 80

    img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))  # black bg
    draw = ImageDraw.Draw(img)
    draw.text((lap_x, lap_y), lap_text, font=FONT, fill=(255, 255, 255))

    # Convert once to numpy BGR for direct overlay
    overlay = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
    return overlay


def create_lap_overlay_and_mask(lap_number):
    lap_overlay = create_lap_overlay(lap_number)
    lap_mask = np.any(lap_overlay != 0, axis=2).astype(np.uint8) * 255  # mask 0 or 255 for OpenCV
    return lap_overlay, lap_mask

# def render_frame(lap_overlay, lap_mask, time_elapsed, timer_frames):
#     frame_idx = int(time_elapsed * FPS_NUM)
#     if frame_idx >= len(timer_frames):
#         frame_idx = len(timer_frames) - 1

#     base_frame = timer_frames[frame_idx].copy()

#     # Use OpenCV copyTo with mask - much faster than numpy boolean indexing
#     cv2.copyTo(lap_overlay, lap_mask, base_frame)

#     return base_frame

# def render_lap_video(lap_number, lap_time, temp_dir, timer_frames):
#     filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     writer = cv2.VideoWriter(filename, fourcc, FPS_NUM, (WIDTH, HEIGHT))

#     lap_overlay, lap_mask = create_lap_overlay_and_mask(lap_number)

#     frame_count = math.floor(FPS_NUM * lap_time) + 1
#     for f in tqdm(range(frame_count), desc=f"Rendering Lap {lap_number}"):
#         t = f / FPS_NUM
#         frame = render_frame(lap_overlay, lap_mask, t, timer_frames)
#         writer.write(frame)

#     writer.release()
#     return filename


def render_frame(lap_overlay, lap_mask, time_elapsed, timer_frames):
    frame_idx = int(time_elapsed * FPS_NUM)
    if frame_idx >= len(timer_frames):
        frame_idx = len(timer_frames) - 1

    base_frame = timer_frames[frame_idx].get()  # get NumPy array from UMat

    # Use OpenCV copyTo with mask (lap_overlay and lap_mask can stay numpy arrays)
    cv2.copyTo(lap_overlay, lap_mask, base_frame)

    return base_frame

def render_lap_video(lap_number, lap_time, temp_dir, timer_frames):
    filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS_NUM, (WIDTH, HEIGHT))

    lap_overlay, lap_mask = create_lap_overlay_and_mask(lap_number)
    
    # Convert once - IMPORTANT: This is where you use UMat
    timer_frames_umat = [cv2.UMat(f) for f in timer_frames]

    frame_count = math.floor(FPS_NUM * lap_time) + 1
    for f in tqdm(range(frame_count), desc=f"Rendering Lap {lap_number}"):
        t = f / FPS_NUM
        # Pass UMat frames to render_frame (modify render_frame to accept UMat inputs)
        frame = render_frame(lap_overlay, lap_mask, t, timer_frames_umat)
        # Convert back to numpy array to write with VideoWriter
        writer.write(frame.get() if isinstance(frame, cv2.UMat) else frame)

    writer.release()
    return filename

def create_blank_video(duration, filename):
    
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS_NUM, (WIDTH, HEIGHT))
    blank = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    frame_count = int(FPS_NUM* duration)
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
    #     "ffmpeg",
    #     "-y",
    #     "-f", "concat",
    #     "-safe", "0",
    #     "-i", concat_txt,
    #     "-fps_mode", "cfr",
    #     "-c:v", "libx264",
    #     "-r", FPS,
    #     "-crf", "18",
    #     "-preset", "slow",
    #     "-pix_fmt", "yuv420p",
    #     output_file
    # ]

    """
    Super fast render: "-c:v", "h264_nvenc", fast settings
    - (Power mode - Performance)
        frame=52919 fps=2674 q=13.0 Lsize=   71133KiB time=00:08:49.19 bitrate=1101.2kbits/s speed=26.7x
    - (Power mode - ECO)  
        frame=52919 fps=2103 q=13.0 Lsize=   71133KiB time=00:08:49.19 bitrate=1101.2kbits/s speed=  21x
    vs
    frame=52919 fps=1080 q=-1.0 Lsize=   11754KiB time=00:08:49.17 bitrate= 182.0kbits/s speed=10.8x
    """
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", concat_txt,
        "-fps_mode", "cfr",
        "-c:v", "h264_nvenc",
        "-r", FPS,
        "-preset", "fast",   # NVENC specific presets: default, slow, medium, fast, hp, hq, bd, ll, llhq, llhp
        "-rc", "vbr",        # rate control: vbr, cbr, etc.
        "-cq", "19",         # constant quantizer (quality)
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
        # precache_times()
        # 2. Render laps in parallel
        lap_videos = []
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
        concat_videos([start_blank] + lap_videos, OUTPUT_VIDEO)

        # Temp files deleted automatically on context exit


# from concurrent.futures import ProcessPoolExecutor, as_completed

# def main():
#     with tempfile.TemporaryDirectory() as temp_dir:
#         start_blank = os.path.join(temp_dir, "start_blank.mp4")
#         create_blank_video(START_DURATION, start_blank)

#         lap_videos = []
#         with ProcessPoolExecutor() as executor:
#             futures = {
#                 executor.submit(render_lap_video, i + 1, lap_time, temp_dir, timer_frames): i + 1
#                 for i, lap_time in enumerate(LAP_TIMES)
#             }

#             for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
#                 lap_number = futures[future]
#                 lap_videos.append(future.result())

#         lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

#         concat_videos([start_blank] + lap_videos, OUTPUT_VIDEO)


if __name__ == "__main__":
    cProfile.run('main()')

# import subprocess

# def run_cmd(cmd):
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     return result.stdout.strip()

# def main():
#     hwaccels = run_cmd(["ffmpeg", "-hwaccels"])
#     print("Hardware acceleration methods:")
#     print(hwaccels)
#     print("\nNVENC encoders:")
#     encoders = run_cmd(["ffmpeg", "-encoders"])
#     nvenc_encoders = [line for line in encoders.splitlines() if "nvenc" in line.lower()]
#     print("\n".join(nvenc_encoders) if nvenc_encoders else "No NVENC encoders found")

# if __name__ == "__main__":
#     main()
