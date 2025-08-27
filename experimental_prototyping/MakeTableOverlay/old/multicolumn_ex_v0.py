import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# === Configs ===
LAP_TIMES = [24.459, 23.888, 22.623, 23.368]

# New: Column settings
COL_WIDTHS = [100, 200, 150]  # widths per column
HEADERS = ["Lap", "Time", "Sector"]
WHITE = (255, 255, 255)

ROW_HEIGHT = 40
PADDING = {'top': 10, 'bottom': 10, 'left': 10, 'right': 10}
FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

TABLE_WIDTH = sum(COL_WIDTHS)
TABLE_HEIGHT = (len(LAP_TIMES) + 1) * ROW_HEIGHT
FRAME_WIDTH = TABLE_WIDTH + PADDING['left'] + PADDING['right']
FRAME_HEIGHT = TABLE_HEIGHT + PADDING['top'] + PADDING['bottom']

font_cache = {}
def get_font(size):
    if size not in font_cache:
        font_cache[size] = ImageFont.truetype(FONTPATH, size)
    return font_cache[size]

def draw_centered_text_pil(img, text, x, y, font_size, color):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    font = get_font(font_size)
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]
    draw.text((x - text_w // 2, y - text_h // 2), text, font=font, fill=color)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

def draw_table(img, x, y, data_rows):
    row_h = ROW_HEIGHT
    font_size_header = int(row_h * 0.8)
    font_size_row = int(row_h * 0.7)

    # Header row
    x_offset = x
    for i, (header, width) in enumerate(zip(HEADERS, COL_WIDTHS)):
        center_x = x_offset + width // 2
        img = draw_centered_text_pil(img, header, center_x, y + row_h // 2, font_size_header, WHITE)
        x_offset += width
    cv2.rectangle(img, (x, y), (x + TABLE_WIDTH, y + row_h), WHITE, 1)

    # Data rows
    for row_idx, row in enumerate(data_rows):
        top = y + row_h * (row_idx + 1)
        x_offset = x
        for col_idx, cell in enumerate(row):
            width = COL_WIDTHS[col_idx]
            center_x = x_offset + width // 2
            img = draw_centered_text_pil(img, str(cell), center_x, top + row_h // 2, font_size_row, WHITE)
            x_offset += width
        cv2.rectangle(img, (x, top), (x + TABLE_WIDTH, top + row_h), WHITE, 1)

    return img

# === Build example data ===
lap_data = [
    (i + 1, f"{t:.3f}", f"{t * 0.4:.3f}") for i, t in enumerate(LAP_TIMES)
]

# === Generate image ===
img = np.zeros((FRAME_HEIGHT, FRAME_WIDTH, 3), dtype=np.uint8)
img = draw_table(img, x=PADDING['left'], y=PADDING['top'], data_rows=lap_data)

# === Save ===
os.makedirs("lap_tables_test", exist_ok=True)
cv2.imwrite("lap_tables_test/dynamic_table.png", img)
print("✅ Saved table image with 3 columns.")
