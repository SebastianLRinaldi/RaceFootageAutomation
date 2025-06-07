"""
https://github.com/juanmcasillas/gopro2gpx

Simplest wat to get csvs of the data:
https://goprotelemetryextractor.com/free/#

Index 0: video (H264)

Index 1: audio (AAC)

Index 2: data (tmcd) — timecode stream

Index 3: data (gpmd) — GoPro Metadata stream (this is telemetry!)

Index 4: data (fdsc) — likely GoPro sensor data stream (SOS)

Streams 3 and 4 are your telemetry data.

parse these data streams (gpmd and fdsc).



"""

# import subprocess
# import sys

# def run_ffprobe(video_path):
#     cmd = ['ffprobe', '-show_streams', video_path]
#     result = subprocess.run(cmd, capture_output=True, text=True)
#     if result.returncode != 0:
#         print(f"ffprobe error:\n{result.stderr}")
#         sys.exit(1)
#     print(result.stdout)

# if __name__ == "__main__":
#     video = r'F:\_Large\GoKart Vids\GH012596(5-23-25)-R2.MP4' #input("Paste full path to your video file: ").strip()
#     run_ffprobe(video)

import subprocess

import subprocess
import os
import sys
import gopro2gpx

def run_cmd(cmd):
    result = subprocess.run(cmd, capture_output=True, text=True)
    if result.returncode != 0:
        print(f"Command failed: {' '.join(cmd)}")
        print("Error:", result.stderr.strip())
        sys.exit(1)
    return result.stdout

def find_gps_stream(video):
    print("Looking for GPS metadata stream...")
    output = run_cmd(['ffprobe', '-loglevel', 'error', '-show_streams', video])
    lines = output.splitlines()
    for i, line in enumerate(lines):
        if 'codec_tag_string=fdsc' in line:
            for back_line in reversed(lines[:i]):
                if back_line.startswith('index='):
                    stream_idx = back_line.split('=')[1]
                    print(f"GPS metadata stream found at index {stream_idx}")
                    return stream_idx
    print("No GPS metadata stream found in video.")
    sys.exit(1)

def extract_gps(video, stream_idx, out_bin):
    print(f"Extracting GPS metadata stream #{stream_idx} to {out_bin}...")
    cmd = ['ffmpeg', '-y', '-i', video, '-map', f'0:{stream_idx}', '-c', 'copy', '-copy_unknown', '-f', 'data', out_bin]
    run_cmd(cmd)




# import subprocess
# import struct
# import json

# VIDEO_PATH = r"F:\_Large\GoKart Vids\GH012596(5-23-25)-R2.MP4"
# OUTPUT_BIN = "gopro_metadata.bin"

# import subprocess
# import re
# import csv

# VIDEO_PATH = r"F:\_Large\GoKart Vids\GH012596(5-23-25)-R2.MP4"

# def extract_gpmf_data(video_path):
#     result = subprocess.run(['gpmf-parser', '-i', video_path], capture_output=True, text=True)
#     if result.returncode != 0:
#         raise RuntimeError(f"gpmf-parser failed: {result.stderr}")

#     output = result.stdout

#     accel_data = []
#     gyro_data = []

#     pattern = re.compile(r'\[(ACC|GYRO)\]\s+([0-9.]+)\s+([\d\s\-\.]+)')

#     for line in output.splitlines():
#         match = pattern.search(line)
#         if match:
#             sensor, timestamp, values = match.groups()
#             values = [float(v) for v in values.strip().split()]
#             if sensor == 'ACC':
#                 accel_data.append((float(timestamp), *values))
#             else:
#                 gyro_data.append((float(timestamp), *values))

#     return accel_data, gyro_data

# def save_to_csv(filename, data):
#     with open(filename, 'w', newline='') as f:
#         writer = csv.writer(f)
#         writer.writerow(['timestamp', 'x', 'y', 'z'])
#         writer.writerows(data)

# if __name__ == "__main__":
#     acc, gyro = extract_gpmf_data(VIDEO_PATH)
#     save_to_csv('accel.csv', acc)
#     save_to_csv('gyro.csv', gyro)
#     print(f"Saved {len(acc)} accel samples to accel.csv")
#     print(f"Saved {len(gyro)} gyro samples to gyro.csv")







# main()










# import json
# import pandas as pd
# import matplotlib.pyplot as plt

# # Load JSON
# with open('telemetry.json', 'r') as f:
#     data = json.load(f)

# # Example: Access accelerometer data
# # Path may vary depending on GoPro model — inspect JSON!
# accel_data = data['streams']['ACC1']['samples']  # Example key

# # Convert to DataFrame
# df_accel = pd.DataFrame(accel_data)

# # Typically looks like:
# # df_accel['value'] → [X, Y, Z]
# # df_accel['cts'] → timestamp in ms
# df_accel[['accel_x', 'accel_y', 'accel_z']] = pd.DataFrame(df_accel['value'].tolist(), index=df_accel.index)

# # Plot G-force over time
# plt.figure(figsize=(12, 6))
# plt.plot(df_accel['cts'] / 1000.0, df_accel['accel_x'], label='Accel X')
# plt.plot(df_accel['cts'] / 1000.0, df_accel['accel_y'], label='Accel Y')
# plt.plot(df_accel['cts'] / 1000.0, df_accel['accel_z'], label='Accel Z')
# plt.xlabel('Time (s)')
# plt.ylabel('Acceleration (G)')
# plt.legend()
# plt.title('G-Force over Time')
# plt.grid(True)
# plt.show()





import cv2
import csv
import numpy as np

VIDEO_PATH = "input.mp4"
OUTPUT_PATH = "output_with_overlay.mp4"
TELEMETRY_CSV = "GH012596(5-23-25)-R2_HERO8 Black-ACCL.csv"

# # Load telemetry data keyed by timestamp
# telemetry = {}
# with open(TELEMETRY_CSV, newline='') as f:
#     reader = csv.DictReader(f)
#     for row in reader:
#         t = float(row['timestamp'])
#         telemetry[t] = row  # parse floats as needed

# # Open video
# cap = cv2.VideoCapture(VIDEO_PATH)
# fps = cap.get(cv2.CAP_PROP_FPS)
# frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))
# width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
# height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

# # VideoWriter for output (use mp4 codec)
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(OUTPUT_PATH, fourcc, fps, (width, height))

# def closest_telemetry(t):
#     return telemetry[min(telemetry.keys(), key=lambda x: abs(x - t))]

# frame_idx = 0
# while cap.isOpened():
#     ret, frame = cap.read()
#     if not ret:
#         break

#     t = frame_idx / fps  # current time in seconds
#     data = closest_telemetry(t)

#     # Example: Calculate g-force magnitude from accel
#     ax = float(data['accel_x'])
#     ay = float(data['accel_y'])
#     az = float(data['accel_z'])
#     g_force = (ax**2 + ay**2 + az**2)**0.5

#     # Draw overlay text on frame
#     cv2.putText(frame, f"G-Force: {g_force:.2f} g", (50, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)

#     # Write frame
#     out.write(frame)
#     frame_idx += 1

# cap.release()
# out.release()
# print(f"Saved overlay video to {OUTPUT_PATH}")





import cv2
import csv
import numpy as np
import math
from tqdm import tqdm

# Paths
GYRO_CSV = 'GH012596(5-23-25)-R2_HERO8 Black-GYRO.csv'
ACCEL_CSV = 'GH012596(5-23-25)-R2_HERO8 Black-ACCL.csv'
OUTPUT_PATH = 'telemetry_overlay.mp4'

# Video settings
FPS = 30
WIDTH, HEIGHT = 1280, 720
DURATION_SECONDS = 500  # make this match your data length!


"""
gryo
temp_col = next((k for k in row if 'temperature' in k.lower()), None)
if temp_col:
    temp_val = float(row[temp_col])
else:
    temp_val = 0.0

then can do 'temp': temp_val


accel
# Fuzzy lookup of columns:
col_ax = next((k for k in reader.fieldnames if 'accelerometer' in k.lower() and '(x' in k.lower()), None)
col_ay = next((k for k in reader.fieldnames if 'accelerometer' in k.lower() and '(y' in k.lower()), None)
col_az = next((k for k in reader.fieldnames if 'accelerometer' in k.lower() and '(z' in k.lower()), None)
col_temp = next((k for k in reader.fieldnames if 'temperature' in k.lower()), None)

for row in reader:
    t = float(row['cts'])
    temp_val = float(row[col_temp]) if col_temp else 0.0

    telemetry[t] = {
        'accel_z': float(row[col_az]) if col_az else 0.0,
        'accel_x': float(row[col_ax]) if col_ax else 0.0,
        'accel_y': float(row[col_ay]) if col_ay else 0.0,
        'temp': temp_val
    }





"""


# Load gyro CSV
def load_gyro_csv(path):
    telemetry = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        print("CSV GYRO columns:", reader.fieldnames) 
        for row in reader:
            t = float(row['cts'])
            telemetry[t] = {
                'gyro_z': float(row['Gyroscope (z) [rad/s]']),
                'gyro_x': float(row['Gyroscope (x) [rad/s]']),
                'gyro_y': float(row['Gyroscope (y) [rad/s]']),
                'temp': float(row['temperature [Â°C]'])
            }
    return telemetry

# Load accel CSV
def load_accel_csv(path):
    telemetry = {}
    with open(path, newline='') as f:
        reader = csv.DictReader(f)
        print("CSV ACCEL columns:", reader.fieldnames) 
        for row in reader:
            t = float(row['cts'])
            telemetry[t] = {
                'accel_z': float(row['Accelerometer (z) [m/sÂ²]']),
                'accel_x': float(row['Accelerometer (x) [m/sÂ²]']),
                'accel_y': float(row['Accelerometer (y) [m/sÂ²]']),
                'temp': float(row['temperature [Â°C]'])
            }
    return telemetry



# import pandas as pd
# import plotly.graph_objects as go

# # Load CSVs
# gyro_df = pd.read_csv('GH012596(5-23-25)-R2_HERO8 Black-GYRO.csv', encoding='utf-8-sig')
# accel_df = pd.read_csv('GH012596(5-23-25)-R2_HERO8 Black-ACCL.csv', encoding='utf-8-sig')

# # Clean column names if needed
# gyro_df.rename(columns=lambda x: x.replace('Â', ''), inplace=True)
# accel_df.rename(columns=lambda x: x.replace('Â', ''), inplace=True)

# # Plot Gyro
# fig = go.Figure()
# fig.add_trace(go.Scatter(x=gyro_df['cts'], y=gyro_df['Gyroscope (x) [rad/s]'], name='Gyro X'))
# fig.add_trace(go.Scatter(x=gyro_df['cts'], y=gyro_df['Gyroscope (y) [rad/s]'], name='Gyro Y'))
# fig.add_trace(go.Scatter(x=gyro_df['cts'], y=gyro_df['Gyroscope (z) [rad/s]'], name='Gyro Z'))

# # Plot Accel
# fig.add_trace(go.Scatter(x=accel_df['cts'], y=accel_df['Accelerometer (x) [m/s²]'], name='Accel X'))
# fig.add_trace(go.Scatter(x=accel_df['cts'], y=accel_df['Accelerometer (y) [m/s²]'], name='Accel Y'))
# fig.add_trace(go.Scatter(x=accel_df['cts'], y=accel_df['Accelerometer (z) [m/s²]'], name='Accel Z'))

# # Fancy layout
# fig.update_layout(title='Gyro + Accelerometer Telemetry',
#                   xaxis_title='Timestamp (cts)',
#                   yaxis_title='Sensor value',
#                   legend_title='Sensor',
#                   template='plotly_dark')

# fig.show()


# exit()


# Find closest timestamp
import bisect


# Main
gyro_data = load_gyro_csv(GYRO_CSV)
accel_data = load_accel_csv(ACCEL_CSV)

gyro_times = sorted(gyro_data.keys())
accel_times = sorted(accel_data.keys())
# import numpy as np
# import cv2

# # Prepare numpy arrays of times and data
# gyro_times_np = np.array(sorted(gyro_data.keys()))
# accel_times_np = np.array(sorted(accel_data.keys()))

# gyro_vals_x = np.array([gyro_data[t]['gyro_x'] for t in gyro_times_np])
# gyro_vals_y = np.array([gyro_data[t]['gyro_y'] for t in gyro_times_np])
# gyro_vals_z = np.array([gyro_data[t]['gyro_z'] for t in gyro_times_np])

# accel_vals_x = np.array([accel_data[t]['accel_x'] for t in accel_times_np])
# accel_vals_y = np.array([accel_data[t]['accel_y'] for t in accel_times_np])
# accel_vals_z = np.array([accel_data[t]['accel_z'] for t in accel_times_np])

# def interp_1d(times, values, t):
#     if t <= times[0]:
#         return values[0]
#     if t >= times[-1]:
#         return values[-1]
#     idx = np.searchsorted(times, t)
#     t0, t1 = times[idx-1], times[idx]
#     v0, v1 = values[idx-1], values[idx]
#     return v0 + (v1 - v0) * (t - t0) / (t1 - t0)

# # Video setup
# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(OUTPUT_PATH, fourcc, FPS, (WIDTH, HEIGHT))

# frame_count = int(DURATION_SECONDS * FPS)

# for frame_idx in range(frame_count):
#     t = frame_idx / FPS

#     # Interpolate gyro and accel data
#     gx = interp_1d(gyro_times_np, gyro_vals_x, t)
#     gy = interp_1d(gyro_times_np, gyro_vals_y, t)
#     gz = interp_1d(gyro_times_np, gyro_vals_z, t)

#     ax = interp_1d(accel_times_np, accel_vals_x, t)
#     ay = interp_1d(accel_times_np, accel_vals_y, t)
#     az = interp_1d(accel_times_np, accel_vals_z, t)

#     # Compute g-force
#     g_force = (ax**2 + ay**2 + az**2)**0.5 / 9.80665

#     # Create black frame
#     frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

#     # Draw G-force and Gyro data
#     cv2.putText(frame, f"G-Force: {g_force:.8f} g", (50, 100),
#                 cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

#     cv2.putText(frame, f"Gyro Yaw (Z): {gz:.8f} rad/s", (50, 200),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
#     cv2.putText(frame, f"Gyro Roll (X): {gx:.8f} rad/s", (50, 300),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
#     cv2.putText(frame, f"Gyro Pitch (Y): {gy:.8f} rad/s", (50, 400),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

#     # Frame info
#     cv2.putText(frame, f"Frame: {frame_idx} Time: {t:.2f}s", (50, 600),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#     out.write(frame)

# out.release()
# print(f"Overlay video saved to {OUTPUT_PATH}")




import numpy as np
import cv2

# Prepare sorted times and data arrays
gyro_times_np = np.array(sorted(gyro_data.keys()))
accel_times_np = np.array(sorted(accel_data.keys()))

gyro_vals_x = np.array([gyro_data[t]['gyro_x'] for t in gyro_times_np])
gyro_vals_y = np.array([gyro_data[t]['gyro_y'] for t in gyro_times_np])
gyro_vals_z = np.array([gyro_data[t]['gyro_z'] for t in gyro_times_np])

accel_vals_x = np.array([accel_data[t]['accel_x'] for t in accel_times_np])
accel_vals_y = np.array([accel_data[t]['accel_y'] for t in accel_times_np])
accel_vals_z = np.array([accel_data[t]['accel_z'] for t in accel_times_np])

# Frame times
frame_count = int(DURATION_SECONDS * FPS)
frame_times = np.arange(frame_count) / FPS  # shape (frame_count,)

def interp_vectorized(times, values, query_times):
    # Clamp query_times to times range
    query_times = np.clip(query_times, times[0], times[-1])

    # Find insertion positions
    idxs = np.searchsorted(times, query_times, side='right')

    idxs_left = idxs - 1
    idxs_right = idxs

    t_left = times[idxs_left]
    t_right = times[idxs_right]
    v_left = values[idxs_left]
    v_right = values[idxs_right]

    # Avoid division by zero (if two times are equal)
    denom = (t_right - t_left)
    denom[denom == 0] = 1  # avoids div by zero; if equal times, value is just v_left

    weights_right = (query_times - t_left) / denom
    weights_left = 1 - weights_right

    return v_left * weights_left + v_right * weights_right

# Interpolate all frames at once
gx_all = interp_vectorized(gyro_times_np, gyro_vals_x, frame_times)
gy_all = interp_vectorized(gyro_times_np, gyro_vals_y, frame_times)
gz_all = interp_vectorized(gyro_times_np, gyro_vals_z, frame_times)

ax_all = interp_vectorized(accel_times_np, accel_vals_x, frame_times)
ay_all = interp_vectorized(accel_times_np, accel_vals_y, frame_times)
az_all = interp_vectorized(accel_times_np, accel_vals_z, frame_times)

# Video setup
fourcc = cv2.VideoWriter_fourcc(*'mp4v')
out = cv2.VideoWriter(OUTPUT_PATH, fourcc, FPS, (WIDTH, HEIGHT))
for frame_idx in tqdm(range(frame_count), desc=f"Rendering"):
# for frame_idx in range(frame_count):
    t = frame_times[frame_idx]

    gx = gx_all[frame_idx]
    gy = gy_all[frame_idx]
    gz = gz_all[frame_idx]

    ax = ax_all[frame_idx]
    ay = ay_all[frame_idx]
    az = az_all[frame_idx]

    g_force = np.sqrt(ax**2 + ay**2 + az**2) / 9.80665

    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    cv2.putText(frame, f"G-Force: {g_force:.8f} g", (50, 100),
                cv2.FONT_HERSHEY_SIMPLEX, 2, (0, 255, 0), 3)

    cv2.putText(frame, f"Accel X: {ax:.8f} m/s²", (50, 180),
            cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
    cv2.putText(frame, f"Accel Y: {ay:.8f} m/s²", (50, 250),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)
    cv2.putText(frame, f"Accel Z: {az:.8f} m/s²", (50, 320),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (0, 255, 255), 2)

    
    cv2.putText(frame, f"Gyro Yaw (Z): {gz:.8f} rad/s", (50, 200),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    cv2.putText(frame, f"Gyro Roll (X): {gx:.8f} rad/s", (50, 300),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)
    cv2.putText(frame, f"Gyro Pitch (Y): {gy:.8f} rad/s", (50, 400),
                cv2.FONT_HERSHEY_SIMPLEX, 1.5, (255, 0, 0), 2)

    cv2.putText(frame, f"Frame: {frame_idx} Time: {t:.2f}s", (50, 600),
                cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

    out.write(frame)

out.release()
print(f"Overlay video saved to {OUTPUT_PATH}")

































# def closest_telemetry(t, times):
#     return min(times, key=lambda x: abs(x - t))

# # Draw G-Force gauge
# def draw_gforce_gauge(frame, center, radius, g_force):
#     max_g = 3.0  # define max G you expect
#     angle = min(g_force / max_g, 1.0) * 360  # clamp

#     cv2.circle(frame, center, radius, (100, 100, 100), 3)

#     # Draw arc (approximate with line for simplicity)
#     end_angle_rad = math.radians(angle - 90)
#     x = int(center[0] + radius * math.cos(end_angle_rad))
#     y = int(center[1] + radius * math.sin(end_angle_rad))
#     cv2.line(frame, center, (x, y), (0, 255, 0), 6)

#     # Display text
#     cv2.putText(frame, f"G: {g_force:.8f}g", (center[0] - 40, center[1] + radius + 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# # Draw Yaw dial
# def draw_yaw_dial(frame, center, radius, yaw_rate):
#     cv2.circle(frame, center, radius, (100, 100, 100), 3)

#     # Map yaw rate rad/s → angle visualization
#     yaw_angle_deg = yaw_rate * 20  # tuning factor (you can adjust)
#     yaw_angle_deg = max(min(yaw_angle_deg, 180), -180)

#     angle_rad = math.radians(yaw_angle_deg - 90)
#     x = int(center[0] + radius * math.cos(angle_rad))
#     y = int(center[1] + radius * math.sin(angle_rad))
#     cv2.line(frame, center, (x, y), (0, 0, 255), 6)

#     cv2.putText(frame, f"Yaw: {yaw_rate:.8f} rad/s", (center[0] - 80, center[1] + radius + 40),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

# # Draw horizontal bar
# def draw_bar(frame, pos, length, value, label, color):
#     # Map value to [-1,1] scaled bar
#     max_val = 5  # tuning factor
#     bar_length = int((value / max_val) * length)
#     x, y = pos

#     cv2.rectangle(frame, (x, y - 10), (x + length, y + 10), (50, 50, 50), -1)
#     if bar_length >= 0:
#         cv2.rectangle(frame, (x, y - 10), (x + bar_length, y + 10), color, -1)
#     else:
#         cv2.rectangle(frame, (x + bar_length, y - 10), (x, y + 10), color, -1)

#     cv2.putText(frame, f"{label}: {value:.8f}", (x, y - 20),
#                 cv2.FONT_HERSHEY_SIMPLEX, 0.8, (255, 255, 255), 2)

# # MAIN
# gyro_data = load_gyro_csv(GYRO_CSV)
# accel_data = load_accel_csv(ACCEL_CSV)

# gyro_times = sorted(gyro_data.keys())
# accel_times = sorted(accel_data.keys())

# fourcc = cv2.VideoWriter_fourcc(*'mp4v')
# out = cv2.VideoWriter(OUTPUT_PATH, fourcc, FPS, (WIDTH, HEIGHT))

# frame_count = int(DURATION_SECONDS * FPS)
# for frame_idx in tqdm(range(frame_count), desc=f"Rendering Telem"):
# # for frame_idx in range(frame_count):
#     t = 240+frame_idx / FPS

#     cts_gyro = closest_telemetry(t, gyro_times)
#     cts_accel = closest_telemetry(t, accel_times)

#     gyro = gyro_data[cts_gyro]
#     accel = accel_data[cts_accel]

#     ax = accel['accel_x']
#     ay = accel['accel_y']
#     az = accel['accel_z']
#     g_force = (ax**2 + ay**2 + az**2)**0.5 / 9.80665

#     frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

#     # Draw G-Force gauge

#     draw_gforce_gauge(frame, (300, 300), 100, g_force)

#     # Draw Yaw dial
#     draw_yaw_dial(frame, (WIDTH - 300, 300), 100, gyro['gyro_z'])

#     # Draw Roll & Pitch bars
#     draw_bar(frame, (100, HEIGHT - 200), 400, gyro['gyro_x'], 'Roll (X)', (0, 255, 255))
#     draw_bar(frame, (100, HEIGHT - 100), 400, gyro['gyro_y'], 'Pitch (Y)', (255, 0, 255))

#     # Debug info
#     cv2.putText(frame, f"Frame: {frame_idx} Time: {t:.2f}s", (50, 50),
#                 cv2.FONT_HERSHEY_SIMPLEX, 1, (255, 255, 255), 2)

#     out.write(frame)

# out.release()
# print(f"Fancy overlay video saved to {OUTPUT_PATH}")