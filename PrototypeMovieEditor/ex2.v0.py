# import numpy as np
# from moviepy import VideoClip
# from PIL import Image, ImageDraw, ImageFont

# lap_times = [28.999, 25.844, 27.111]
# countdown_time = 5
# total_duration = countdown_time + sum(lap_times)

# try:
#     font = ImageFont.truetype("arial.ttf", 40)
# except IOError:
#     font = ImageFont.load_default()

# def pil_to_np(img):
#     return np.array(img)

# def make_frame(t):
#     img = Image.new("RGB", (800, 600), (0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     if t < countdown_time:
#         count = int(countdown_time - t) + 1
#         draw.text((350, 250), f"{count}", fill="white", font=font)
#         draw.text((250, 320), "Get Ready...", fill="white", font=font)
#     else:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed
#         for lt in lap_times:
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         draw.text((50, 50), f"Time: {time_in_lap:.3f}s", fill="white", font=font)
#         draw.text((50, 100), f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", fill="white", font=font)

#         y = 200
#         draw.text((50, y), "Completed Laps:", fill="white", font=font)
#         for i in range(min(lap, len(lap_times))):
#             y += 40
#             draw.text((70, y), f"Lap {i + 1}: {lap_times[i]:.3f}s", fill="white", font=font)

#     return pil_to_np(img)

# clip = VideoClip(make_frame, duration=total_duration)
# clip.write_videofile("lap_overlay_countdown.mp4", fps=30, codec="libx264")


 
# import numpy as np
# from moviepy import VideoClip
# from PIL import Image, ImageDraw, ImageFont

# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231, 25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544, 23.424, 22.756, 22.609, 22.474, None]
# countdown_time = 5
# total_duration = countdown_time + sum(lap_times)

# try:
#     font = ImageFont.truetype("arial.ttf", 40)
# except IOError:
#     font = ImageFont.load_default()

# def pil_to_np(img):
#     return np.array(img)

# def draw_table(draw, x, y, lap_times, font):
#     col1_w, col2_w = 100, 200
#     row_h = 40


#     def center_text(text, x_start, width, y_start, height):
#         bbox = draw.textbbox((0, 0), text, font=font)
#         w = bbox[2] - bbox[0]
#         h = bbox[3] - bbox[1]
#         # PIL's text drawing y-position is baseline, so add adjustment:
#         y_pos = y_start + (height - h) / 2 - bbox[1]  # subtract top bbox offset
#         x_pos = x_start + (width - w) / 2
#         return x_pos, y_pos

#     # Header
#     draw.rectangle([x, y, x + col1_w + col2_w, y + row_h], outline="white")
#     draw.line([x + col1_w, y, x + col1_w, y + row_h], fill="white")

#     lap_text_pos = center_text("Lap", x, col1_w, y, row_h)
#     time_text_pos = center_text("Time (s)", x + col1_w, col2_w, y, row_h)
#     draw.text(lap_text_pos, "Lap", fill="white", font=font)
#     draw.text(time_text_pos, "Time (s)", fill="white", font=font)

#     # Rows
#     for i, t in enumerate(lap_times):
#         top = y + row_h * (i + 1)
#         draw.rectangle([x, top, x + col1_w + col2_w, top + row_h], outline="white")
#         draw.line([x + col1_w, top, x + col1_w, top + row_h], fill="white")

#         lap_num = str(i + 1)
#         lap_pos = center_text(lap_num, x, col1_w, top, row_h)
#         time_pos = center_text(f"{t:.3f}", x + col1_w, col2_w, top, row_h)
#         draw.text(lap_pos, lap_num, fill="white", font=font)
#         draw.text(time_pos, f"{t:.3f}", fill="white", font=font)


# def make_frame(t):
#     img = Image.new("RGB", (800, 600), (0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     if t < countdown_time:
#         count = int(countdown_time - t) + 1
#         draw.text((350, 250), f"{count}", fill="white", font=font)
#         draw.text((250, 320), "Get Ready...", fill="white", font=font)
#     else:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed
#         for lt in lap_times:
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         draw.text((50, 50), f"Time: {time_in_lap:.3f}s", fill="white", font=font)
#         draw.text((50, 100), f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", fill="white", font=font)

#         if lap > 0:
#             draw.text((50, 150), "Completed Laps:", fill="white", font=font)
#             draw_table(draw, 50, 200, lap_times[:lap], font=font)

#     return pil_to_np(img)

# clip = VideoClip(make_frame, duration=total_duration)
# clip.write_videofile("lap_overlay_countdown.mp4", fps=30, codec="libx264")




# import numpy as np
# from moviepy import VideoClip
# from PIL import Image, ImageDraw, ImageFont

# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231, 25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544, 23.424, 22.756, 22.609, 22.474, None]
# countdown_time = 5
# total_duration = countdown_time + sum(t for t in lap_times if t is not None)

# try:
#     font = ImageFont.truetype("arial.ttf", 40)
# except IOError:
#     font = ImageFont.load_default()

# def pil_to_np(img):
#     return np.array(img)

# def draw_table(draw, x, y, lap_times, font):
#     col1_w, col2_w = 100, 200
#     row_h = 40

#     def center_text(text, x_start, width, y_start, height):
#         bbox = draw.textbbox((0, 0), text, font=font)
#         w = bbox[2] - bbox[0]
#         h = bbox[3] - bbox[1]
#         y_pos = y_start + (height - h) / 2 - bbox[1]
#         x_pos = x_start + (width - w) / 2
#         return x_pos, y_pos

#     # Header
#     draw.rectangle([x, y, x + col1_w + col2_w, y + row_h], outline="white")
#     draw.line([x + col1_w, y, x + col1_w, y + row_h], fill="white")

#     lap_text_pos = center_text("Lap", x, col1_w, y, row_h)
#     time_text_pos = center_text("Time (s)", x + col1_w, col2_w, y, row_h)
#     draw.text(lap_text_pos, "Lap", fill="white", font=font)
#     draw.text(time_text_pos, "Time (s)", fill="white", font=font)

#     # Rows
#     for i, t in enumerate(lap_times):
#         top = y + row_h * (i + 1)
#         draw.rectangle([x, top, x + col1_w + col2_w, top + row_h], outline="white")
#         draw.line([x + col1_w, top, x + col1_w, top + row_h], fill="white")

#         lap_num = str(i + 1)
#         time_str = f"{t:.3f}" if t is not None else "—"
#         lap_pos = center_text(lap_num, x, col1_w, top, row_h)
#         time_pos = center_text(time_str, x + col1_w, col2_w, top, row_h)
#         draw.text(lap_pos, lap_num, fill="white", font=font)
#         draw.text(time_pos, time_str, fill="white", font=font)

# def make_frame(t):
#     img = Image.new("RGB", (800, 600), (0, 0, 0))
#     draw = ImageDraw.Draw(img)

#     if t < countdown_time:
#         count = max(1, int(np.ceil(countdown_time - t)))
#         draw.text((350, 250), f"{count}", fill="white", font=font)
#         draw.text((250, 320), "Get Ready...", fill="white", font=font)
#     else:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed

#         for lt in lap_times:
#             if lt is None:
#                 break
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         draw.text((50, 50), f"Time: {time_in_lap:.3f}s", fill="white", font=font)
#         draw.text((50, 100), f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", fill="white", font=font)

#         if lap > 0:
#             draw.text((50, 150), "Completed Laps:", fill="white", font=font)
#             draw_table(draw, 50, 200, lap_times[:lap], font=font)

#     return pil_to_np(img)

# clip = VideoClip(make_frame, duration=total_duration)
# clip.write_videofile("lap_overlay_countdown.mp4", fps=30, codec="libx264")



# import subprocess

# def remove_black_bg(input_file, output_file):
#     cmd = [
#         "ffmpeg",
#         "-i", input_file,
#         "-vf", "colorkey=black:0.1:0.0",
#         "-c:v", "png",
#         "-pix_fmt", "rgba",
#         output_file
#     ]
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     if result.returncode != 0:
#         print("Error:", result.stderr)
#     else:
#         print(f"Output saved to {output_file}")

# if __name__ == "__main__":
#     input_path = "lap_overlay_countdown.mp4"  # Replace with your input file
#     output_path = "no_bg_output.mov"  # Output with transparency support
#     remove_black_bg(input_path, output_path)






# import skia
# import numpy as np
# from multiprocessing import Pool, cpu_count
# import subprocess
# from tqdm import tqdm

# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474, None]
# countdown_time = 5

# WIDTH, HEIGHT = 800, 600
# FPS = 30
# total_duration = countdown_time + sum(t for t in lap_times if t is not None)
# total_frames = int(total_duration * FPS)

# font = skia.Font(skia.Typeface('Arial'), 40)
# paint_text = skia.Paint(Color=skia.ColorWHITE)
# paint_line = skia.Paint(Color=skia.ColorWHITE, Style=skia.Paint.kStroke_Style, StrokeWidth=2)

# def draw_text(canvas, text, x, y, font):
#     canvas.drawString(text, x, y, font, paint_text)

# def draw_table(canvas, x, y, lap_times):
#     col1_w, col2_w = 100, 200
#     row_h = 40
#     canvas.drawRect(skia.Rect.MakeXYWH(x, y, col1_w + col2_w, row_h), paint_line)
#     canvas.drawLine(x + col1_w, y, x + col1_w, y + row_h, paint_line)
#     canvas.drawString("Lap", x + col1_w/2 - 15, y + 30, font, paint_text)
#     canvas.drawString("Time (s)", x + col1_w + col2_w/2 - 60, y + 30, font, paint_text)
#     for i, t in enumerate(lap_times):
#         top = y + row_h * (i + 1)
#         canvas.drawRect(skia.Rect.MakeXYWH(x, top, col1_w + col2_w, row_h), paint_line)
#         canvas.drawLine(x + col1_w, top, x + col1_w, top + row_h, paint_line)
#         lap_num = str(i + 1)
#         time_str = f"{t:.3f}" if t is not None else "—"
#         canvas.drawString(lap_num, x + col1_w/2 - 10, top + 30, font, paint_text)
#         canvas.drawString(time_str, x + col1_w + col2_w/2 - 50, top + 30, font, paint_text)

# def render_frame(frame_idx):
#     try:
#         t = frame_idx / FPS
#         surface = skia.Surface(WIDTH, HEIGHT)
#         canvas = surface.getCanvas()
#         canvas.clear(skia.ColorBLACK)

#         if t < countdown_time:
#             count = max(1, int(countdown_time - t + 1))
#             draw_text(canvas, str(count), 350, 300, font)
#             draw_text(canvas, "Get Ready...", 250, 350, font)
#         else:
#             lap_time_passed = t - countdown_time
#             lap = 0
#             time_in_lap = lap_time_passed

#             for lt in lap_times:
#                 if lt is None:
#                     break
#                 if time_in_lap < lt:
#                     break
#                 time_in_lap -= lt
#                 lap += 1

#             draw_text(canvas, f"Time: {time_in_lap:.3f}s", 50, 80, font)
#             draw_text(canvas, f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", 50, 130, font)

#             if lap > 0:
#                 draw_text(canvas, "Completed Laps:", 50, 180, font)
#                 draw_table(canvas, 50, 220, lap_times[:lap])

#         img = surface.makeImageSnapshot()
#         img_bytes = img.tobytes()
#         return img_bytes
#     except Exception as e:
#         print(f"Error rendering frame {frame_idx}: {e}")
#         # Return a black frame to keep video consistent
#         return b'\x00' * (WIDTH * HEIGHT * 4)

# def main():
#     ffmpeg_cmd = [
#         'ffmpeg',
#         '-y',
#         '-f', 'rawvideo',
#         '-pixel_format', 'rgba',
#         '-video_size', f'{WIDTH}x{HEIGHT}',
#         '-framerate', str(FPS),
#         '-i', '-',
#         '-c:v', 'libx264',
#         '-pix_fmt', 'yuv420p',
#         'lap_overlay_countdown.mp4'
#     ]

#     with subprocess.Popen(ffmpeg_cmd, stdin=subprocess.PIPE) as proc:
#         with Pool(cpu_count()) as pool:
#             for img_bytes in tqdm(pool.imap(render_frame, range(total_frames), chunksize=10), total=total_frames):
#                 proc.stdin.write(img_bytes)
#         proc.stdin.close()
#         proc.wait()

# if __name__ == "__main__":
#     main()




# import cv2
# import numpy as np

# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474, None]

# countdown_time = 5
# total_duration = countdown_time + sum(t for t in lap_times if t is not None)

# width, height = 800, 600
# fps = 30

# # Precalculate font settings for OpenCV
# font = cv2.FONT_HERSHEY_SIMPLEX
# font_scale = 1
# thickness = 2
# white = (255, 255, 255)

# def draw_centered_text(img, text, x, y, font, font_scale, thickness, color):
#     (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
#     pos = (int(x - text_w / 2), int(y + text_h / 2))
#     cv2.putText(img, text, pos, font, font_scale, color, thickness, lineType=cv2.LINE_AA)

# def draw_table(img, x, y, lap_times):
#     col1_w, col2_w = 100, 200
#     row_h = 40

#     # Draw header
#     cv2.rectangle(img, (x, y), (x + col1_w + col2_w, y + row_h), white, 1)
#     cv2.line(img, (x + col1_w, y), (x + col1_w, y + row_h), white, 1)

#     draw_centered_text(img, "Lap", x + col1_w // 2, y + row_h // 2, font, 0.8, 1, white)
#     draw_centered_text(img, "Time (s)", x + col1_w + col2_w // 2, y + row_h // 2, font, 0.8, 1, white)

#     # Draw rows
#     for i, t in enumerate(lap_times):
#         top = y + row_h * (i + 1)
#         cv2.rectangle(img, (x, top), (x + col1_w + col2_w, top + row_h), white, 1)
#         cv2.line(img, (x + col1_w, top), (x + col1_w, top + row_h), white, 1)

#         lap_num = str(i + 1)
#         time_str = f"{t:.3f}" if t is not None else "—"

#         draw_centered_text(img, lap_num, x + col1_w // 2, top + row_h // 2, font, 0.7, 1, white)
#         draw_centered_text(img, time_str, x + col1_w + col2_w // 2, top + row_h // 2, font, 0.7, 1, white)

# def make_frame(t):
#     img = np.zeros((height, width, 3), dtype=np.uint8)

#     if t < countdown_time:
#         count = max(1, int(np.ceil(countdown_time - t)))
#         draw_centered_text(img, str(count), width // 2, height // 2 - 20, font, 3, 3, white)
#         draw_centered_text(img, "Get Ready...", width // 2, height // 2 + 40, font, 1, 2, white)
#     else:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed

#         for lt in lap_times:
#             if lt is None:
#                 break
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         # Show timer and lap info
#         cv2.putText(img, f"Time: {time_in_lap:.3f}s", (50, 50), font, 1, white, 2, cv2.LINE_AA)
#         cv2.putText(img, f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", (50, 100), font, 1, white, 2, cv2.LINE_AA)

#         if lap > 0:
#             cv2.putText(img, "Completed Laps:", (50, 150), font, 1, white, 2, cv2.LINE_AA)
#             draw_table(img, 50, 200, lap_times[:lap])

#     return img

# # Optional: write video
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('lap_overlay_countdown_opencv.mp4', fourcc, fps, (width, height))

# # for frame_i in range(int(total_duration * fps)):
# #     t = frame_i / fps
# #     frame = make_frame(t)
# #     out.write(frame)

# # import sys

# # total_frames = int(total_duration * fps)
# # for frame_i in range(total_frames):
# #     t = frame_i / fps
# #     frame = make_frame(t)
# #     out.write(frame)

# #     # Progress bar in console
# #     progress = (frame_i + 1) / total_frames
# #     bar_length = 40
# #     filled_length = int(bar_length * progress)
# #     bar = '=' * filled_length + '-' * (bar_length - filled_length)
# #     sys.stdout.write(f'\rRendering frames: [{bar}] {progress*100:.1f}%')
# #     sys.stdout.flush()
# from tqdm import tqdm

# total_frames = int(total_duration * fps)

# for frame_i in tqdm(range(total_frames), desc="Rendering frames"):
#     t = frame_i / fps
#     frame = make_frame(t)
#     out.write(frame)

# out.release()
# print("Done.")



# import cv2
# import numpy as np

# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474, None]

# countdown_time = 5
# total_duration = countdown_time + sum(t for t in lap_times if t is not None)

# width, height = 500, 2000
# fps = 30

# font = cv2.FONT_HERSHEY_SIMPLEX
# thickness = 2
# white = (255, 255, 255)

# def draw_centered_text(img, text, x, y, font, font_scale, thickness, color):
#     (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
#     pos = (int(x - text_w / 2), int(y + text_h / 2))
#     cv2.putText(img, text, pos, font, font_scale, color, thickness, lineType=cv2.LINE_AA)

# def draw_table(img, x, y, lap_times):
#     col1_w, col2_w = 100, 200
#     total_rows = len(lap_times) + 1  # +1 for header
#     max_height = height - y - 20  # leave bottom margin
#     row_h = max(20, min(40, max_height // total_rows))

#     font_scale_header = row_h / 40 * 0.8
#     font_scale_row = row_h / 40 * 0.7
#     thickness_scaled = 1

#     # Header
#     cv2.rectangle(img, (x, y), (x + col1_w + col2_w, y + row_h), white, 1)
#     cv2.line(img, (x + col1_w, y), (x + col1_w, y + row_h), white, 1)
#     draw_centered_text(img, "Lap", x + col1_w // 2, y + row_h // 2, font, font_scale_header, thickness_scaled, white)
#     draw_centered_text(img, "Time (s)", x + col1_w + col2_w // 2, y + row_h // 2, font, font_scale_header, thickness_scaled, white)

#     # Rows
#     for i, t in enumerate(lap_times):
#         top = y + row_h * (i + 1)
#         cv2.rectangle(img, (x, top), (x + col1_w + col2_w, top + row_h), white, 1)
#         cv2.line(img, (x + col1_w, top), (x + col1_w, top + row_h), white, 1)

#         lap_num = str(i + 1)
#         time_str = f"{t:.3f}" if t is not None else "—"

#         draw_centered_text(img, lap_num, x + col1_w // 2, top + row_h // 2, font, font_scale_row, thickness_scaled, white)
#         draw_centered_text(img, time_str, x + col1_w + col2_w // 2, top + row_h // 2, font, font_scale_row, thickness_scaled, white)

# def make_frame(t):
#     img = np.zeros((height, width, 3), dtype=np.uint8)

#     if t < countdown_time:
#         count = max(1, int(np.ceil(countdown_time - t)))
#         draw_centered_text(img, str(count), width // 2, height // 2 - 20, font, 3, 3, white)
#         draw_centered_text(img, "Get Ready...", width // 2, height // 2 + 40, font, 1, 2, white)
#     else:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed

#         for lt in lap_times:
#             if lt is None:
#                 break
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         cv2.putText(img, f"Time: {time_in_lap:.3f}s", (50, 50), font, 1, white, 2, cv2.LINE_AA)
#         cv2.putText(img, f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", (50, 100), font, 1, white, 2, cv2.LINE_AA)

#         if lap > 0:
#             cv2.putText(img, "Completed Laps:", (50, 150), font, 1, white, 2, cv2.LINE_AA)
#             draw_table(img, 50, 200, lap_times[:lap])

#     return img

# # Optional: write video
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter('lap_overlay_countdown_opencv.mp4', fourcc, fps, (width, height))

# for i in range(int(total_duration * fps)):
#     t = i / fps
#     frame = make_frame(t)
#     out.write(frame)

# out.release()



# import cv2
# import numpy as np

# lap_times = [24.459, 23.888, 22.623, 23.368, 23.087, 24.201, 22.646, 22.654, 25.23, 23.231,
#              25.676, 22.721, 22.708, 23.561, 26.509, 22.933, 22.871, 22.643, 22.671, 23.544,
#              23.424, 22.756, 22.609, 22.474, None]

# countdown_time = 5
# total_duration = countdown_time + sum(t for t in lap_times if t is not None)

# fps = 30
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')

# # Video sizes: timer smaller, table taller
# timer_size = (500, 200)  # width x height
# table_size = (500, 1500)

# font = cv2.FONT_HERSHEY_DUPLEX
# white = (255, 255, 255)



# def draw_centered_text(img, text, x, y, font, font_scale, thickness, color):
#     (text_w, text_h), _ = cv2.getTextSize(text, font, font_scale, thickness)
#     pos = (int(x - text_w / 2), int(y + text_h / 2))
#     cv2.putText(img, text, pos, font, font_scale, color, thickness, lineType=cv2.LINE_AA)

# def draw_table(img, x, y, lap_times):
#     col1_w, col2_w = 100, 200
#     total_rows = len(lap_times) + 1  # header
#     max_height = table_size[1] - y - 20
#     row_h = max(20, min(40, max_height // total_rows))

#     font_scale_header = row_h / 40 * 0.8
#     font_scale_row = row_h / 40 * 0.7
#     thickness_scaled = 1

#     # Header
#     cv2.rectangle(img, (x, y), (x + col1_w + col2_w, y + row_h), white, 1)
#     cv2.line(img, (x + col1_w, y), (x + col1_w, y + row_h), white, 1)
#     draw_centered_text(img, "Lap", x + col1_w // 2, y + row_h // 2, font, font_scale_header, thickness_scaled, white)
#     draw_centered_text(img, "Time (s)", x + col1_w + col2_w // 2, y + row_h // 2, font, font_scale_header, thickness_scaled, white)

#     # Rows
#     for i, t in enumerate(lap_times):
#         top = y + row_h * (i + 1)
#         cv2.rectangle(img, (x, top), (x + col1_w + col2_w, top + row_h), white, 1)
#         cv2.line(img, (x + col1_w, top), (x + col1_w, top + row_h), white, 1)

#         lap_num = str(i + 1)
#         time_str = f"{t:.3f}" if t is not None else "—"

#         draw_centered_text(img, lap_num, x + col1_w // 2, top + row_h // 2, font, font_scale_row, thickness_scaled, white)
#         draw_centered_text(img, time_str, x + col1_w + col2_w // 2, top + row_h // 2, font, font_scale_row, thickness_scaled, white)

# def make_timer_frame(t):
#     img = np.zeros((timer_size[1], timer_size[0], 3), dtype=np.uint8)

#     if t < countdown_time:
#         count = max(1, int(np.ceil(countdown_time - t)))
#         draw_centered_text(img, str(count), timer_size[0] // 2, timer_size[1] // 2 - 20, font, 3, 3, white)
#         draw_centered_text(img, "Get Ready...", timer_size[0] // 2, timer_size[1] // 2 + 40, font, 1, 2, white)
#     else:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed

#         for lt in lap_times:
#             if lt is None:
#                 break
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         cv2.putText(img, f"Time: {time_in_lap:.3f}s", (50, 50), font, 1, white, 2, cv2.LINE_AA)
#         cv2.putText(img, f"Lap: {min(lap + 1, len(lap_times))}/{len(lap_times)}", (50, 100), font, 1, white, 2, cv2.LINE_AA)

#     return img

# def make_table_frame(t):
#     img = np.zeros((table_size[1], table_size[0], 3), dtype=np.uint8)

#     # if t >= countdown_time:
#     #     lap_time_passed = t - countdown_time
#     #     lap = 0
#     #     time_in_lap = lap_time_passed

#     #     for lt in lap_times:
#     #         if lt is None:
#     #             break
#     #         if time_in_lap < lt:
#     #             break
#     #         time_in_lap -= lt
#     #         lap += 1

#     #     if lap > 0:
#     #         cv2.putText(img, "Completed Laps:", (50, 50), font, 1, white, 2, cv2.LINE_AA)
#     #         draw_table(img, 50, 100, lap_times[:lap])

#     # return img





#     if t >= countdown_time:
#         lap_time_passed = t - countdown_time
#         lap = 0
#         time_in_lap = lap_time_passed

#         for lt in lap_times:
#             if lt is None:
#                 break
#             if time_in_lap < lt:
#                 break
#             time_in_lap -= lt
#             lap += 1

#         cv2.putText(img, "Completed Laps:", (50, 50), font, 1, white, 2, cv2.LINE_AA)
#         draw_table(img, 50, 100, lap_times[:lap])  # handles lap=0: just draws headers

#     return img

# out_timer = cv2.VideoWriter('lap_timer.mp4', fourcc, fps, timer_size)
# out_table = cv2.VideoWriter('lap_table.mp4', fourcc, fps, table_size)

# from tqdm import tqdm

# total_frames = int(total_duration * fps)
# for i in tqdm(range(total_frames), desc="Rendering video"):
#     t = i / fps
#     out_timer.write(make_timer_frame(t))
#     out_table.write(make_table_frame(t))

# out_timer.release()
# out_table.release()





import subprocess

def remove_black_bg(input_file, output_file):
    cmd = [
        "ffmpeg",
        "-i", input_file,
        "-vf", "colorkey=black:0.1:0.0",
        "-c:v", "png",
        "-pix_fmt", "rgba",
        output_file
    ]
    result = subprocess.run(cmd, text=True)
    if result.returncode != 0:
        print("Error:", result.stderr)
    else:
        print(f"Output saved to {output_file}")

if __name__ == "__main__":
    input_path1 = "lap_timer.mp4"  
    output_path1 = "lap_timer_no_bg.mov"
    input_path2 = "lap_table.mp4"  
    output_path2 = "lap_table_no_bg.mov"# Output with transparency support
    remove_black_bg(input_path1, output_path1)
    remove_black_bg(input_path2, output_path2)



