from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *


import os
import subprocess
import tempfile
import cv2
import numpy as np
import math
from math import ceil

from PIL import ImageFont, ImageDraw, Image
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm import tqdm
import traceback


from .layout import Layout
from src.components import *
from src.helper_functions import *
from src.helper_classes import *

"""
    # List of lap time deltas is 0-based
    # If there are 24 laps, valid indexes are 0 to 23
    # lap_number = 1-based external label (e.g., for display)
    # index = lap_number - 1

    # Slicing with [:lap_number] returns first 'lap_number' items (indexes 0 to lap_number-1)
    # So:
    # self.project_directory.lap_time_deltas[:0] => returns [] (no laps) | HEADER DISPLAYED + no laps on table 
    # self.project_directory.lap_time_deltas[:1] => returns first lap only (index 0) | Headers + lap 1 on table 
    # self.project_directory.lap_time_deltas[:23] => returns 23 laps (indexes 0 to 22) | headers +  laps 1-23 on table 
    # self.project_directory.lap_time_deltas[:24] => returns full 24 laps (indexes 0 to 23) | headers +  laps 1-24 on table 
    
    # self.project_directory.lap_time_deltas[0][1] => Duration of lap 1 | [LAP 1 DURATION]
    # self.project_directory.lap_time_deltas[1][1] => Duration of lap 2 | Headers + lap 1 for [lap 2 duration]
    # self.project_directory.lap_time_deltas[23][1] => Duration of lap 24 | Headers + lap 1-23 for [lap 24 duration]
    # self.project_directory.lap_time_deltas[24][1] => IndexError (only 24 laps; valid indexes are 0 to 23) | Headers + lap 1-24 [for custom end duration - no lap time duration]

    ----
    interation 0 = HEADER DISPLAYED + no laps on table [LAP 1 DURATION]
    interation 1 = HEADER DISPLAYED +  lap 1 on table [LAP 2 DURATION]
    interation 23 = HEADER DISPLAYED +  lap 1-23 on table [LAP 24 DURATION]
    interation 24 = HEADER DISPLAYED +  lap 1-24 on table [CUSTOM END DURATION]
    ----
    interation 0 =      lap_time_deltas[:0] | lap_time_deltas[0][1]
    interation 1 =      lap_time_deltas[:1] |  lap_time_deltas[1][1]
    interation 23 =    lap_time_deltas[:23] | lap_time_deltas[23][1]
    interation 24 =    lap_time_deltas[:24] |  [CUSTOM END DURATION]

"""
class OverlayWorker(QThread):
    finished = pyqtSignal()
    error = pyqtSignal(str, str)

    def __init__(self, logic: 'Logic'):
        super().__init__()
        self.logic = logic  # store the Logic instance

    def run(self):
        try:
            self.logic.make_table_overlay()  # call the instance method
            self.finished.emit()
        except Exception as e:
            err_type = type(e).__name__
            tb_str = traceback.format_exc()
            self.error.emit(err_type, tb_str)

class Logic(QObject):
    # lap_started = pyqtSignal(int)
    # lap_progress = pyqtSignal(int, int)  # lap_number, percent
    # lap_finished = pyqtSignal(int)
    
    def __init__(self, ui: Layout):
        super().__init__()
        self.ui = ui
        self.project_directory = ProjectDirectory()
        self.lap_labels = {}
        # self.lap_started.connect(self.create_lap_label)
        # self.lap_progress.connect(self.update_lap_label)
        # self.lap_finished.connect(self.remove_lap_label)

        self.width = 1920
        self.height = 1080
        self.fps = 59.94
        self.use_gpu = True

        self.start_duration = 5
        self.end_duration = 15

        self.rendered_name = f"Table_Overlay.mp4"

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
        self.font_size = 16
        self.font = ImageFont.truetype(self.font_path, self.font_size)

        # self.padding_top = 10
        # self.padding_bottom = 10
        # self.padding_left = 10
        # self.padding_right = 10


        # Dynamic headers and column widths - add more columns here
        self.HEADERS = ["Lap", "Time", "Best Lap Diff"]  
        self.COL_WIDTHS = [100, 143, 334]

        self.ROW_HEIGHT_MIN = 20
        self.ROW_HEIGHT_MAX = 40

        self.PADDING = {
            'top': 10,
            'bottom': 10,
            'left': 10,
            'right': 10
        }

        self.TABLE_Y = 0
        self.TABLE_X = 0
        
        self.FRAME_WIDTH = sum(self.COL_WIDTHS)+1
        self.FRAME_HEIGHT = 1080
        
        self.TOTAL_ROWS = len(self.project_directory.lap_times) + 1
        
        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, self.width),
            ("height", self.ui.height_input, self.height),
            ("fps", self.ui.fps_input, self.fps),
            ("use_gpu", self.ui.use_gpu_checkbox, self.use_gpu),

            # ("padding_top", self.ui.padding_top_input, self.padding_top),
            # ("padding_bottom", self.ui.padding_bottom_input, self.padding_bottom),
            # ("padding_left", self.ui.padding_left_input, self.padding_left),
            # ("padding_right", self.ui.padding_right_input, self.padding_right),

            ("start_duration", self.ui.start_duration_input, self.start_duration),
            ("end_duration", self.ui.end_duration_input, self.end_duration),

            ("rendered_name", self.ui.rendered_file_name, self.rendered_name),
            ("font_path", self.ui.font_path_input.layout.line_edit, self.font_path ),
            ("font_size", self.ui.font_size_input, self.font_size),
        ]

        self.settings_handler = SettingsHandler(SETTINGS_FIELDS, target=self, app="make_table_overlay")
        # print(f"TOTAL_ROWS (type: {type(self.TOTAL_ROWS)}): {self.TOTAL_ROWS}")
        # print(f"TABLE_WIDTH (type: {type(self.TABLE_WIDTH)}): {self.TABLE_WIDTH}")
        # print(f"FRAME_WIDTH (type: {type(self.FRAME_WIDTH)}): {self.FRAME_WIDTH}")
        # print(f"FRAME_HEIGHT (type: {type(self.FRAME_HEIGHT)}): {self.FRAME_HEIGHT}")
        # print(f"TABLE_X (type: {type(self.TABLE_X)}): {self.TABLE_X}")
        # print(f"TABLE_Y (type: {type(self.TABLE_Y)}): {self.TABLE_Y}")

    def on_project_updated(self):
        pass
        # self.TABLE_WIDTH = sum(self.COL_WIDTHS)
        # self.FRAME_WIDTH = self.TABLE_WIDTH + self.PADDING['left'] + self.PADDING['right']
        
        # self.TOTAL_ROWS = len(self.project_directory.lap_times) + 1
        # self.FRAME_HEIGHT = (self.TOTAL_ROWS * self.ROW_HEIGHT_MAX) + self.PADDING['top'] + self.PADDING['bottom']

        # self.TABLE_X = self.PADDING['left']
        # self.TABLE_Y = self.PADDING['top']

    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Table Overlay...")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.progress.setFormat("Rendering... 0%")
        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        self.ui.generate_button.setEnabled(True)
        
        print(f"✅ Table Overlay Video saved as {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        print(f'File "{self.project_directory.make_rendered_file_path(self.rendered_name)}"')
        self.ui.progress.setFormat("Ready")

    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.generate_button.setEnabled(True)
        self.ui.progress.setFormat("Ready")

    def get_ffmpeg_cmd(self, concat_txt):
        base_cmd = [
            "ffmpeg",
            "-y",
            "-f", "concat",
            "-safe", "0",
            "-i", concat_txt,
            "-fps_mode", "cfr",
            "-r", str(self.fps),
            "-pix_fmt", "yuv420p",
            self.project_directory.make_rendered_file_path(self.rendered_name),
        ]

        if self.use_gpu:
            gpu_opts = [
                "-c:v", "h264_nvenc",
                "-preset", "fast",   # NVENC presets
                "-rc", "vbr",
                "-cq", "18"
            ]
            # Insert GPU options before output_file
            return base_cmd[:-1] + gpu_opts + [base_cmd[-1]]
        else:
            cpu_opts = [
                "-c:v", "libx264",
                "-crf", "18",
                "-preset", "slow"
            ]
            # Insert CPU options before output_file
            return base_cmd[:-1] + cpu_opts + [base_cmd[-1]]

    def concat_videos(self, file_list, output_file):
        # Create concat text file for ffmpeg
        concat_txt = os.path.join(os.path.dirname(output_file), "concat_list_table_overlay.txt")
        with open(concat_txt, "w") as f:
            for file in file_list:
                f.write(f"file '{file}'\n")

        # Usage example:
        cmd = self.get_ffmpeg_cmd(concat_txt=concat_txt)

        
        # subprocess.run(cmd, check=True)

        process = subprocess.Popen(cmd, stderr=subprocess.PIPE, text=True)
    
        for line in process.stderr:
            self.ui.status_label.setText(line.strip())  # shows the full line
            QApplication.processEvents()  # make sure QLabel updates immediately

        process.wait()

    def draw_table(self, data_rows:list, draw_alignment=False):
        # Define starting position and padding
        rows = len(data_rows) + 1  # Number of rows based on your data + 1 for headers
        columns = len(self.HEADERS) if rows > 0 else 0  # Number of columns based on headers

        # cell_width = (self.FRAME_WIDTH-1)/columns
        # cell_height = (self.FRAME_HEIGHT-1)/rows
        max_cell_height = 50  # Example max height (adjust as needed)
        cell_height = min((self.FRAME_HEIGHT - 1) / rows, max_cell_height)

        # print(f"cell_width:{cell_width} | cell_height:{cell_height} | rows:{rows} | columns{columns}")


        
        img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)  # Initial image
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        header_font = ImageFont.truetype(self.font_path, cell_height * 1.05)
        row_font = ImageFont.truetype(self.font_path, cell_height * 0.8)


        sorted_rows = sorted(enumerate(self.project_directory.lap_time_deltas), key=lambda x: x[1][1])  # Sort by time in column 1
        best_time_row = sorted_rows[0][0] + 1  # Best time row (add 1 for header offset)
        second_best_row = sorted_rows[1][0] + 1  # Second best time row
        third_best_row = sorted_rows[2][0] + 1  # Third best time row
        worst_time_row = sorted_rows[-1][0] + 1  # Worst time row

        # Draw the grid (rows and columns)
        for row in range(rows):  # We now have an extra row for headers
            for col in range(columns):
                # Calculate top left and bottom right coordinates of each cell
                # top_left = (x + col * cell_width, y + row * cell_height)
                # bottom_right = (x + (col + 1) * cell_width, y + (row + 1) * cell_height)
                # Calculate the starting x position of the current column

                
                x_pos = sum(self.COL_WIDTHS[:col])  # Sum widths of all previous columns
                col_width = self.COL_WIDTHS[col]  # Use specific column width from COL_WIDTH
                # Calculate top left and bottom right coordinates of each cell
                top_left = (x_pos, self.TABLE_Y + row * cell_height)
                bottom_right = (x_pos + col_width, self.TABLE_Y + (row + 1) * cell_height)


                

                # Draw the rectangle for the cell
                draw.rectangle([top_left, bottom_right], outline=(255,255,255), width=1)

                # Add the corresponding data inside the cell (centered)
                if row == 0:
                    text = self.HEADERS[col]  # Use header text for the first row
                    current_font = header_font  # Use header font for the header
                    text_color = (255, 255, 255)
                else:
                    text = str(data_rows[row - 1][col])  # Subtract 1 from row index for data rows
                    current_font = row_font  # Use normal font for data rows

                    if row == best_time_row:
                        text_color = (179, 18, 204)  # Purple for best time row
                    elif row == second_best_row:
                        text_color = (255, 255, 0)  # Yellow for second best
                    elif row == third_best_row:
                        text_color = (255, 165, 0)  # Orange for third best
                    elif row == worst_time_row:
                        text_color = (255, 0, 0)  # Red for worst time row
                    else:
                        text_color = (255, 255, 255)  # White for normal rows


                # Calculate center (x, y) of the cell
                cell_center_x = (top_left[0] + bottom_right[0]) // 2
                cell_center_y = (top_left[1] + bottom_right[1]) // 2


                
                draw_text_centered(draw, current_font, text,  (cell_center_x,cell_center_y), color=text_color)

                if draw_alignment:
                    # Draw vertical center line through the cell
                    draw.line([cell_center_x, top_left[1], cell_center_x, bottom_right[1]], fill='red', width=1)

                    # Draw horizontal center line through the cell
                    draw.line([top_left[0], cell_center_y, bottom_right[0], cell_center_y], fill='red', width=1)
        # pil_img.show()  # This opens the image in the default image viewer
        return pil_img

    def create_table_section(self, lap_number, temp_dir):
        current_laps = self.project_directory.lap_time_deltas[:lap_number]
        
        if lap_number == len(self.project_directory.lap_time_deltas):
            # last lap
            duration = self.end_duration
        else:
            target_duration = self.project_directory.lap_time_deltas[lap_number][1]
            duration = target_duration
        
        # print(f"lap_number: {lap_number} |  firstlap?: {lap_number == 0}   | lastlap?: {lap_number == len(self.project_directory.lap_time_deltas)} | duration: {duration} | current_laps {current_laps}\n")
        frame_count = int(float(duration) * self.fps)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, frameSize=(self.FRAME_WIDTH, self.FRAME_HEIGHT))


        img = self.draw_table(current_laps)

        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


        try:
            # for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
            #     writer.write(frame_bgr)

            # self.lap_started.emit(lap_number)

            for i in range(frame_count):
                writer.write(frame_bgr)
                percent = int(((i + 1) / frame_count) * 100)

                # update QLabel from worker thread safely
                QMetaObject.invokeMethod(
                    self.ui.status_label,
                    "setText",
                    Qt.ConnectionType.QueuedConnection,
                    Q_ARG(str, f"Rendering Table for Lap {lap_number}... {percent}%")
                )
                # self.lap_progress.emit(lap_number, percent)

            # self.lap_finished.emit(lap_number)
        finally:
            writer.release()  # Ensure it's always released
            del writer


        return filename

    def make_table_overlay(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            render_single = False
            
            lap_videos = []
            if render_single:
                lap_video = self.create_table_section( 1, temp_dir)
                lap_videos.append(lap_video)
            else:
                with ThreadPoolExecutor() as executor:
                    futures = {
                                executor.submit(self.create_table_section, i , temp_dir): i
                                for i in range(len(self.project_directory.lap_time_deltas)+1)
                            }

                    # for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                    #     lap_number = futures[future]
                    #     lap_videos.append(future.result())

                    total = len(futures)
                    done = 0
                    for future in as_completed(futures):
                        lap_number = futures[future]
                        lap_videos.append(future.result())
                        done += 1
                        percent = int((done / total) * 100)
                        
                        QMetaObject.invokeMethod(
                            self,  # where `update_render_progress` is defined
                            "update_render_progress",
                            Qt.ConnectionType.QueuedConnection,
                            Q_ARG(int, percent)
                        )

            # Sort videos by lap number (they can complete out of order)
            lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))
            
            # 3. Concatenate all videos: start_blank + lap videos
            self.concat_videos(lap_videos, self.rendered_name)

            # Temp files deleted automatically on context exit






    # # In your main window:
    # def create_lap_label(self, lap_number):
    #     print(f"MAKING LABEL LAP:{lap_number}")
    #     label = QLabel(f"Rendering Table for Lap {lap_number}... 0%")
    #     self.ui.layout().addWidget(label)
    #     self.lap_labels[lap_number] = label

    # # def update_lap_label(self, lap_number, percent):
    # #     print(f"UPDATING LABEL LAP:{lap_number}")
    # #     label = self.lap_labels.get(lap_number)
    # #     if label:
    # #         label.setText(f"Rendering Table for Lap {lap_number}... {percent}%")
    # def update_lap_label(self, lap_number, percent):
    #     label = self.lap_labels.get(lap_number)
    #     if label:
    #         # only update text if percent actually changed
    #         if getattr(label, "_last_percent", -1) != percent:
    #             label.setText(f"Rendering Table for Lap {lap_number}... {percent}%")
    #         label._last_percent = percent

    # def remove_lap_label(self, lap_number):
    #     print(f"REMOVING LABEL LAP:{lap_number}")
    #     label = self.lap_labels.pop(lap_number, None)
    #     if label:
    #         self.ui.layout().removeWidget(label)
    #         label.deleteLater()


    # def create_lap_label(self, lap_number):
    #     progress = QProgressBar()
    #     progress.setRange(0, 100)  # 0% to 100%
    #     progress.setValue(0)
    #     progress.setFormat(f"Rendering Table for Lap {lap_number}: %p%")
    #     self.ui.layout().addWidget(progress)
    #     self.lap_labels[lap_number] = progress

    # def update_lap_label(self, lap_number, percent):
    #     progress = self.lap_labels.get(lap_number)
    #     if progress:
    #         progress.setValue(percent)

    # def remove_lap_label(self, lap_number):
    #     progress = self.lap_labels.pop(lap_number, None)
    #     if progress:
    #         self.ui.layout().removeWidget(progress)
    #         progress.deleteLater()

    @pyqtSlot(int)
    def update_render_progress(self, percent:int):
        self.ui.progress.setValue(percent)
        self.ui.progress.setFormat(f"Rendering... {percent:>3d}%")