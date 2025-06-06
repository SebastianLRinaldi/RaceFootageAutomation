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

# Canvas dimensions
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

# Table layout constants
COL1_WIDTH = 100
COL2_WIDTH = 200

ROW_HEIGHT_MIN = 20
ROW_HEIGHT_MAX = 40

PADDING = {
    'top': 10,
    'bottom': 10,
    'left': 10,
    'right': 10
}

WHITE = (255, 255, 255)

FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
IMG_FOLDER = "lap_tables_test"
OUTPUT_VIDEO = "lap_table_video_test.mp4"
FFMPEG_INPUT_FILE = "ffmpeg_input.txt"

START_DURATION = 5
LAST_HOLD_DURATION = 5

# Computed constants - adapt automatically when above change
TOTAL_ROWS = len(LAP_TIMES) + 1
TABLE_WIDTH = COL1_WIDTH + COL2_WIDTH
TABLE_HEIGHT = TOTAL_ROWS * ROW_HEIGHT_MAX  # Use max row height for sizing

FRAME_WIDTH = TABLE_WIDTH + PADDING['left'] + PADDING['right']
FRAME_HEIGHT = TABLE_HEIGHT + PADDING['top'] + PADDING['bottom']

TABLE_X = PADDING['left']  # Fixed at left padding; center logic possible but unused
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

    # Data rows
    for i, t in enumerate(lap_times):
        top = y + row_h * (i + 1)
        cv2.rectangle(img, (x, top), (x + COL1_WIDTH + COL2_WIDTH, top + row_h), WHITE, 1)
        cv2.line(img, (x + COL1_WIDTH, top), (x + COL1_WIDTH, top + row_h), WHITE, 1)

        lap_num = str(i + 1)
        time_str = f"{t:.3f}" if t is not None else "N/A"
        img = draw_centered_text_pil(img, lap_num, x + COL1_WIDTH // 2, top + row_h // 2, font_size_row, WHITE)
        img = draw_centered_text_pil(img, time_str, x + COL1_WIDTH + COL2_WIDTH // 2, top + row_h // 2, font_size_row, WHITE)

    return img

def make_table_frame(preview_time=0):
    # Always use max row height for consistent size
    img = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    return draw_table(img, x=TABLE_X, y=TABLE_Y, lap_times=LAP_TIMES)

def make_blank_frame():
    img = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    return img

# Main execution
if __name__ == "__main__":
    os.makedirs(IMG_FOLDER, exist_ok=True)

    blank_img = make_blank_frame()
    cv2.imwrite(os.path.join(IMG_FOLDER, "blank.png"), blank_img)

    # Header-only table image
    img = draw_table(
        img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
        x=TABLE_X,
        y=TABLE_Y,
        lap_times=[]
    )
    cv2.imwrite(f"{IMG_FOLDER}/lap_table_00.png", img)
    print(f"Saved: {IMG_FOLDER}/lap_table_00.png")

    if not LAP_TIMES:
        raise ValueError("LAP_TIMES is empty. Nothing to render.")

    for i in tqdm(range(1, len(LAP_TIMES) + 1), desc="Generating images"):
        current_laps = LAP_TIMES[:i]
        img = draw_table(
            img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
            x=TABLE_X,
            y=TABLE_Y,
            lap_times=current_laps
        )
        filename = f"{IMG_FOLDER}/lap_table_{i:02}.png"
        cv2.imwrite(filename, img)

# Write ffmpeg input file
with open(FFMPEG_INPUT_FILE, "w") as f:
    f.write(f"file '{os.path.join(IMG_FOLDER, 'blank.png')}'\n")
    f.write(f"duration {START_DURATION}\n")

    for i in tqdm(range(0, len(LAP_TIMES)), desc="Writing ffmpeg input"):
        t = LAP_TIMES[i]
        duration = t if t is not None else 5
        img_file = f"lap_table_{i:02}.png"
        f.write(f"file '{os.path.join(IMG_FOLDER, img_file)}'\n")
        f.write(f"duration {duration}\n")

    last_img = f"lap_table_{i+1:02}.png"
    f.write(f"file '{os.path.join(IMG_FOLDER, last_img)}'\n")
    f.write(f"duration {LAST_HOLD_DURATION}\n")

# Run ffmpeg
subprocess.run([
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", FFMPEG_INPUT_FILE,
    "-fps_mode", "cfr",
    "-c:v", "libx264",
    "-crf", "18",
    "-preset", "slow",
    "-pix_fmt", "yuv420p",
    OUTPUT_VIDEO
], check=True)

print(f"✅ Video saved as {OUTPUT_VIDEO}")
