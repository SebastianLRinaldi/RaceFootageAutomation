# import os
# import subprocess
# from tqdm import tqdm
# import cv2
# import numpy as np
# from PIL import ImageFont, ImageDraw, Image

# # Constants
# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474, None]

# countdown_time = 5
# total_duration = countdown_time + sum(t for t in lap_times if t is not None)
# post_finish_duration = 15
# final_duration = total_duration + post_finish_duration

# FPS = 60
# TIMER_SIZE = (1920, 1080)
# WHITE = (255, 255, 255)
# FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
# OUTPUT_VIDEO = "lap_timer_test.mp4"
# FFMPEG_INPUT_FILE = "ffmpeg_timer_input.txt"
# IMG_FOLDER = "timer_frames"
# START_DURATION = 5
# LAST_HOLD_DURATION = 5

# LAP_TIMES = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474, None]


# font_cache = {}
# def get_font(size):
#     if size not in font_cache:
#         font_cache[size] = ImageFont.truetype(FONTPATH, size)
#     return font_cache[size]

# def draw_centered_text(img, text, x, y, font_size, color):
#     pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     draw = ImageDraw.Draw(pil_img)
#     font = get_font(font_size)
#     bbox = draw.textbbox((0, 0), text, font=font)
#     text_w, text_h = bbox[2] - bbox[0], bbox[3] - bbox[1]
#     draw.text((x - text_w // 2, y - text_h // 2), text, font=font, fill=color)
#     return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# def make_timer_frame(t):
#     img = np.zeros((TIMER_SIZE[1], TIMER_SIZE[0], 3), dtype=np.uint8)

#     if t < countdown_time:
#         count = max(1, int(np.ceil(countdown_time - t)))
#         img = draw_centered_text(img, str(count), TIMER_SIZE[0] // 2, TIMER_SIZE[1] // 2 - 80, 200, WHITE)
#         img = draw_centered_text(img, "Get Ready...", TIMER_SIZE[0] // 2, TIMER_SIZE[1] // 2 + 60, 80, WHITE)
#     else:
#         lap_time_passed = t - countdown_time
#         total_lap_time = sum(x for x in lap_times if x is not None)
#         if lap_time_passed >= total_lap_time:
#             img = draw_centered_text(img, "FINISHED", TIMER_SIZE[0] // 2, TIMER_SIZE[1] // 2, 120, WHITE)
#         else:
#             lap = 0
#             time_in_lap = lap_time_passed
#             for lt in lap_times:
#                 if lt is None: break
#                 if time_in_lap < lt: break
#                 time_in_lap -= lt
#                 lap += 1
#             if lap < len(lap_times) and lap_times[lap] is None:
#                 img = draw_centered_text(img, "Time: N/A", TIMER_SIZE[0] // 2, TIMER_SIZE[1] // 2 - 40, 64, WHITE)
#             else:
#                 img = draw_centered_text(img, f"Time: {time_in_lap:.3f}s", TIMER_SIZE[0] // 2, TIMER_SIZE[1] // 2 - 40, 64, WHITE)
#             img = draw_centered_text(img, f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", TIMER_SIZE[0] // 2, TIMER_SIZE[1] // 2 + 60, 64, WHITE)

#     return img

# def render_timer_frames():
#     frame_count = int(final_duration * FPS)
#     with open(FFMPEG_INPUT_FILE, "w") as f:
#         for i in range(frame_count):
#             t = i / FPS
#             frame = make_timer_frame(t)
#             filename = os.path.join(IMG_FOLDER, f"frame_{i:06d}.png")
#             cv2.imwrite(filename, frame)
#             f.write(f"file '{filename}'\n")
#             if i % (FPS * 5) == 0:
#                 print(f"[Timer] {i}/{frame_count} frames")


# def write_ffmpeg_input():
#     with open(FFMPEG_INPUT_FILE, "w") as f:
#         f.write(f"file '{os.path.join(IMG_FOLDER, 'blank.png')}'\n")
#         f.write(f"duration {START_DURATION}\n")

#         for i, lap_time in enumerate(tqdm(LAP_TIMES, desc="Writing ffmpeg input")):
#             duration = lap_time if lap_time is not None else 5
#             img_file = f"lap_table_{i+1:02}.png"
#             f.write(f"file '{os.path.join(IMG_FOLDER, img_file)}'\n")
#             f.write(f"duration {duration}\n")

#         # Repeat last frame for LAST_HOLD_DURATION
#         last_img = f"lap_table_{len(LAP_TIMES):02}.png"
#         f.write(f"file '{os.path.join(IMG_FOLDER, last_img)}'\n")
#         f.write(f"duration {LAST_HOLD_DURATION}\n")

# def run_ffmpeg():
#     subprocess.run([
#         "ffmpeg",
#         "-y",
#         "-f", "concat",
#         "-safe", "0",
#         "-i", FFMPEG_INPUT_FILE,
#         "-fps_mode", "cfr",
#         "-c:v", "libx264",
#         "-crf", "18",
#         "-preset", "slow",
#         "-pix_fmt", "yuv420p",
#         OUTPUT_VIDEO
#     ], check=True)

# if __name__ == "__main__":
#     render_timer_frames()
#     run_ffmpeg()



"""
Works pretty well
"""

# import cv2
# import numpy as np
# import subprocess
# from PIL import Image, ImageDraw, ImageFont
# from tqdm import tqdm

# # Constants
# WIDTH, HEIGHT = 1280, 720
# FPS = 30
# OUTPUT_VIDEO = "timer_overlay_test.mp4"
# FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

# LAP_TIMES = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474]
# LAST_HOLD_DURATION = 2  # hold last frame extra
# START_DURATION = 2  # show blank frame first

# font = ImageFont.truetype(FONT_PATH, 80)

# def render_frame(lap_number, time_elapsed):
#     """Returns a single BGR frame with lap number and count-up timer."""
#     img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     draw.text((WIDTH // 3, HEIGHT // 3 - 80), f"Lap {lap_number}", font=font, fill=(255, 255, 255))
#     draw.text((WIDTH // 3, HEIGHT // 3 + 40), f"{time_elapsed:.3f} sec", font=font, fill=(0, 255, 0))

#     return cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

# def pipe_frames_to_ffmpeg():
#     proc = subprocess.Popen([
#         "ffmpeg",
#         "-y",
#         "-f", "rawvideo",
#         "-vcodec", "rawvideo",
#         "-pix_fmt", "bgr24",
#         "-s", f"{WIDTH}x{HEIGHT}",
#         "-r", str(FPS),
#         "-i", "-",
#         "-an",
#         "-vcodec", "libx264",
#         "-crf", "18",
#         "-preset", "fast",
#         "-pix_fmt", "yuv420p",
#         OUTPUT_VIDEO
#     ], stdin=subprocess.PIPE)

#     # Start blank screen
#     blank_frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
#     for _ in range(int(FPS * START_DURATION)):
#         proc.stdin.write(blank_frame.tobytes())

#     # Lap frames with timer
#     for i, lap_time in enumerate(tqdm(LAP_TIMES, desc="Rendering laps")):
#         frame_count = int(FPS * lap_time)
#         for f in range(frame_count):
#             t = f / FPS  # time elapsed in seconds
#             frame = render_frame(i + 1, t)
#             proc.stdin.write(frame.tobytes())

#     # Hold last frame
#     for _ in range(int(FPS * LAST_HOLD_DURATION)):
#         proc.stdin.write(frame.tobytes())

#     proc.stdin.close()
#     proc.wait()


# if __name__ == "__main__":
#     pipe_frames_to_ffmpeg()


import os
import subprocess
from tqdm import tqdm
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Config
FPS = 24
WIDTH, HEIGHT = 1280, 720
START_DURATION = 2  # seconds of blank start screen
LAST_HOLD_DURATION = 3  # seconds to hold last frame
OUTPUT_VIDEO = "timer_overlay_test_2.mp4"

# Monospaced font path (adjust for your system)
FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
FONT_SIZE = 64

# Lap times
LAP_TIMES = [23.715, 22.728, 22.784, 22.75, 23.901, 23.076, 22.719, 22.742, 23.345, 
            22.614, 22.423, 23.725, 22.988, 22.766, 22.386, 22.592, 22.322, 22.796, 
            22.49, 22.315, 22.473, 22.187, 22.221]

# FFmpeg encoding params
DEV_MODE = True  # False for final
CRF = "23" if DEV_MODE else "18"
PRESET = "ultrafast" if DEV_MODE else "slow"

# Prepare font and cache
font = ImageFont.truetype(FONT_PATH, FONT_SIZE)
lap_label_cache = {}

# def render_frame(lap_number, time_elapsed):
#     if lap_number not in lap_label_cache:
#         img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
#         draw = ImageDraw.Draw(img)
#         draw.text((WIDTH // 3, HEIGHT // 3 - 80), f"Lap {lap_number:02}", font=font, fill=(255, 255, 255))
#         lap_label_cache[lap_number] = img.copy()
#     base = lap_label_cache[lap_number].copy()
#     draw = ImageDraw.Draw(base)
#     draw.text((WIDTH // 3, HEIGHT // 3 + 40), f"{time_elapsed:.3f} sec", font=font, fill=(0, 255, 0))
#     return cv2.cvtColor(np.array(base), cv2.COLOR_RGB2BGR)


def render_frame(lap_number, time_elapsed):
    lap_text = f"Lap {lap_number:02}"
    time_text = f"{time_elapsed:.3f} sec"

    # Measure text bounding boxes
    lap_bbox = font.getbbox(lap_text)
    lap_w = lap_bbox[2] - lap_bbox[0]
    lap_h = lap_bbox[3] - lap_bbox[1]

    time_bbox = font.getbbox(time_text)
    time_w = time_bbox[2] - time_bbox[0]
    time_h = time_bbox[3] - time_bbox[1]

    # Center X coordinate for both texts
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




def pipe_frames_to_ffmpeg():
    proc = subprocess.Popen([
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", f"{WIDTH}x{HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-an",
        "-vcodec", "libx264",
        "-crf", CRF,
        "-preset", PRESET,
        "-pix_fmt", "yuv420p",
        OUTPUT_VIDEO
    ], stdin=subprocess.PIPE)

    blank = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)
    for _ in range(int(FPS * START_DURATION)):
        proc.stdin.write(blank.tobytes())

    for i, lap_time in enumerate(tqdm(LAP_TIMES, desc="Rendering laps")):
        frame_count = int(FPS * lap_time)
        for f in range(frame_count):
            t = f / FPS
            frame = render_frame(i + 1, t)
            proc.stdin.write(frame.tobytes())

    for _ in range(int(FPS * LAST_HOLD_DURATION)):
        proc.stdin.write(frame.tobytes())

    proc.stdin.close()
    proc.wait()

if __name__ == "__main__":
    pipe_frames_to_ffmpeg()
