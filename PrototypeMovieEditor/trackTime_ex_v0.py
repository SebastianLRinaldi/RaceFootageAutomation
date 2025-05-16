# import cv2
# import numpy as np

# video_path = 'main_bg.mp4'
# output_path = 'edited_output.mp4'

# lap_times = [
#     {"lap": 1, "start": 0, "end": 75.4},
#     {"lap": 2, "start": 75.4, "end": 149.2},
#     {"lap": 3, "start": 149.2, "end": 224.0},
# ]

# # Precompute lap durations
# for lap in lap_times:
#     lap["duration"] = lap["end"] - lap["start"]
# fastest = min(lap_times, key=lambda x: x["duration"])

# cap = cv2.VideoCapture(video_path)
# fps = cap.get(cv2.CAP_PROP_FPS)
# frame_width = int(cap.get(3))
# frame_height = int(cap.get(4))
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(output_path, fourcc, fps, (frame_width, frame_height))

# font = cv2.FONT_HERSHEY_SIMPLEX
# frame_idx = 0

# def draw_lap_table(frame):
#     y_offset = 30
#     for lap in lap_times:
#         color = (0, 255, 0) if lap == fastest else (255, 255, 255)
#         text = f"Lap {lap['lap']}: {lap['duration']:.2f}s"
#         cv2.putText(frame, text, (frame_width - 320, y_offset), font, 0.6, color, 1)
#         y_offset += 25

# def draw_flash(frame):
#     overlay = frame.copy()
#     cv2.rectangle(overlay, (0, 0), (frame_width, frame_height), (0, 0, 255), -1)
#     return cv2.addWeighted(overlay, 0.3, frame, 0.7, 0)

# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     current_time = frame_idx / fps
#     timer_text = ""
#     draw_flash_flag = False

#     # Find current lap and elapsed time
#     for lap in lap_times:
#         if lap["start"] <= current_time < lap["end"]:
#             elapsed = current_time - lap["start"]
#             fade_in = min(1.0, elapsed / 2.0)
#             color = tuple(int(c * fade_in) for c in (0, 255, 255))  # Yellow fade

#             timer_text = f"Lap {lap['lap']} Timer: {elapsed:.2f}s"

#             # Delta time vs fastest lap
#             delta = elapsed - fastest["duration"]
#             delta_color = (0, 255, 0) if delta < 0 else (0, 0, 255)  # Green if faster else red
#             delta_sign = "-" if delta < 0 else "+"
#             delta_text = f"Delta vs Fastest: {delta_sign}{abs(delta):.2f}s"

#             # Lap progress bar
#             bar_width = 400
#             bar_height = 20
#             bar_x = 50
#             bar_y = frame_height - 50
#             progress = elapsed / lap["duration"]
#             progress = min(max(progress, 0), 1)

#             # Draw progress bar background
#             cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (50, 50, 50), -1)
#             # Draw progress bar fill
#             progress_width = int(bar_width * progress)
#             cv2.rectangle(frame, (bar_x, bar_y), (bar_x + progress_width, bar_y + bar_height), (255, 255, 0), -1)
#             # Draw border
#             cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255), 2)

#             break
#         elif abs(current_time - lap["end"]) < 0.5:
#             draw_flash_flag = True

#     if draw_flash_flag:
#         frame = draw_flash(frame)

#     draw_lap_table(frame)

#     if timer_text:
#         cv2.putText(frame, timer_text, (50, 50), font, 0.8, color, 2)
#         cv2.putText(frame, delta_text, (50, 90), font, 0.7, delta_color, 2)

#     # Show frame live
#     cv2.imshow('Editing Preview', frame)
#     if cv2.waitKey(1) & 0xFF == ord('q'):  # Press 'q' to stop early
#         break

#     out.write(frame)
#     frame_idx += 1

# cap.release()
# out.release()
# cv2.destroyAllWindows()


import cv2
import numpy as np
import os
import subprocess

# ------------------------- CONFIG -------------------------
input_video = "main_bg.mp4"
output_video = "final_output.mp4"
fps = 30
width, height = 1280, 720
overlay_dir = "overlay_frames"

lap_times = [
    {"lap": 1, "start": 0, "end": 75.4},
    {"lap": 2, "start": 75.4, "end": 149.2},
    {"lap": 3, "start": 149.2, "end": 224.0},
]
# ----------------------------------------------------------

for lap in lap_times:
    lap["duration"] = lap["end"] - lap["start"]
fastest = min(lap_times, key=lambda x: x["duration"])

frame_count = int(lap_times[-1]["end"] * fps)
font = cv2.FONT_HERSHEY_SIMPLEX
os.makedirs(overlay_dir, exist_ok=True)


def make_frame_overlay(current_time):
    frame = np.zeros((height, width, 4), dtype=np.uint8)
    for lap in lap_times:
        if lap["start"] <= current_time < lap["end"]:
            elapsed = current_time - lap["start"]
            fade_in = min(1.0, elapsed / 2.0)
            color = (0, int(255 * fade_in), int(255 * fade_in), int(255 * fade_in))

            timer_text = f"Lap {lap['lap']} Timer: {elapsed:.2f}s"
            delta = elapsed - fastest["duration"]
            delta_color = (0, 255, 0, 255) if delta < 0 else (0, 0, 255, 255)
            delta_sign = "-" if delta < 0 else "+"
            delta_text = f"Δ vs Fastest: {delta_sign}{abs(delta):.2f}s"

            cv2.putText(frame, timer_text, (50, 50), font, 0.8, color, 2, cv2.LINE_AA)
            cv2.putText(frame, delta_text, (50, 90), font, 0.7, delta_color, 2, cv2.LINE_AA)

            # Progress bar
            bar_width = 400
            bar_height = 20
            bar_x = 50
            bar_y = height - 50
            progress = elapsed / lap["duration"]
            fill_w = int(bar_width * progress)

            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (80, 80, 80, 180), -1)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + fill_w, bar_y + bar_height), (255, 255, 0, 255), -1)
            cv2.rectangle(frame, (bar_x, bar_y), (bar_x + bar_width, bar_y + bar_height), (255, 255, 255, 255), 2)
            break
    return frame


print("🎬 Generating overlay frames...")
for i in range(frame_count):
    t = i / fps
    frame = make_frame_overlay(t)
    cv2.imwrite(f"{overlay_dir}/frame_{i:05d}.png", frame)

print("🎞️  Converting to transparent video...")
subprocess.run([
    "ffmpeg", "-y",
    "-framerate", str(fps),
    "-i", f"{overlay_dir}/frame_%05d.png",
    "-c:v", "libvpx-vp9",
    "-pix_fmt", "yuva420p",
    "-b:v", "2M",
    "overlay.webm"
], check=True)

print("🔀 Merging overlay with input video...")
subprocess.run([
    "ffmpeg", "-y",
    "-i", input_video,
    "-i", "overlay.webm",
    "-filter_complex", "[0:v][1:v]overlay=shortest=1[outv]",
    "-map", "[outv]", "-map", "0:a",
    "-c:a", "copy",
    output_video
], check=True)

print(f"✅ Done. Final video saved to: {output_video}")
