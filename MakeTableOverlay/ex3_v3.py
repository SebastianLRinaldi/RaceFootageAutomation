import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Configs
LAP_TIMES = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201,
             22.646, 22.654, 25.23, 23.231, 25.676, 22.721,
             22.708, 23.561, 26.509, 22.933, 22.871, 22.643,
             22.671, 23.544, 23.424, 22.756, 22.609, 22.474]

# Table and layout configs
COL1_WIDTH = 100
COL2_WIDTH = 200
ROW_HEIGHT_MIN = 20
ROW_HEIGHT_MAX = 40

# Padding around table
PADDING = {
    'top': 50,
    'bottom': 50,
    'left': 50,
    'right': 50
}

WHITE = (255, 255, 255)
FONTPATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
IMG_FOLDER = "lap_tables"

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
    img = draw_centered_text_pil(img, "Time (s)", x + COL1_WIDTH + COL2_WIDTH // 2, y + row_h // 2, font_size_header, WHITE)
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
    total_rows = len(LAP_TIMES) + 1
    row_h = min(ROW_HEIGHT_MAX, max(ROW_HEIGHT_MIN, 40))  # Default row height
    table_width = COL1_WIDTH + COL2_WIDTH
    table_height = total_rows * row_h

    frame_width = table_width + PADDING['left'] + PADDING['right']
    frame_height = table_height + PADDING['top'] + PADDING['bottom']

    img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    return draw_table(img, x=PADDING['left'], y=PADDING['top'], lap_times=LAP_TIMES)

def make_blank_frame():
    total_rows = len(LAP_TIMES) + 1
    row_h = min(ROW_HEIGHT_MAX, max(ROW_HEIGHT_MIN, 40))
    table_width = COL1_WIDTH + COL2_WIDTH
    table_height = total_rows * row_h

    frame_width = table_width + PADDING['left'] + PADDING['right']
    frame_height = table_height + PADDING['top'] + PADDING['bottom']

    # Just zeros = black image, no text
    img = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
    return img


# if __name__ == "__main__":
#     cv2.namedWindow('Table Preview', cv2.WINDOW_NORMAL)
#     cv2.imshow('Table Preview', make_table_frame(0))  # preview_time unused here
#     cv2.waitKey(0)
#     cv2.destroyAllWindows()


# if __name__ == "__main__":
#     os.makedirs("lap_tables", exist_ok=True)
#     for i in range(1, len(LAP_TIMES) + 1):
#         current_laps = LAP_TIMES[:i]
#         img = draw_table(
#             img=np.zeros((1080, 400, 3), dtype=np.uint8),
#             x=PADDING['left'],
#             y=PADDING['top'],
#             lap_times=current_laps
#         )
#         filename = f"lap_tables/lap_table_{i:02}.png"
#         cv2.imwrite(filename, img)
#         print(f"Saved: {filename}")


# if __name__ == "__main__":
#     os.makedirs("lap_tables", exist_ok=True)

#     blank_img = make_blank_frame()
#     cv2.imwrite(os.path.join(IMG_FOLDER, "blank.png"), blank_img)
    
    # # Add the header-only table first
    # img = draw_table(
    #     img=np.zeros((1080, 400, 3), dtype=np.uint8),
    #     x=PADDING['left'],
    #     y=PADDING['top'],
    #     lap_times=[]
    # )
    # cv2.imwrite("lap_tables/lap_table_00.png", img)
    # print("Saved: lap_tables/lap_table_00.png")

    # # Then loop through incremental lap counts
    # for i in range(1, len(LAP_TIMES) + 1):
    #     current_laps = LAP_TIMES[:i]
    #     img = draw_table(
    #         img=np.zeros((1080, 400, 3), dtype=np.uint8),
    #         x=PADDING['left'],
    #         y=PADDING['top'],
    #         lap_times=current_laps
    #     )
    #     filename = f"lap_tables/lap_table_{i:02}.png"
    #     cv2.imwrite(filename, img)
    #     print(f"Saved: {filename}")


# from tqdm import tqdm
# IMG_FOLDER = "lap_tables"
# OUTPUT_VIDEO = "lap_table_video.mp4"
# FPS = 30

# # Use the first valid image to get frame size
# sample_img = cv2.imread(os.path.join(IMG_FOLDER, "lap_table_00.png"))
# height, width, _ = sample_img.shape
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# video = cv2.VideoWriter(OUTPUT_VIDEO, fourcc, FPS, (width, height))

# # Frame 0 (header only)
# img_path = os.path.join(IMG_FOLDER, "lap_table_00.png")
# img = cv2.imread(img_path)
# duration = LAP_TIMES[0] or 1
# for _ in tqdm(range(int(duration * FPS)), desc="Rendering 00"):
#     video.write(img)

# # Remaining frames
# for i, t in enumerate(tqdm(LAP_TIMES[1:], desc="Rendering laps", position=0), start=1):
#     img_path = os.path.join(IMG_FOLDER, f"lap_table_{i:02}.png")
#     img = cv2.imread(img_path)
#     duration = t or 1
#     for _ in tqdm(range(int(duration * FPS)), desc=f"Lap {i:02}", leave=False):
#         video.write(img)

# video.release()
# print(f"Video saved as {OUTPUT_VIDEO}")

# import os
# import subprocess
# IMG_FOLDER = "lap_tables"
# OUTPUT_VIDEO = "lap_table_video_fast.mp4"
# FFMPEG_INPUT_FILE = "ffmpeg_input.txt"

# # Step 1: Write the ffmpeg input file
# with open(FFMPEG_INPUT_FILE, "w") as f:
#     # Header only (00)
#     duration = LAP_TIMES[0] or 1
#     f.write(f"file '{os.path.join(IMG_FOLDER, 'lap_table_00.png')}'\n")
#     f.write(f"duration {duration}\n")

#     # Laps 1 to N
#     for i, t in enumerate(LAP_TIMES[1:], start=1):
#         duration = t or 1
#         img_file = f"lap_table_{i:02}.png"
#         f.write(f"file '{os.path.join(IMG_FOLDER, img_file)}'\n")
#         f.write(f"duration {duration}\n")

#     # Repeat last image once more (ffmpeg requirement)
#     last_img = f"lap_table_{i:02}.png"
#     f.write(f"file '{os.path.join(IMG_FOLDER, last_img)}'\n")

# # Step 2: Run ffmpeg
# subprocess.run([
#     "ffmpeg",
#     "-y",
#     "-f", "concat",
#     "-safe", "0",
#     "-i", FFMPEG_INPUT_FILE,
#     "-vsync", "vfr",
#     "-pix_fmt", "yuv420p",
#     OUTPUT_VIDEO
# ], check=True)

# print(f"✅ Video saved as {OUTPUT_VIDEO}")



import os
import subprocess
IMG_FOLDER = "lap_tables"
OUTPUT_VIDEO = "lap_table_video_complete1.mp4"
FFMPEG_INPUT_FILE = "ffmpeg_input.txt"


START_DURATION = 5
LAST_HOLD_DURATION = 5

with open(FFMPEG_INPUT_FILE, "w") as f:
    # Blank frame first
    f.write(f"file '{os.path.join(IMG_FOLDER, 'blank.png')}'\n")
    f.write(f"duration {START_DURATION}\n")


    for i in range(0, len(LAP_TIMES)):
        # print(f"indx={i}")
        t = LAP_TIMES[i]
        duration = t or 5
        # print(duration)
        img_file = f"lap_table_{i:02}.png"
        f.write(f"file '{os.path.join(IMG_FOLDER, img_file)}'\n")
        f.write(f"duration {duration}\n")
        print(img_file)



    # Hold last frame for LAST_HOLD_DURATION seconds
    last_img = f"lap_table_{i+1:02}.png"
    print(last_img)
    f.write(f"file '{os.path.join(IMG_FOLDER, last_img)}'\n")
    f.write(f"duration {LAST_HOLD_DURATION}\n")

    # Repeat last image once more (ffmpeg requirement)
    f.write(f"file '{os.path.join(IMG_FOLDER, last_img)}'\n")
    f.write(f"duration {LAST_HOLD_DURATION}\n")

# # Step 2: Run ffmpeg
subprocess.run([
    "ffmpeg",
    "-y",
    "-f", "concat",
    "-safe", "0",
    "-i", FFMPEG_INPUT_FILE,
    "-vsync", "vfr",
    "-pix_fmt", "yuv420p",
    OUTPUT_VIDEO
], check=True)

print(f"✅ Video saved as {OUTPUT_VIDEO}")