import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Your existing data and constants
lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
             25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
             23.424, 22.756, 22.609, 22.474, None]

countdown_time = 5
fps = 60
final_duration = countdown_time + sum(t for t in lap_times if t is not None) + 15

table_size = (500, 1500)
white = (255, 255, 255)
font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

font_cache = {}
def get_font(font_size):
    if font_size not in font_cache:
        font_cache[font_size] = ImageFont.truetype(font_path, font_size)
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
    col1_w, col2_w = 100, 200
    total_rows = len(lap_times) + 1
    max_height = table_size[1] - y - 20
    row_h = max(20, min(40, max_height // total_rows))

    font_size_header = int(row_h * 0.8)
    font_size_row = int(row_h * 0.7)

    img = draw_centered_text_pil(img, "Lap", x + col1_w // 2, y + row_h // 2, font_size_header, white)
    img = draw_centered_text_pil(img, "Time (s)", x + col1_w + col2_w // 2, y + row_h // 2, font_size_header, white)
    cv2.rectangle(img, (x, y), (x + col1_w + col2_w, y + row_h), white, 1)
    cv2.line(img, (x + col1_w, y), (x + col1_w, y + row_h), white, 1)

    for i, t in enumerate(lap_times):
        top = y + row_h * (i + 1)
        cv2.rectangle(img, (x, top), (x + col1_w + col2_w, top + row_h), white, 1)
        cv2.line(img, (x + col1_w, top), (x + col1_w, top + row_h), white, 1)

        lap_num = str(i + 1)
        time_str = f"{t:.3f}" if t is not None else "N/A"
        img = draw_centered_text_pil(img, lap_num, x + col1_w // 2, top + row_h // 2, font_size_row, white)
        img = draw_centered_text_pil(img, time_str, x + col1_w + col2_w // 2, top + row_h // 2, font_size_row, white)

    return img

def pre_render_table_snapshots():
    snapshots = []
    cumulative_time = 0
    for i, t in enumerate(lap_times):
        if t is None:
            snapshots.append(None)
            continue
        cumulative_time += t
        img = np.zeros((table_size[1], table_size[0], 3), dtype=np.uint8)
        img = draw_centered_text_pil(img, "Completed Laps:", 250, 40, 32, white)
        img = draw_table(img, 100, 100, lap_times[:i+1])
        snapshots.append(img)
    return snapshots

def get_table_frame(t, snapshots):
    if t < countdown_time:
        # Before countdown ends, empty table or no laps done
        img = np.zeros((table_size[1], table_size[0], 3), dtype=np.uint8)
        return img
    lap_time_passed = t - countdown_time
    cumulative = 0
    lap_idx = -1
    for i, lap in enumerate(lap_times):
        if lap is None:
            break
        cumulative += lap
        if lap_time_passed < cumulative:
            lap_idx = i
            break
    if lap_time_passed >= cumulative:
        lap_idx = len(lap_times) - 1  # All laps done
    if lap_idx == -1:
        return np.zeros((table_size[1], table_size[0], 3), dtype=np.uint8)
    return snapshots[lap_idx]

# --- Add timer image caching here ---

timer_font_size = 72
timer_img_size = (400, 150)  # width, height
timer_color = white
timer_cache = {}

def pre_render_timer_images(max_time, fps):
    steps = int(max_time * 100) + 1  # 0.01 sec steps for smoother caching
    font = get_font(timer_font_size)
    blank = np.zeros((timer_img_size[1], timer_img_size[0], 3), dtype=np.uint8)

    for i in range(steps):
        t = i / 100.0
        img = blank.copy()
        img = draw_centered_text_pil(img, f"{t:.2f}", timer_img_size[0]//2, timer_img_size[1]//2, timer_font_size, timer_color)
        timer_cache[round(t,2)] = img

def get_timer_frame(t):
    key = round(t, 2)
    if key in timer_cache:
        return timer_cache[key]
    # Return last cached frame if out of range
    return timer_cache[max(timer_cache.keys())]

# --- Compose final frame with timer + table ---

def compose_frame(t, table_snapshots):
    base = get_table_frame(t, table_snapshots)
    if t < countdown_time:
        # Show countdown timer only
        timer_img = get_timer_frame(countdown_time - t)
    else:
        # Show elapsed time since countdown ended
        timer_img = get_timer_frame(t - countdown_time)
    
    # Place timer_img top-left corner with some margin
    margin = 20
    x, y = margin, margin
    h, w = timer_img.shape[:2]
    
    # Overlay timer on base
    base[y:y+h, x:x+w] = timer_img
    return base


from tqdm import tqdm
if __name__ == "__main__":
    import time
    table_snapshots = pre_render_table_snapshots()

    out_table = cv2.VideoWriter("lap_table_fast.mp4", cv2.VideoWriter_fourcc(*'mp4v'), fps, table_size)
    total_frames = int(final_duration * fps)

    for i in tqdm(range(total_frames), desc="Rendering frames"):
        t = i / fps
        frame = get_table_frame(t, table_snapshots)
        out_table.write(frame)

    out_table.release()
    print("Done writing fast table video.")
