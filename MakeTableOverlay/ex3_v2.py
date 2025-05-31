# lap_timer_video.py

import os
import cv2
import numpy as np
from PIL import ImageFont
from functools import lru_cache
from tqdm import tqdm

# --- Configuration ---
LAP_TIMES = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201,
             22.646, 22.654, 25.23, 23.231, 25.676, 22.721,
             22.708, 23.561, 26.509, 22.933, 22.871, 22.643,
             22.671, 23.544, 23.424, 22.756, 22.609, 22.474, None]
COUNTDOWN = 5.0  # seconds
FPS = 60
FINAL_DURATION = COUNTDOWN + sum(t for t in LAP_TIMES if t) + 15

# Dimensions and colors
TABLE_WIDTH, TABLE_HEIGHT = 500, 1500  # width, height
TIMER_WIDTH, TIMER_HEIGHT = 400, 150
WHITE = (255, 255, 255)
FONT_PATH = r"C:\Users\epics\AppData\Local\Microsoft\Windows\Fonts\NIS-Heisei-Mincho-W9-Condensed.TTF"

# Preload fonts
_font_cache = {size: ImageFont.truetype(FONT_PATH, size) for size in (24, 32, 40, 48, 72)}

def get_font(size: int):
    if size not in _font_cache:
        _font_cache[size] = ImageFont.truetype(FONT_PATH, size)
    return _font_cache[size]

# --- Text Rendering with OpenCV ---

def draw_text_cv2(img, text, center, font_scale):
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 2
    (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
    x = int(center[0] - text_w / 2)
    y = int(center[1] + text_h / 2)
    cv2.putText(img, text, (x, y), font, font_scale, WHITE, thickness, cv2.LINE_AA)

# --- Table Rendering ---

def draw_table(img, offset, times):
    x0, y0 = offset
    col_w = [100, 200]
    rows = len(times) + 1
    row_h = max(20, min(40, (TABLE_HEIGHT - y0 - 20) // rows))

    # Header
    for idx, hdr in enumerate(["Lap", "Time (s)"]):
        cx = x0 + sum(col_w[:idx]) + col_w[idx] // 2
        cy = y0 + row_h // 2
        draw_text_cv2(img, hdr, (cx, cy), row_h * 0.03)

    # Grid lines
    for r in range(rows + 1):
        y = y0 + r * row_h
        cv2.line(img, (x0, y), (x0 + sum(col_w), y), WHITE, 1)
    cv2.line(img, (x0 + col_w[0], y0), (x0 + col_w[0], y0 + rows * row_h), WHITE, 1)
    cv2.rectangle(img, (x0, y0), (x0 + sum(col_w), y0 + rows * row_h), WHITE, 1)

    # Rows
    for i, t in enumerate(times):
        cy = y0 + (i + 1) * row_h + row_h // 2
        draw_text_cv2(img, str(i+1), (x0 + col_w[0]//2, cy), row_h * 0.025)
        val = f"{t:.3f}" if t else "N/A"
        draw_text_cv2(img, val, (x0 + col_w[0] + col_w[1]//2, cy), row_h * 0.025)

# Table snapshots cache
_table_snapshots = None

def render_table_snapshots():
    global _table_snapshots
    if _table_snapshots is None:
        snaps = []
        for i, t in enumerate(LAP_TIMES):
            if t is None:
                snaps.append(None)
                continue
            img = np.zeros((TABLE_HEIGHT, TABLE_WIDTH, 3), dtype=np.uint8)
            draw_text_cv2(img, "Completed Laps:", (TABLE_WIDTH//2, 40), 1.5)
            draw_table(img, (100, 200), LAP_TIMES[:i+1])
            snaps.append(img)
        _table_snapshots = snaps
    return _table_snapshots

# Get table frame

def get_table_frame(t):
    if t < COUNTDOWN:
        return np.zeros((TABLE_HEIGHT, TABLE_WIDTH, 3), dtype=np.uint8)
    elapsed = t - COUNTDOWN
    snaps = render_table_snapshots()
    total = 0
    for i, lap in enumerate(LAP_TIMES):
        if lap is None or elapsed < total + lap:
            prev = snaps[i-1] if i > 0 else snaps[0]
            return prev
        total += lap
    # After all laps
    last_valid = snaps[-2] if snaps and snaps[-2] is not None else snaps[-1]
    return last_valid

# --- Timer Rendering with LRU Cache ---

@lru_cache(maxsize=500)
def get_timer_image(t):
    img = np.zeros((TIMER_HEIGHT, TIMER_WIDTH, 3), dtype=np.uint8)
    draw_text_cv2(img, f"{t:.2f}", (TIMER_WIDTH//2, TIMER_HEIGHT//2), 2.5)
    return img

# Compose final frame

def compose_frame(t):
    base = get_table_frame(t)
    timer_val = COUNTDOWN - t if t < COUNTDOWN else t - COUNTDOWN
    timer_img = get_timer_image(round(timer_val, 2))
    h, w = timer_img.shape[:2]
    base[20:20+h, 20:20+w] = timer_img
    return base

# --- Main Execution ---

def main():
    os.makedirs("output", exist_ok=True)
    out_path = os.path.join("output", "lap_table_fast_G.mp4")
    writer = cv2.VideoWriter(
        out_path,
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS,
        (TABLE_WIDTH, TABLE_HEIGHT)
    )
    total_frames = int(FINAL_DURATION * FPS)
    for i in tqdm(range(total_frames), desc="Rendering frames"):
        frame = compose_frame(i / FPS)
        writer.write(frame)
    writer.release()
    print(f"Video saved to {out_path}")

if __name__ == "__main__":
    main()
