# import cv2
# import pandas as pd
# import xml.etree.ElementTree as ET

# # 1️⃣ Load GPX acceleration data
# def parse_gpx_accel(gpx_file):
#     ns = {'gpxacc': 'http://www.garmin.com/xmlschemas/AccelerationExtension/v1'}
#     tree = ET.parse(gpx_file)
#     root = tree.getroot()

#     times = []
#     x_vals = []
#     y_vals = []
#     z_vals = []

#     for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
#         time_elem = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
#         acc_elem = trkpt.find('.//gpxacc:accel', ns)
#         if time_elem is not None and acc_elem is not None:
#             time_text = time_elem.text
#             x = float(acc_elem.attrib['x'])
#             y = float(acc_elem.attrib['y'])
#             z = float(acc_elem.attrib['z'])
            
#             # GPX time format → seconds since start
#             pd_time = pd.to_datetime(time_text)
#             times.append(pd_time)
#             x_vals.append(x)
#             y_vals.append(y)
#             z_vals.append(z)

#     df = pd.DataFrame({
#         'time': pd.to_datetime(times),
#         'x': x_vals,
#         'y': y_vals,
#         'z': z_vals
#     })

#     # Normalize time to seconds since start
#     df['time_sec'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()

#     return df

# # 2️⃣ Map G to screen
# def map_to_screen(x_g, y_g, center_x, center_y, scale=200):
#     screen_x = int(center_x + x_g * scale)
#     screen_y = int(center_y - y_g * scale)  # Invert y axis for visual logic
#     return screen_x, screen_y

# # 3️⃣ Main function
# def overlay_g_force(mp4_file, gpx_file, output_file):
#     # Load GPX data
#     df = parse_gpx_accel(gpx_file)

#     # Load video
#     cap = cv2.VideoCapture(mp4_file)
#     fps = cap.get(cv2.CAP_PROP_FPS)
#     frame_width = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
#     frame_height = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
#     frame_count = int(cap.get(cv2.CAP_PROP_FRAME_COUNT))

#     print(f"Video FPS: {fps}, Frames: {frame_count}")

#     # Video writer
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

#     for i in range(frame_count):
#         ret, frame = cap.read()
#         if not ret:
#             break

#         current_time_sec = i / fps

#         # Find closest GPX time
#         closest_idx = (df['time_sec'] - current_time_sec).abs().idxmin()
#         x_g = df.loc[closest_idx, 'x']
#         y_g = df.loc[closest_idx, 'y']
#         z_g = df.loc[closest_idx, 'z']

#         # Draw background circle
#         center_x, center_y = frame_width // 2, frame_height // 2
#         radius = 200
#         cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), 2)

#         # Map dot position
#         dot_x, dot_y = map_to_screen(x_g, y_g, center_x, center_y)
#         cv2.circle(frame, (dot_x, dot_y), 15, (0, 255, 0), -1)

#         # Draw 8 decimal text
#         text = f"X: {x_g:.8f} Y: {y_g:.8f} Z: {z_g:.8f}"
#         cv2.putText(frame, text, (50, 50), cv2.FONT_HERSHEY_SIMPLEX, 1.0, (0, 255, 0), 2)

#         # Write frame
#         out.write(frame)

#         # Optional progress
#         if i % 100 == 0:
#             print(f"Frame {i}/{frame_count}")

#     cap.release()
#     out.release()
#     print(f"Saved to {output_file}")

# # 4️⃣ Run it
# if __name__ == "__main__":
#     mp4_file = 'input.mp4'          # YOUR video file
#     gpx_file = 'GH022604_1_ACCL (3).gpx'          # YOUR GPX file
#     output_file = 'output_overlay.mp4'

#     overlay_g_force(mp4_file, gpx_file, output_file)


import cv2
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np


"""
https://goprotelemetryextractor.com/free/#
- for generating the GPX file
"""

# 1️⃣ Parse GPX acceleration data with timestamps
def parse_gpx_accel(gpx_file):
    ns = {'gpxacc': 'http://www.garmin.com/xmlschemas/AccelerationExtension/v1'}
    tree = ET.parse(gpx_file)
    root = tree.getroot()

    times = []
    x_vals = []
    y_vals = []
    z_vals = []
    print("Make DF")
    for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
        time_elem = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
        acc_elem = trkpt.find('.//gpxacc:accel', ns)
        if time_elem is not None and acc_elem is not None:
            time_text = time_elem.text
            x = float(acc_elem.attrib['x'])
            y = float(acc_elem.attrib['y'])
            z = float(acc_elem.attrib['z'])
            pd_time = pd.to_datetime(time_text)
            times.append(pd_time)
            x_vals.append(x)
            y_vals.append(y)
            z_vals.append(z)

    df = pd.DataFrame({
        'time': pd.to_datetime(times),
        'x': x_vals,
        'y': y_vals,
        'z': z_vals
    })
    df['time_sec'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()

    return df

# 2️⃣ EMA smoothing
def ema(data, alpha=0.1):
    smoothed = [data[0]]
    for val in data[1:]:
        smoothed.append(alpha * val + (1 - alpha) * smoothed[-1])
    return smoothed

# 2️⃣ Map G-force to screen coords
def map_to_screen(x_g, y_g, center_x, center_y, scale=200):
    screen_x = int(center_x + x_g * scale)
    screen_y = int(center_y - y_g * scale)  # invert y axis
    return screen_x, screen_y

def draw_vertical_bar(frame, pos_x, center_y, height, val, max_val=2.0, color=(0, 0, 255)):
    # val normalized -max_val to +max_val → bar length
    half_height = height // 2
    bar_len = int((val / max_val) * half_height)
    cv2.line(frame, (pos_x, center_y - half_height), (pos_x, center_y + half_height), (50,50,50), 5)
    if bar_len > 0:
        cv2.line(frame, (pos_x, center_y), (pos_x, center_y - bar_len), color, 10)
    else:
        cv2.line(frame, (pos_x, center_y), (pos_x, center_y - bar_len), (0,255,255), 10)  # Different color for negative

def draw_horizontal_bar(frame, center_x, pos_y, width, val, max_val=2.0, color=(0, 0, 255)):
    half_width = width // 2
    bar_len = int((val / max_val) * half_width)
    cv2.line(frame, (center_x - half_width, pos_y), (center_x + half_width, pos_y), (50,50,50), 5)
    if bar_len > 0:
        cv2.line(frame, (center_x, pos_y), (center_x + bar_len, pos_y), color, 10)
    else:
        cv2.line(frame, (center_x, pos_y), (center_x + bar_len, pos_y), (0,255,255), 10)

def generate_overlay_video(gpx_file, output_file, fps=59.94, duration=None):
    df = parse_gpx_accel(gpx_file)
    total_duration = duration if duration else df['time_sec'].iloc[-1]
    total_frames = int(total_duration * fps)

    frame_width, frame_height = 640, 480
    center_x, center_y = frame_width // 2, frame_height // 2
    radius = 200

    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

    time_points = np.linspace(0, total_duration, total_frames)
    x_interp = np.interp(time_points, df['time_sec'], df['x'])
    y_interp = np.interp(time_points, df['time_sec'], df['y'])
    z_interp = np.interp(time_points, df['time_sec'], df['z'])

    for i in range(total_frames):
        frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

        # Circle
        cv2.circle(frame, (center_x, center_y), radius, (255,255,255), 2)

        # Dot inside circle
        dot_x, dot_y = map_to_screen(x_interp[i], y_interp[i], center_x, center_y)
        cv2.circle(frame, (dot_x, dot_y), 15, (0,255,0), -1)

        # Left vertical bar (brake/accel = y)
        bar_x = center_x - radius - 50
        draw_vertical_bar(frame, bar_x, center_y, radius*2, y_interp[i], max_val=2.0, color=(0,0,255))

        # Bottom horizontal bar (left/right = x)
        bar_y = center_y + radius + 20
        draw_horizontal_bar(frame, center_x, bar_y, radius*2, x_interp[i], max_val=2.0, color=(255,0,0))

        # Text overlay with 8 decimals
        text = f"X: {x_interp[i]:.8f}  Y: {y_interp[i]:.8f}  Z: {z_interp[i]:.8f}"
        cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

        out.write(frame)
        if i % 1000 == 0:
            print(f"Frame {i}/{total_frames}")

    out.release()
    print(f"Saved overlay video: {output_file}")

"""
Working Raw
"""
# # 3️⃣ Generate overlay video from GPX accel only
# def generate_overlay_video(gpx_file, output_file, fps=59.94, duration=None):
#     df = parse_gpx_accel(gpx_file)

#     # Determine total duration in seconds
#     total_duration = duration if duration is not None else df['time_sec'].iloc[-1]
#     total_frames = int(total_duration * fps)

#     # Video settings
#     frame_width, frame_height = 640, 480
#     center_x, center_y = frame_width // 2, frame_height // 2
#     radius = 200

#     # VideoWriter setup
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

#     # Interpolate x,y,z for each frame time
#     time_points = np.linspace(0, total_duration, total_frames)
#     x_interp = np.interp(time_points, df['time_sec'], df['x'])
#     y_interp = np.interp(time_points, df['time_sec'], df['y'])
#     z_interp = np.interp(time_points, df['time_sec'], df['z'])
#     print("Gen Frame")
#     for i in range(total_frames):
#         frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)  # black background

#         # Draw circle background
#         cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), 2)

#         # Dot position based on interpolated G
#         dot_x, dot_y = map_to_screen(x_interp[i], y_interp[i], center_x, center_y)
#         cv2.circle(frame, (dot_x, dot_y), 15, (0, 255, 0), -1)

#         # Text with 8 decimals
#         text = f"X: {x_interp[i]:.8f} Y: {y_interp[i]:.8f} Z: {z_interp[i]:.8f}"
#         cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 255, 0), 2)

#         out.write(frame)

#         if i % 500 == 0:
#             print(f"Frame {i}/{total_frames}")

#     out.release()
#     print(f"Overlay video saved as {output_file}")





"""
No working smoothing
"""
# # 4️⃣ Generate overlay video with smoothed data (no base video)
# def generate_overlay_video(df, output_file, fps=30, duration_sec=None, alpha=0.1):
#     if duration_sec is None:
#         duration_sec = df['time_sec'].iloc[-1]

#     width, height = 640, 480
#     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#     out = cv2.VideoWriter(output_file, fourcc, fps, (width, height))

#     # Apply EMA smoothing
#     df['x_smooth'] = ema(df['x'], alpha)
#     df['y_smooth'] = ema(df['y'], alpha)
#     df['z_smooth'] = ema(df['z'], alpha)

#     total_frames = int(duration_sec * fps)

#     for i in range(total_frames):
#         current_time = i / fps

#         # Find closest GPX time
#         closest_idx = (df['time_sec'] - current_time).abs().idxmin()
#         x_g = df.loc[closest_idx, 'x_smooth']
#         y_g = df.loc[closest_idx, 'y_smooth']
#         z_g = df.loc[closest_idx, 'z_smooth']

#         # Create black frame
#         frame = 0 * np.ones((height, width, 3), dtype=np.uint8)

#         # Draw circle
#         center_x, center_y = width // 2, height // 2
#         radius = 200
#         cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), 2)

#         # Draw dot representing lateral/forward acceleration
#         dot_x, dot_y = map_to_screen(x_g, y_g, center_x, center_y)
#         cv2.circle(frame, (dot_x, dot_y), 15, (0, 255, 0), -1)

#         # Draw decimal precision text
#         text = f"X: {x_g:.8f}  Y: {y_g:.8f}  Z: {z_g:.8f}"
#         cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0,255,0), 2)

#         out.write(frame)

#         if i % 100 == 0:
#             print(f"Frame {i}/{total_frames}")

#     out.release()
#     print(f"Overlay video saved to {output_file}")

if __name__ == "__main__":
    gpx_file = 'GH022604_1_ACCL (3).gpx'        # Your GPX file here
    output_file = 'overlay_telem_full.mp4'  # Output overlay video
    generate_overlay_video(gpx_file, output_file)
