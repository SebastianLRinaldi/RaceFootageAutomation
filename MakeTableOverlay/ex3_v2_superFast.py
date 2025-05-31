# lap_timer_video.py

import os
import cv2
import numpy as np
from PIL import ImageFont
from functools import lru_cache
from concurrent.futures import ThreadPoolExecutor, as_completed
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
TABLE_SIZE = (500, 1500)
TIMER_SIZE = (400, 150)
WHITE = (255, 255, 255)
FONT_PATH = r"C:\Users\epics\AppData\Local\Microsoft\Windows\Fonts\NIS-Heisei-Mincho-W9-Condensed.TTF"

# Preload common font sizes
_font_cache = {
    size: ImageFont.truetype(FONT_PATH, size)
    for size in (24, 32, 40, 48, 72)
}

def get_font(size: int) -> ImageFont.FreeTypeFont:
    """Return a cached font or load if missing."""
    if size not in _font_cache:
        _font_cache[size] = ImageFont.truetype(FONT_PATH, size)
    return _font_cache[size]

# --- Text Rendering with OpenCV ---

def draw_text_cv2(img: np.ndarray, text: str, center: tuple, font_scale: float) -> None:
    """Draw centered text on an OpenCV image."""
    font = cv2.FONT_HERSHEY_SIMPLEX
    thickness = 2
    text_size, _ = cv2.getTextSize(text, font, font_scale, thickness)
    text_w, text_h = text_size
    x = int(center[0] - text_w / 2)
    y = int(center[1] + text_h / 2)
    cv2.putText(img, text, (x, y), font, font_scale, WHITE, thickness, cv2.LINE_AA)

# --- Table Rendering ---

def draw_table(img: np.ndarray, offset: tuple, times: list) -> None:
    x0, y0 = offset
    col_w = [100, 200]
    rows = len(times) + 1
    row_h = max(20, min(40, (TABLE_SIZE[1] - y0 - 20) // rows))

    # Draw header
    headers = ["Lap", "Time (s)"]
    for idx, hdr in enumerate(headers):
        cx = x0 + sum(col_w[:idx]) + col_w[idx] // 2
        cy = y0 + row_h // 2
        draw_text_cv2(img, hdr, (cx, cy), row_h * 0.025)

    # Draw grid
    for r in range(rows + 1):
        y = y0 + r * row_h
        cv2.line(img, (x0, y), (x0 + sum(col_w), y), WHITE, 1)
    cv2.line(img, (x0 + col_w[0], y0), (x0 + col_w[0], y0 + rows * row_h), WHITE, 1)
    cv2.rectangle(img, (x0, y0), (x0 + sum(col_w), y0 + rows * row_h), WHITE, 1)

    # Fill rows
    for i, t in enumerate(times):
        y = y0 + (i+1) * row_h + row_h // 2
        draw_text_cv2(img, str(i+1), (x0 + col_w[0]//2, y), row_h * 0.02)
        txt = f"{t:.3f}" if t else "N/A"
        draw_text_cv2(img, txt, (x0 + col_w[0] + col_w[1]//2, y), row_h * 0.02)

# Pre-render table snapshots
_table_snapshots = None

def render_table_snapshots() -> list:
    global _table_snapshots
    if _table_snapshots is None:
        snaps = []
        for i, t in enumerate(LAP_TIMES):
            if t is None:
                snaps.append(None)
                continue
            img = np.zeros((TABLE_SIZE[1], TABLE_SIZE[0], 3), np.uint8)
            draw_text_cv2(img, "Completed Laps:", (TABLE_SIZE[0]//2, 40), 1.2)
            draw_table(img, (100, 100), LAP_TIMES[:i+1])
            snaps.append(img)
        _table_snapshots = snaps
    return _table_snapshots

# Get table frame at time t
def get_table_frame(t: float) -> np.ndarray:
    if t < COUNTDOWN:
        return np.zeros((TABLE_SIZE[1], TABLE_SIZE[0], 3), np.uint8)

    elapsed = t - COUNTDOWN
    total = 0
    snaps = render_table_snapshots()
    for i, lap in enumerate(LAP_TIMES):
        if lap is None or elapsed < total + lap:
            return snaps[i-1] if i > 0 else snaps[0]
        total += lap
    return snaps[-2]

# --- Timer Rendering with LRU Cache ---

@lru_cache(maxsize=500)
def get_timer_image(t: float) -> np.ndarray:
    img = np.zeros((TIMER_SIZE[1], TIMER_SIZE[0], 3), np.uint8)
    draw_text_cv2(img, f"{t:.2f}", (TIMER_SIZE[0]//2, TIMER_SIZE[1]//2), 2.5)
    return img

# Compose final frame
def compose_frame(t: float) -> np.ndarray:
    base = get_table_frame(t)
    timer_t = COUNTDOWN - t if t < COUNTDOWN else t - COUNTDOWN
    timer = get_timer_image(round(timer_t, 2))
    # Overlay timer at top-left
    h, w = timer.shape[:2]
    base[20:20+h, 20:20+w] = timer
    return base

# --- Main Execution ---

def main():
    out = cv2.VideoWriter(
        "lap_table_fast_E.mp4",
        cv2.VideoWriter_fourcc(*"mp4v"),
        FPS,
        TABLE_SIZE[::-1]
    )
    total_frames = int(FINAL_DURATION * FPS)

    # Parallel frame rendering
    with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
        futures = {executor.submit(compose_frame, i/FPS): i for i in range(total_frames)}
        for future in tqdm(as_completed(futures), total=total_frames, desc="Rendering frames"):
            frame = future.result()
            out.write(frame)

    out.release()
    print("Rendering complete. Video saved as lap_table_fast.mp4")

if __name__ == "__main__":
    main()
