import os
import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
             25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
             23.424, 22.756, 22.609, 22.474, None]

countdown_time = 5

total_duration = countdown_time + sum(t for t in lap_times if t is not None)
post_finish_duration = 15  # seconds to show Finished + full table
final_duration = total_duration + post_finish_duration

fps = 60
fourcc = cv2.VideoWriter_fourcc(*'mp4v')

timer_size = (500, 200)
table_size = (500, 1500)

output_dir = "overlay_videos"
os.makedirs(output_dir, exist_ok=True)  # Create if doesn't exist

timer_path = os.path.join(output_dir, "lap_timer.mp4")
table_path = os.path.join(output_dir, "lap_table.mp4")


white = (255, 255, 255)
font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

"""
Helvetica Neue 
Helvetica
Xanh Mono | Don't have
all-caps Helvetica 
Matisse EB (Jap Font) | Dont ahve
Microsoft Sans Serif = sans-serif
Times New Roman
TT-JTCE'EE'CE'i`M9 
TT-JTCE'EE'CE'i`M9P | True Eva
TT-NISi:e^ :n~i'(c)e:A~W3 | True Eva
TT-NISi:e^ :n~i'(c)e:A~W3P
TT-NIS平成明朝体W9 | Best Eva
TT-n~xn~i'(c) | Close Eva
TT-n~xn~i'(c)P
"""

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

def make_timer_frame(t):
    img = np.zeros((timer_size[1], timer_size[0], 3), dtype=np.uint8)
    if t < countdown_time:
        count = max(1, int(np.ceil(countdown_time - t)))
        img = draw_centered_text_pil(img, str(count), timer_size[0] // 2, timer_size[1] // 2 - 20, 64, white)
        img = draw_centered_text_pil(img, "Get Ready...", timer_size[0] // 2, timer_size[1] // 2 + 40, 32, white)
    else:
        lap_time_passed = t - countdown_time
        total_lap_time = sum(t for t in lap_times if t is not None)
        if lap_time_passed >= total_lap_time:
            img = draw_centered_text_pil(img, "Finished", timer_size[0] // 2, timer_size[1] // 2, 48, white)
        else:
            lap = 0
            time_in_lap = lap_time_passed
            for lt in lap_times:
                if lt is None: break
                if time_in_lap < lt: break
                time_in_lap -= lt
                lap += 1
            if lap < len(lap_times) and lap_times[lap] is None:
                img = draw_centered_text_pil(img, "Time: N/A", 250, 60, 28, white)
            else:
                img = draw_centered_text_pil(img, f"Time: {time_in_lap:.3f}s", 250, 60, 28, white)
            img = draw_centered_text_pil(img, f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", 250, 120, 28, white)

    return img

def make_table_frame(t):
    img = np.zeros((table_size[1], table_size[0], 3), dtype=np.uint8)
    if t >= countdown_time:
        lap_time_passed = t - countdown_time
        total_lap_time = sum(t for t in lap_times if t is not None)
        if lap_time_passed >= total_lap_time:
            completed_laps = lap_times
        else:
            lap = 0
            time_in_lap = lap_time_passed
            for lt in lap_times:
                if lt is None: break
                if time_in_lap < lt: break
                time_in_lap -= lt
                lap += 1
            completed_laps = lap_times[:lap]
        img = draw_centered_text_pil(img, "Completed Laps:", 250, 40, 32, white)
        img = draw_table(img, 100, 100, completed_laps)
    return img


# out_timer = cv2.VideoWriter(timer_path, fourcc, fps, timer_size)
# out_table = cv2.VideoWriter(table_path, fourcc, fps, table_size)

# from tqdm import tqdm


# preview_duration = 15  # seconds
# fps_preview = 30
# total_preview_frames = int(preview_duration * fps_preview)

# for i in range(total_preview_frames):
#     t = i / fps_preview
#     frame = make_timer_frame(t)
#     cv2.imshow('Timer Preview', frame)
#     if cv2.waitKey(int(1000 / fps_preview)) & 0xFF == 27:  # ESC to exit early
#         break

# cv2.destroyAllWindows()



# # Preview overlay at 3 seconds
# preview_time = 560.0
# cv2.namedWindow('Timer Preview', cv2.WINDOW_NORMAL)
# cv2.namedWindow('Table Preview', cv2.WINDOW_NORMAL)
# cv2.imshow('Timer Preview', make_timer_frame(preview_time))
# cv2.imshow('Table Preview', make_table_frame(preview_time))
# cv2.waitKey(0)
# cv2.destroyAllWindows()



# total_frames = int(final_duration * fps)
# for i in tqdm(range(total_frames), desc="Rendering video"):
#     t = i / fps
#     out_timer.write(make_timer_frame(t))
#     out_table.write(make_table_frame(t))

# out_timer.release()
# out_table.release()



from multiprocessing import Process

import time

def render_timer(timer_path, fps, final_duration):
    start = time.time()
    out_timer = cv2.VideoWriter(timer_path, fourcc, fps, timer_size)
    total_frames = int(final_duration * fps)
    for i in range(total_frames):
        t = i / fps
        out_timer.write(make_timer_frame(t))
        if i % (fps * 5) == 0:
            elapsed = time.time() - start
            # print(f"[Timer] {i}/{total_frames} frames, elapsed {elapsed:.1f}s")
            print(f"[Timer] {i}/{total_frames} frames, elapsed {elapsed:.1f}s", end='\r', flush=True)

    out_timer.release()
    print(f"Timer done in {time.time() - start:.2f}s")

def render_table(table_path, fps, final_duration):
    start = time.time()
    out_table = cv2.VideoWriter(table_path, fourcc, fps, table_size)
    total_frames = int(final_duration * fps)
    for i in range(total_frames):
        t = i / fps
        out_table.write(make_table_frame(t))
        if i % (fps * 5) == 0:
            elapsed = time.time() - start
            # print(f"[Table] {i}/{total_frames} frames, elapsed {elapsed:.1f}s")
            print(f"[Table] {i}/{total_frames} frames, elapsed {elapsed:.1f}s", end='\r', flush=True)
    out_table.release()
    print(f"Table done in {time.time() - start:.2f}s")

if __name__ == "__main__":
    timer_proc = Process(target=render_timer, args=(timer_path, fps, final_duration))
    # table_proc = Process(target=render_table, args=(table_path, fps, final_duration))

    timer_proc.start()
    # table_proc.start()

    timer_proc.join()
    # table_proc.join()
