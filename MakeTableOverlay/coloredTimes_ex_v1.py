import os
import subprocess
from tqdm import tqdm
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Configs
LAP_TIMES = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201,
             22.646, 22.654, 25.23, 23.231, 25.676, 22.721,
             22.708, 23.561, 26.509, 22.933, 22.871, 22.643,
             22.671, 23.544, 23.424, 22.756, 22.609, 22.474]

# Canvas and table layout
CANVAS_WIDTH, CANVAS_HEIGHT = 1920, 1080
COL1_WIDTH, COL2_WIDTH = 100, 200
ROW_HEIGHT_MIN, ROW_HEIGHT_MAX = 20, 40
PADDING = {'top': 10, 'bottom': 10, 'left': 10, 'right': 10}
WHITE = (255, 255, 255)

FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

TOTAL_ROWS = len(LAP_TIMES) + 1
TABLE_WIDTH = COL1_WIDTH + COL2_WIDTH
TABLE_HEIGHT = TOTAL_ROWS * ROW_HEIGHT_MAX

FRAME_WIDTH = TABLE_WIDTH + PADDING['left'] + PADDING['right']
FRAME_HEIGHT = TABLE_HEIGHT + PADDING['top'] + PADDING['bottom']

TABLE_X = PADDING['left']
TABLE_Y = PADDING['top']

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

def draw_table(img, x, y, lap_times):
    total_rows = len(lap_times) + 1
    available_height = img.shape[0] - y - PADDING['bottom']
    row_h = max(ROW_HEIGHT_MIN, min(ROW_HEIGHT_MAX, available_height // total_rows))
    font_size_header = int(row_h * 0.8)
    font_size_row = int(row_h * 0.7)

    # Header row
    img = draw_centered_text_pil(img, "Lap", x + COL1_WIDTH // 2, y + row_h // 2, font_size_header, WHITE)
    img = draw_centered_text_pil(img, "Time", x + COL1_WIDTH + COL2_WIDTH // 2, y + row_h // 2, font_size_header, WHITE)
    cv2.rectangle(img, (x, y), (x + COL1_WIDTH + COL2_WIDTH, y + row_h), WHITE, 1)
    cv2.line(img, (x + COL1_WIDTH, y), (x + COL1_WIDTH, y + row_h), WHITE, 1)

    if not lap_times:
        return img

    min_t = min(lap_times)
    max_t = max(lap_times)

    for i, t in enumerate(lap_times):
        top = y + row_h * (i + 1)
        cv2.rectangle(img, (x, top), (x + COL1_WIDTH + COL2_WIDTH, top + row_h), WHITE, 1)
        cv2.line(img, (x + COL1_WIDTH, top), (x + COL1_WIDTH, top + row_h), WHITE, 1)

        # Normalize for color: green=fast, red=slow
        norm = (t - min_t) / (max_t - min_t + 1e-6)
        r = int(255 * norm)
        g = int(255 * (1 - norm))
        color = (r, g, 0)

        img = draw_centered_text_pil(img, str(i + 1), x + COL1_WIDTH // 2, top + row_h // 2, font_size_row, color)
        img = draw_centered_text_pil(img, f"{t:.3f}", x + COL1_WIDTH + COL2_WIDTH // 2, top + row_h // 2, font_size_row, color)

    # Draw stats below table
    img = draw_stats(img, lap_times, y + row_h * (len(lap_times) + 1))

    return img

def draw_stats(img, lap_times, y_offset):
    avg = sum(lap_times) / len(lap_times)
    best = min(lap_times)
    worst = max(lap_times)
    diff = worst - best
    stats = [
        f"Avg: {avg:.3f}s",
        f"Best: {best:.3f}s",
        f"Worst: {worst:.3f}s",
        f"Δ: {diff:.3f}s"
    ]
    font_size = 32
    x = PADDING['left'] + 100
    y = y_offset + 20
    for stat in stats:
        img = draw_centered_text_pil(img, stat, x, y, font_size, WHITE)
        y += 40
    return img

def make_canvas():
    return np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)

def interpolate_lap_times(lap_times, frame_idx, frames_per_lap):
    # Fully shown laps before frame_idx // frames_per_lap
    count = frame_idx // frames_per_lap
    alpha = (frame_idx % frames_per_lap) / frames_per_lap
    if count >= len(lap_times):
        return lap_times
    times = lap_times[:count]
    if count < len(lap_times):
        partial_time = lap_times[count] * alpha
        times.append(partial_time)
    return times

if __name__ == "__main__":
    FPS = 60
    SECONDS_PER_LAP = 0.5
    FRAMES_PER_LAP = int(FPS * SECONDS_PER_LAP)
    OUTPUT_VIDEO = "lap_table_video_test_time_colored.mp4"

    # Setup ffmpeg pipe
    cmd = [
        "ffmpeg",
        "-y",
        "-f", "rawvideo",
        "-vcodec", "rawvideo",
        "-pix_fmt", "bgr24",
        "-s", f"{FRAME_WIDTH}x{FRAME_HEIGHT}",
        "-r", str(FPS),
        "-i", "-",
        "-an",
        "-c:v", "libx264",
        "-crf", "18",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        OUTPUT_VIDEO
    ]

    with subprocess.Popen(cmd, stdin=subprocess.PIPE) as proc:
        total_frames = FRAMES_PER_LAP * len(LAP_TIMES)
        for frame_idx in tqdm(range(total_frames), desc="Rendering video"):
            times_to_draw = interpolate_lap_times(LAP_TIMES, frame_idx, FRAMES_PER_LAP)
            img = make_canvas()
            img = draw_table(img, TABLE_X, TABLE_Y, times_to_draw)
            proc.stdin.write(img.tobytes())
        proc.stdin.close()
        proc.wait()

    print(f"✅ Video saved as {OUTPUT_VIDEO}")

