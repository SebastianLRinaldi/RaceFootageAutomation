from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


import cv2
import pandas as pd
import xml.etree.ElementTree as ET
import numpy as np
import traceback
import os
import shutil
import cv2
import pandas as pd
import numpy as np
import xml.etree.ElementTree as ET
import traceback
import os
from multiprocessing import Process, Queue
from lxml import etree

from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *



# class WorkerThread(QThread):
#     finished = pyqtSignal(str)

#     def __init__(self, gpx_file, logic: 'Logic'):
#         super().__init__()
#         self.logic = logic  # store the Logic instance


#     def run(self):
#         self.logic.generate_overlay_video()
#         self.finished.emit(self.output_file)

class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic', gpx_file):
        super().__init__()
        self.logic = logic  # store the Logic instance
        self.gpx_file = gpx_file

    def run(self):
        try:
            self.logic.generate_overlay_video(self.gpx_file)  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)


"""
https://goprotelemetryextractor.com/free/#
- Free Box
- Accelerometer
- Virb Edit
- for generating the GPX file
"""
class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()

        self.width = 640
        self.height = 480
        self.fps = 59.94

        self.radius = 200
        self.scale = 200
        self.max_val = 2.0

        self.rendered_name = f"Telemetry_Overlay.mp4"
        self.asset_name = f"Telemetry_Overlay_Section.mp4"

        self.processes = []
        self.progress_queue = None
        self.progress_timer = None
        

        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, int, self.width),
            ("height", self.ui.height_input, int, self.height),
            ("fps", self.ui.fps_input, float, self.fps),

            ("rendered_name", self.ui.rendered_file_name, str, self.rendered_name),
            
            ("radius", self.ui.radius_input, int, self.radius),
            ("scale", self.ui.scale_input, int, self.scale),

            ("max_val", self.ui.max_val_input, float, self.max_val),
        ]

        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, app="make_telem_overlay")

        self.threads = []
    # 1️⃣ Parse GPX acceleration data with timestamps
    def parse_gpx_accel(self, gpx_file):
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
                times.append(time_elem.text)  # raw strings only here
                x_vals.append(float(acc_elem.attrib['x']))
                y_vals.append(float(acc_elem.attrib['y']))
                z_vals.append(float(acc_elem.attrib['z']))
        print("DONE-Make DF")

        # Convert all timestamps at once here
        times_dt = pd.to_datetime(times)

        df = pd.DataFrame({
            'time': times_dt,
            'x': x_vals,
            'y': y_vals,
            'z': z_vals
        })
        df['time_sec'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()

        return df





    # def parse_gpx_accel_streaming(gpx_file):
    #     ns_gpx = 'http://www.topografix.com/GPX/1/1'
    #     ns_acc = 'http://www.garmin.com/xmlschemas/AccelerationExtension/v1'

    #     times, x_vals, y_vals, z_vals = [], [], [], []

    #     # Setup iterparse to only pull trkpt elements, avoid full tree load
    #     context = etree.iterparse(gpx_file, events=('end',), tag=f'{{{ns_gpx}}}trkpt')

    #     for event, elem in context:
    #         time_elem = elem.find(f'{{{ns_gpx}}}time')
    #         acc_elem = elem.find(f'.//{{{ns_acc}}}accel')

    #         if time_elem is not None and acc_elem is not None:
    #             times.append(time_elem.text)
    #             x_vals.append(float(acc_elem.get('x')))
    #             y_vals.append(float(acc_elem.get('y')))
    #             z_vals.append(float(acc_elem.get('z')))

    #         # Free memory for processed element
    #         elem.clear()
    #         while elem.getprevious() is not None:
    #             del elem.getparent()[0]

    #     times = pd.to_datetime(times)
    #     df = pd.DataFrame({'time': times, 'x': x_vals, 'y': y_vals, 'z': z_vals})
    #     df['time_sec'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()
    #     return df


    # 2️⃣ EMA smoothing
    def ema(self, data, alpha=0.1):
        smoothed = [data[0]]
        for val in data[1:]:
            smoothed.append(alpha * val + (1 - alpha) * smoothed[-1])
        return smoothed

    # 2️⃣ Map G-force to screen coords
    def map_to_screen(self, x_g, y_g, center_x, center_y, scale=200):
        screen_x = int(center_x + x_g * scale)
        screen_y = int(center_y - y_g * scale)  # invert y axis
        return screen_x, screen_y

    def draw_vertical_bar(self, frame, pos_x, center_y, height, val, max_val=2.0, color=(0, 0, 255)):
        # val normalized -max_val to +max_val → bar length
        half_height = height // 2
        bar_len = int((val / max_val) * half_height)
        cv2.line(frame, (pos_x, center_y - half_height), (pos_x, center_y + half_height), (50,50,50), 5)
        if bar_len > 0:
            cv2.line(frame, (pos_x, center_y), (pos_x, center_y - bar_len), color, 10)
        else:
            cv2.line(frame, (pos_x, center_y), (pos_x, center_y - bar_len), (0,255,255), 10)  # Different color for negative

    def draw_horizontal_bar(self, frame, center_x, pos_y, width, val, max_val=2.0, color=(0, 0, 255)):
        half_width = width // 2
        bar_len = int((val / max_val) * half_width)
        cv2.line(frame, (center_x - half_width, pos_y), (center_x + half_width, pos_y), (50,50,50), 5)
        if bar_len > 0:
            cv2.line(frame, (center_x, pos_y), (center_x + bar_len, pos_y), color, 10)
        else:
            cv2.line(frame, (center_x, pos_y), (center_x + bar_len, pos_y), (0,255,255), 10)

    def generate_overlay_video(self, gpx_file):
        
        output_file = gpx_file.replace(".gpx", self.asset_name)
        print(f"Generating overlay for {gpx_file} → {output_file}")

        
        df = self.parse_gpx_accel(gpx_file)
        total_duration = df['time_sec'].iloc[-1]
        total_frames = int(total_duration * self.fps)

        frame_width, frame_height = 640, 480
        center_x, center_y = frame_width // 2, frame_height // 2
        radius = 200

        print("MAKING VIDEO OUT")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        out = cv2.VideoWriter(output_file, fourcc, self.fps, (frame_width, frame_height))
        print("DONE-MAKING VIDEO OUT")
        
        print("Points interped")
        time_points = np.linspace(0, total_duration, total_frames)
        x_interp = np.interp(time_points, df['time_sec'], df['x'])
        y_interp = np.interp(time_points, df['time_sec'], df['y'])
        z_interp = np.interp(time_points, df['time_sec'], df['z'])
        print("DONE-Points interped")
        for i in range(total_frames):
            frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)

            # Circle
            cv2.circle(frame, (center_x, center_y), radius, (255,255,255), 2)

            # Dot inside circle
            dot_x, dot_y = self.map_to_screen(x_interp[i], y_interp[i], center_x, center_y)
            cv2.circle(frame, (dot_x, dot_y), 15, (0,255,0), -1)

            # Left vertical bar (brake/accel = y)
            bar_x = center_x - radius - 50
            self.draw_vertical_bar(frame, bar_x, center_y, radius*2, y_interp[i], max_val=2.0, color=(0,0,255))

            # Bottom horizontal bar (left/right = x)
            bar_y = center_y + radius + 20
            self.draw_horizontal_bar(frame, center_x, bar_y, radius*2, x_interp[i], max_val=2.0, color=(255,0,0))

            # Text overlay with 8 decimals
            text = f"X: {x_interp[i]:.8f}  Y: {y_interp[i]:.8f}  Z: {z_interp[i]:.8f}"
            cv2.putText(frame, text, (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0,255,0), 2)

            out.write(frame)
            if i % 1000 == 0:
                print(f"Frame {i}/{total_frames}")

        out.release()
        print(f"Saved overlay video: {output_file}")




    # def add_file(self):
    #     files, _ = QFileDialog.getOpenFileNames(self.ui, "Select GPX Files", "", "GPX Files (*.gpx)")
    #     for file in files:
    #         if file and file not in [self.ui.file_list.item(i).text() for i in range(self.ui.file_list.count())]:
    #             self.ui.file_list.addItem(file)

    def add_file(self):
        files, _ = QFileDialog.getOpenFileNames(self.ui, "Select GPX Files - Will Move to Assets Folder", "", "GPX Files (*.gpx)")
        target_dir = self.project_directory.asset_path

        for file in files:
            # move file to target directory
            dest_path = os.path.join(target_dir, os.path.basename(file))
            shutil.move(file, dest_path)
                

    def generate_all(self):
        # check if any GPX files exist in asset dir
        gpx_files = [f for f in os.listdir(self.project_directory.asset_path) if f.lower().endswith(".gpx")]
        if not gpx_files:
            QMessageBox.warning(self.ui, "No .gpx Files", "Add some GPX files first to Telemetry Assets Folder.")
            return

        for gpx_file in gpx_files:
            full_path = os.path.join(self.project_directory.asset_path, gpx_file)
            thread = OverlayWorker(self, full_path)
            thread.finished.connect(self.on_finished)
            thread.start()
            self.threads.append(thread)

        self.ui.generate_button.setEnabled(False)

    def on_finished(self):
        QMessageBox.information(self.ui, "Overlay Done", f"Generated: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")

        if all(not t.isRunning() for t in self.threads):
            self.ui.generate_button.setEnabled(True)


    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.generate_button.setEnabled(True)

#     def generate_all(self):
#         gpx_files = [
#             f for f in os.listdir(self.project_directory.asset_path)
#             if f.lower().endswith(".gpx")
#         ]
#         if not gpx_files:
#             QMessageBox.warning(self.ui, "No .gpx Files",
#                 "Add some GPX files first to Telemetry Assets Folder.")
#             return

#         self.processes = []
#         self.progress_queue = Queue()

#         for gpx_file in gpx_files:
#             full_path = os.path.join(self.project_directory.asset_path, gpx_file)
#             p = Process(
#                 target=generate_overlay_video_process,
#                 args=(full_path, self.asset_name, self.fps, self.progress_queue)
#             )
#             p.start()
#             self.processes.append(p)

#         self.progress_timer = QTimer()
#         self.progress_timer.timeout.connect(self.check_progress)
#         self.progress_timer.start(200)

#         self.ui.status_label.setText("Generating overlays...")
#         self.ui.generate_button.setEnabled(False)

#     def check_progress(self):
#         while not self.progress_queue.empty():
#             event, gpx_file, data = self.progress_queue.get()

#             if event == "progress":
#                 percent = int(data * 100)
#                 self.ui.status_label.setText(
#                     f"{os.path.basename(gpx_file)}: {percent}%"
#                 )

#             elif event == "done":
#                 self.ui.status_label.setText(
#                     f"✅ Done: {os.path.basename(gpx_file)}"
#                 )

#             elif event == "error":
#                 self.ui.status_label.setText(
#                     f"❌ Error in {os.path.basename(gpx_file)}"
#                 )
#                 print(data)

#         # stop when all processes done
#         if all(not p.is_alive() for p in self.processes):
#             self.progress_timer.stop()
#             self.ui.generate_button.setEnabled(True)
#             QMessageBox.information(self.ui, "Done",
#                 "All overlay videos generated.")

#     # src/overlay_process.py
# def generate_overlay_video_process(gpx_file, asset_name, fps, progress_queue):
#     try:
#         ns = {'gpxacc': 'http://www.garmin.com/xmlschemas/AccelerationExtension/v1'}
#         tree = ET.parse(gpx_file)
#         root = tree.getroot()

#         times, x_vals, y_vals, z_vals = [], [], [], []
#         for trkpt in root.findall('.//{http://www.topografix.com/GPX/1/1}trkpt'):
#             time_elem = trkpt.find('{http://www.topografix.com/GPX/1/1}time')
#             acc_elem = trkpt.find('.//gpxacc:accel', ns)
#             if time_elem is not None and acc_elem is not None:
#                 times.append(pd.to_datetime(time_elem.text))
#                 x_vals.append(float(acc_elem.attrib['x']))
#                 y_vals.append(float(acc_elem.attrib['y']))
#                 z_vals.append(float(acc_elem.attrib['z']))

#         df = pd.DataFrame({'time': times, 'x': x_vals, 'y': y_vals, 'z': z_vals})
#         df['time_sec'] = (df['time'] - df['time'].iloc[0]).dt.total_seconds()

#         output_file = gpx_file.replace(".gpx", asset_name)
#         frame_width, frame_height = 640, 480
#         center_x, center_y = frame_width // 2, frame_height // 2
#         radius = 200
#         total_duration = 30
#         total_frames = int(total_duration * fps)

#         fourcc = cv2.VideoWriter_fourcc(*'mp4v')
#         out = cv2.VideoWriter(output_file, fourcc, fps, (frame_width, frame_height))

#         time_points = np.linspace(0, total_duration, total_frames)
#         x_interp = np.interp(time_points, df['time_sec'], df['x'])
#         y_interp = np.interp(time_points, df['time_sec'], df['y'])
#         z_interp = np.interp(time_points, df['time_sec'], df['z'])

#         for i in range(total_frames):
#             frame = np.zeros((frame_height, frame_width, 3), dtype=np.uint8)
#             cv2.circle(frame, (center_x, center_y), radius, (255, 255, 255), 2)
#             dot_x = int(center_x + x_interp[i] * 200)
#             dot_y = int(center_y - y_interp[i] * 200)
#             cv2.circle(frame, (dot_x, dot_y), 15, (0, 255, 0), -1)
#             out.write(frame)

#             if i % 200 == 0:
#                 progress_queue.put(("progress", gpx_file, i / total_frames))

#         out.release()
#         progress_queue.put(("done", gpx_file, output_file))

#     except Exception:
#         progress_queue.put(("error", gpx_file, traceback.format_exc()))
