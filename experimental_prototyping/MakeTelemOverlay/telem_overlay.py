import cv2
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np


"""
https://goprotelemetryextractor.com/free/#
- Free Box
- Accelerometer
- Virb Edit
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
    print(f"Generating overlay for {gpx_file} → {output_file}")
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




import sys
from PyQt6.QtWidgets import (
    QApplication, QWidget, QPushButton, QVBoxLayout, QFileDialog, QLabel, QListWidget, QMessageBox
)
from PyQt6.QtCore import QThread, pyqtSignal

class WorkerThread(QThread):
    finished = pyqtSignal(str)

    def __init__(self, gpx_file):
        super().__init__()
        self.gpx_file = gpx_file
        self.output_file = gpx_file.replace(".gpx", "_telem_overlay.mp4")

    def run(self):
        generate_overlay_video(self.gpx_file, self.output_file)
        self.finished.emit(self.output_file)

class OverlayApp(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Multi-GPX Overlay Generator")

        self.label = QLabel("Queued files:")
        self.file_list = QListWidget()
        self.button_add = QPushButton("Add GPX File")
        self.button_generate = QPushButton("Generate All Overlays")

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        layout.addWidget(self.file_list)
        layout.addWidget(self.button_add)
        layout.addWidget(self.button_generate)
        self.setLayout(layout)

        self.button_add.clicked.connect(self.add_file)
        self.button_generate.clicked.connect(self.generate_all)

        self.threads = []

    def add_file(self):
        files, _ = QFileDialog.getOpenFileNames(self, "Select GPX Files", "", "GPX Files (*.gpx)")
        for file in files:
            if file and file not in [self.file_list.item(i).text() for i in range(self.file_list.count())]:
                self.file_list.addItem(file)

    def generate_all(self):
        if self.file_list.count() == 0:
            QMessageBox.warning(self, "No Files", "Add some GPX files first.")
            return

        for i in range(self.file_list.count()):
            gpx_file = self.file_list.item(i).text()
            thread = WorkerThread(gpx_file)
            thread.finished.connect(self.on_finished)
            thread.start()
            self.threads.append(thread)

        self.button_generate.setEnabled(False)

    def on_finished(self, output):
        QMessageBox.information(self, "Overlay Done", f"Generated: {output}")
        if all(not t.isRunning() for t in self.threads):
            self.button_generate.setEnabled(True)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = OverlayApp()
    window.show()
    sys.exit(app.exec())
