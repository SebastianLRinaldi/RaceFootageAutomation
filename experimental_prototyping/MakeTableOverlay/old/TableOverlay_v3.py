import os
import subprocess
from tqdm import tqdm
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Configs


LAP_TIMES = [('23.715', '+1.528'), ('22.728', '+0.541'), ('22.784', '+0.597'), ('22.750', '+0.563'), ('23.901', '+1.714'), ('23.076', '+0.889'), ('22.719', '+0.532'), ('22.742', '+0.555'), ('23.345', '+1.158'), ('22.614', '+0.427'), ('22.423', '+0.236'), ('23.725', '+1.538'), ('22.988', '+0.801'), ('22.766', '+0.579'), ('22.386', '+0.199'), ('22.592', '+0.405'), ('22.322', '+0.135'), ('22.796', '+0.609'), ('22.490', 
'+0.303'), ('22.315', '+0.128'), ('22.473', '+0.286'), ('22.187', '+0.000'), ('22.221', '+0.034')]


# Dynamic headers and column widths - add more columns here
HEADERS = ["Lap", "Time", "Best Lap Diff"]  
COL_WIDTHS = [100, 200, 220]

# Canvas dimensions and padding
CANVAS_WIDTH = 1920
CANVAS_HEIGHT = 1080

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
IMG_FOLDER = "lap_tables_test_3"
OUTPUT_VIDEO = "lap_table_video_test_3_multi_column.mp4"
FFMPEG_INPUT_FILE = "ffmpeg_input.txt"

FPS = 59.94
START_DURATION = 5
LAST_HOLD_DURATION = 5

# Computed constants
TOTAL_ROWS = len(LAP_TIMES) + 1
TABLE_WIDTH = sum(COL_WIDTHS)
FRAME_WIDTH = TABLE_WIDTH + PADDING['left'] + PADDING['right']
FRAME_HEIGHT = (TOTAL_ROWS * ROW_HEIGHT_MAX) + PADDING['top'] + PADDING['bottom']

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

def draw_table(img, x, y, data_rows):
    total_rows = len(data_rows) + 1  # +1 for header
    available_height = img.shape[0] - y - PADDING['bottom']
    row_h = max(ROW_HEIGHT_MIN, min(ROW_HEIGHT_MAX, available_height // total_rows))

    font_size_header = int(row_h * 0.8)
    font_size_row = int(row_h * 0.7)

    # Draw header row
    col_x = x
    for i, header in enumerate(HEADERS):
        center_x = col_x + COL_WIDTHS[i] // 2
        img = draw_centered_text_pil(img, header, center_x, y + row_h // 2, font_size_header, WHITE)
        col_x += COL_WIDTHS[i]
    cv2.rectangle(img, (x, y), (x + TABLE_WIDTH, y + row_h), WHITE, 1)
    # Vertical lines in header
    col_x = x
    for width in COL_WIDTHS[:-1]:
        col_x += width
        cv2.line(img, (col_x, y), (col_x, y + row_h), WHITE, 1)

    # Draw data rows
    for i, row in enumerate(data_rows):
        top = y + row_h * (i + 1)
        cv2.rectangle(img, (x, top), (x + TABLE_WIDTH, top + row_h), WHITE, 1)
        col_x = x
        for j, cell in enumerate(row):
            center_x = col_x + COL_WIDTHS[j] // 2
            text = f"{cell}" if cell is not None else "N/A"
            img = draw_centered_text_pil(img, text, center_x, top + row_h // 2, font_size_row, WHITE)
            col_x += COL_WIDTHS[j]
        # vertical lines
        col_x = x
        for width in COL_WIDTHS[:-1]:
            col_x += width
            cv2.line(img, (col_x, top), (col_x, top + row_h), WHITE, 1)

    return img


def make_blank_frame():
    img = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
    return img

if __name__ == "__main__":
    os.makedirs(IMG_FOLDER, exist_ok=True)

    blank_img = make_blank_frame()
    cv2.imwrite(os.path.join(IMG_FOLDER, "blank.png"), blank_img)

    # Header only
    img = draw_table(
        img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
        x=TABLE_X,
        y=TABLE_Y,
        data_rows=[]
    )
    cv2.imwrite(f"{IMG_FOLDER}/lap_table_00.png", img)
    print(f"Saved: {IMG_FOLDER}/lap_table_00.png")

    if not LAP_TIMES:
        raise ValueError("LAP_TIMES is empty. Nothing to render.")

    for i in tqdm(range(1, len(LAP_TIMES) + 1), desc="Generating images"):
        current_data = []
        for idx in range(i):
            lap = idx + 1
            time_str = f"{LAP_TIMES[idx][0]}"
            delta = f"{LAP_TIMES[idx][1]}"
            current_data.append([lap, time_str, delta])
        img = draw_table(
            img=np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8),
            x=TABLE_X,
            y=TABLE_Y,
            data_rows=current_data
        )
        filename = f"{IMG_FOLDER}/lap_table_{i:02}.png"

        cv2.imwrite(filename, img)

    # Write ffmpeg input file
    with open(FFMPEG_INPUT_FILE, "w") as f:
        f.write(f"file '{os.path.join(IMG_FOLDER, 'blank.png')}'\n")
        f.write(f"duration {START_DURATION}\n")

        for i in tqdm(range(0, len(LAP_TIMES)), desc="Writing ffmpeg input"):
            t = LAP_TIMES[i][0]
            duration = t if t is not None else 5
            img_file = f"lap_table_{i:02}.png"  # notice +1 since 00 is header only
            f.write(f"file '{os.path.join(IMG_FOLDER, img_file)}'\n")
            f.write(f"duration {duration}\n")
            print(f"i={i} | img_file={img_file} | duration={duration}")


        last_img = f"lap_table_{len(LAP_TIMES):02}.png"
        f.write(f"file '{os.path.join(IMG_FOLDER, last_img)}'\n")
        f.write(f"duration {LAST_HOLD_DURATION}\n")
        print(f"last={last_img} | LAST_HOLD_DURATION={LAST_HOLD_DURATION}")

    # Run ffmpeg

    cmd_cpu = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", FFMPEG_INPUT_FILE,
        "-fps_mode", "cfr",
        "-c:v", "libx264",
        "-r", str(FPS),
        "-crf", "18",
        "-preset", "slow",
        "-pix_fmt", "yuv420p",
        OUTPUT_VIDEO
    ]
    


    cmd_gpu = [
        "ffmpeg",
        "-y",
        "-f", "concat",
        "-safe", "0",
        "-i", FFMPEG_INPUT_FILE,
        "-fps_mode", "cfr",
        "-c:v", "h264_nvenc",
        "-r", str(FPS),
        "-preset", "fast",   # NVENC specific presets: default, slow, medium, fast, hp, hq, bd, ll, llhq, llhp
        "-rc", "vbr",        # rate control: vbr, cbr, etc.
        "-cq", "18",         # constant quantizer (quality)
        "-pix_fmt", "yuv420p",
        OUTPUT_VIDEO
    ]

    
    subprocess.run(cmd_cpu, check=True)

    print(f"✅ Video saved as {OUTPUT_VIDEO}")
