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

class Logic:
    def __init__(self, ui: Layout):
        self.ui = ui
        self.project_directory = ProjectDirectory()

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

        self.padding_top = 10
        self.padding_bottom = 10
        self.padding_left = 10
        self.padding_right = 10


        # Dynamic headers and column widths - add more columns here
        self.HEADERS = ["Lap", "Time", "Best Lap Diff"]  
        self.COL_WIDTHS = [100, 142, 334]

        self.ROW_HEIGHT_MIN = 20
        self.ROW_HEIGHT_MAX = 40

        self.PADDING = {
            'top': 10,
            'bottom': 10,
            'left': 10,
            'right': 10
        }

        # Computed constants
        
        # self.TABLE_WIDTH = sum(self.COL_WIDTHS)
        # self.FRAME_WIDTH = self.TABLE_WIDTH + self.PADDING['left'] + self.PADDING['right']

        self.FRAME_WIDTH = 530
        self.FRAME_HEIGHT = 1080
        
        self.TOTAL_ROWS = len(self.project_directory.lap_times) + 1
        # self.FRAME_HEIGHT = (self.TOTAL_ROWS * self.ROW_HEIGHT_MAX) + self.PADDING['top'] + self.PADDING['bottom']

        self.TABLE_X = 0 #self.PADDING['left']
        self.TABLE_Y = 0 #self.PADDING['top']

        self.WHITE = (255, 255, 255)

        


        SETTINGS_FIELDS = [
            ("width", self.ui.width_input, self.width),
            ("height", self.ui.height_input, self.height),
            ("fps", self.ui.fps_input, self.fps),
            ("use_gpu", self.ui.use_gpu_checkbox, self.use_gpu),

            ("padding_top", self.ui.padding_top_input, self.padding_top),
            ("padding_bottom", self.ui.padding_bottom_input, self.padding_bottom),
            ("padding_left", self.ui.padding_left_input, self.padding_left),
            ("padding_right", self.ui.padding_right_input, self.padding_right),

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
        self.TABLE_WIDTH = sum(self.COL_WIDTHS)
        self.FRAME_WIDTH = self.TABLE_WIDTH + self.PADDING['left'] + self.PADDING['right']
        
        self.TOTAL_ROWS = len(self.project_directory.lap_times) + 1
        self.FRAME_HEIGHT = (self.TOTAL_ROWS * self.ROW_HEIGHT_MAX) + self.PADDING['top'] + self.PADDING['bottom']

        # self.TABLE_X = self.PADDING['left']
        # self.TABLE_Y = self.PADDING['top']

    def generate_overlay(self):
        self.ui.generate_button.setEnabled(False)
        self.ui.status_label.setText("Generating Table Overlay...")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.worker = OverlayWorker(self)
        self.worker.finished.connect(self.on_finished)
        self.worker.error.connect(self.on_error)
        self.worker.start()

    def on_finished(self):
        self.ui.status_label.setText(f"✅ Done: {self.project_directory.make_rendered_file_path(self.rendered_name)}")
        self.ui.generate_button.setEnabled(True)

    def on_error(self, err_type: str, tb_str: str):
        msg = f"Exception type: {err_type}\n\nTraceback:\n{tb_str}"
        print(msg)
        QMessageBox.critical(self.ui, "Error", msg)
        self.ui.status_label.setText(f"❌ Failed: {err_type}")
        self.ui.status_label.setTextInteractionFlags(Qt.TextInteractionFlag.TextSelectableByMouse)
        self.ui.generate_button.setEnabled(True)

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
        subprocess.run(cmd, check=True)













    # def draw_centered_text_pil(self, img, text, x, y, font_size, color):
    #     pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #     draw = ImageDraw.Draw(pil_img)
    #     font = ImageFont.truetype(self.font_path, font_size)
    #     bbox = draw.textbbox((x, y), text, anchor="mm", align="center", font=font)


    #     draw.text((x, y), text, anchor="mm", align="center", font=font, fill=color)




        
    #     dot_radius = int(font_size / 4)  # Adjust the size of the dot relative to the font size
        
    #     # Calculate the bounding box for the dot
    #     left = int(x - dot_radius)
    #     top = int(y - dot_radius)
    #     right = int(x + dot_radius)
    #     bottom = int(y + dot_radius)

    #     draw.ellipse([left, top, right, bottom], fill=(0, 255, 0))

    #     left, top, right, bottom = bbox  # Unpack the bounding box coordinates

    #     # Calculate center of bounding box for the red lines
    #     center_x = (left + right) // 2  # Middle X of text box
    #     center_y = (top + bottom) // 2  # Middle Y of text box

    #     # Draw the vertical red line (center of text box)
    #     draw.line([center_x, top, center_x, bottom], fill=(0, 0, 255), width=4)

    #     # Draw the horizontal red line (center of text box)
    #     draw.line([left, center_y, right, center_y], fill=(0, 0, 255), width=4)
    #     draw.rectangle([left, top, right, bottom], outline=(0, 0, 255), width=1)  # Red rectangle
        
    #     # Draw the dot (ellipse with equal width and height)
    #     # draw.text([left, top, right, bottom], text, font=font, fill=color)
    #     # draw.text(position, text, font=font, fill=(255, 0, 255))


    #     # left = int(position[0] - dot_radius)
    #     # top = int(position[1] - dot_radius)
    #     # right = int(position[0] + dot_radius)
    #     # bottom = int(position[1] + dot_radius)
        
    #     # # Draw the dot at the text position
    #     # draw.ellipse([left, top, right, bottom], fill=(255, 0, 255))  # Red dot


        



        
    #     return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    # def draw_table(self, img, x, y, data_rows):
    #     total_rows = len(data_rows) + 1  # +1 for header
    #     available_height = img.shape[0] - y - self.PADDING['bottom']
    #     row_h = max(self.ROW_HEIGHT_MIN, min(self.ROW_HEIGHT_MAX, available_height // total_rows))

    #     font_size_header = row_h#int(row_h * 0.7)
    #     font_size_row = row_h#int(row_h * 0.7)

    #     # Draw header row
    #     col_x = x
    #     for i, header in enumerate(self.HEADERS):
    #         center_x = col_x + self.COL_WIDTHS[i] // 2
    #         print(f"{center_x}, {y}, {row_h} | {row_h // 2} | {y + row_h // 2}")
    #         img = self.draw_centered_text_pil(img, header, center_x, y + row_h // 2, font_size_header, self.WHITE)
    #         col_x += self.COL_WIDTHS[i]
    #     cv2.rectangle(img, (x, y), (x + self.TABLE_WIDTH, y + row_h), self.WHITE, 1)
    #     # Vertical lines in header
    #     col_x = x
    #     for width in self.COL_WIDTHS[:-1]:
    #         col_x += width
    #         cv2.line(img, (col_x, y), (col_x, y + row_h), self.WHITE, 1)

    #     # Draw data rows
    #     for i, row in enumerate(data_rows):
    #         top = y + row_h * (i + 1)
    #         cv2.rectangle(img, (x, top), (x + self.TABLE_WIDTH, top + row_h), self.WHITE, 1)
    #         col_x = x
    #         for j, cell in enumerate(row):
    #             center_x = col_x + self.COL_WIDTHS[j] // 2
    #             text = f"{cell}" if cell is not None else "N/A"
    #             img = self.draw_centered_text_pil(img, text, center_x, top + row_h // 2, font_size_row, self.WHITE)
    #             col_x += self.COL_WIDTHS[j]



    #             # Draw two red lines through the center of the cell (both horizontal and vertical)
    #             # Horizontal red line through the center
    #             cv2.line(img, (x, top + row_h // 2), (x + self.TABLE_WIDTH, top + row_h // 2), (0, 0, 255), 2)
    #             # Vertical red line through the center
    #             cv2.line(img, (center_x, top), (center_x, top + row_h), (0, 0, 255), 2)
    #         # vertical lines
    #         col_x = x
    #         for width in self.COL_WIDTHS[:-1]:
    #             col_x += width
    #             cv2.line(img, (col_x, top), (col_x, top + row_h), self.WHITE, 1)

    #     return img

    # def create_blank_video(self, duration, filename):
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     writer = cv2.VideoWriter(filename, fourcc, self.fps, frameSize=(int(self.FRAME_WIDTH), int(self.FRAME_HEIGHT)))
    #     blank = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
    #     frame_count = int(self.fps* duration)
    #     try:
    #         for _ in range(frame_count):
    #             writer.write(blank)
    #     finally:
    #         writer.release()  # Ensure it's always released
    #         del writer

    # # def draw_headers(self):
    # #     # Header only
    # #     img = self.draw_table(
    # #         img=np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8),
    # #         x=self.TABLE_X,
    # #         y=self.TABLE_Y,
    # #         data_rows=[]
    # #     )

    # #     return img

    # # def create_headers_video(self, duration, filename):
    # #     frame_count = int(duration * self.fps)
    # #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # #     writer = cv2.VideoWriter(filename, fourcc, self.fps, frameSize=(self.FRAME_WIDTH, self.FRAME_HEIGHT))

    # #     # Create a styled stats frame using PIL
    # #     # img = Image.new("RGB", (WIDTH, HEIGHT), (0, 0, 0))
    # #     # draw = ImageDraw.Draw(img)
    # #     img = self.draw_headers()
        
    # #     frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # #     try:
    # #         for _ in range(frame_count):
    # #             writer.write(frame_bgr)
    # #     finally:
    # #         writer.release()  # Ensure it's always released

    # # def create_lap_table(self, lap_number, target_lap, temp_dir):
    # #     current_laps = self.project_directory.lap_time_deltas[:lap_number]
    # #     current_data = []

    # #     for idx, current_lap in enumerate(current_laps):
    # #         lap = idx + 1
    # #         time_str = f"{current_lap[0]}"
    # #         delta = f"{current_lap[1]}"
    # #         current_data.append([lap, time_str, delta])

    # #     duration = float(target_lap[0])
    # #     frame_count = int(duration * self.fps)
    # #     filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
    # #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    # #     writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT))


    # #     img = self.draw_table(
    # #             img=np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8),
    # #             x=self.TABLE_X,
    # #             y=self.TABLE_Y,
    # #             data_rows=current_data
    # #         )
        
    # #     frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    # #     for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
    # #         writer.write(frame_bgr)

    # #     writer.release()
    # #     return filename

    # # def create_last_lap_table(self, lap_number, temp_dir):
    #     print(f"lap_number: {lap_number}")
    #     current_laps = self.project_directory.lap_time_deltas[:lap_number]
    #     current_data = []

    #     print(f"current_laps: {current_laps}")
        

    #     for idx, current_lap in enumerate(current_laps):
    #         print(current_lap)
    #         lap = idx + 1
    #         time_str = f"{current_lap[0]}"
    #         delta = f"{current_lap[1]}"
    #         current_data.append([lap, time_str, delta])


    #     fps_float = float(self.fps)
    #     frame_count = int(self.end_duration * fps_float)
    #     filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
    #     fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    #     writer = cv2.VideoWriter(filename, fourcc, fps_float, (self.FRAME_WIDTH, self.FRAME_HEIGHT))


    #     img = self.draw_table(
    #             img=np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8),
    #             x=self.TABLE_X,
    #             y=self.TABLE_Y,
    #             data_rows=current_data
    #         )
        
    #     frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    #     for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
    #         writer.write(frame_bgr)

    #     writer.release()
    #     return filename

    # def make_table_overlay(self):

    #     with tempfile.TemporaryDirectory() as temp_dir:
    #         # 1. Create start blank video
    #         start_blank = os.path.join(temp_dir, "start_blank.mp4")
    #         print("Creating Blank")
    #         self.create_blank_video(self.start_duration, start_blank)
    #         # create_headers_video(END_DURATION, filename)
            
    #         # print(f"lap_timed{self.project_directory.lap_times}")
    #         # print(f"lap_time_deltas{self.project_directory.lap_time_deltas}")

    #         # print(f"len(lap_time_deltas)={len(self.project_directory.lap_time_deltas)} | len(lap_times)={len(self.project_directory.lap_times)}")
    #         last_lap_video = self.create_last_lap_table(len(self.project_directory.lap_times), temp_dir)
    #         # 2. Render laps in parallel
    #         lap_videos = [last_lap_video]

    #         render_single = True

    #         # for i, target_lap in enumerate(LAP_TIMES):
    #         #     lap_videos.append(create_lap_table( i , target_lap, temp_dir))
            
    #         if render_single:
    #             lap_video = self.create_lap_table( 23, self.project_directory.lap_time_deltas[23], temp_dir)
    #             lap_videos.append(lap_video)
    #         else:
    #             with ThreadPoolExecutor() as executor:
    #                 futures = {
    #                             executor.submit(self.create_lap_table, i , target_lap, temp_dir): i
    #                             for i, target_lap in enumerate(self.project_directory.lap_time_deltas)
    #                         }

    #                 for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
    #                     lap_number = futures[future]
    #                     lap_videos.append(future.result())

    #         # Sort videos by lap number (they can complete out of order)
    #         lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

    #         # 3. Concatenate all videos: start_blank + lap videos
    #         self.concat_videos(lap_videos, self.rendered_name)

    #         # Temp files deleted automatically on context exit
    #         print(f"✅ Timer Overlay Video saved as {self.project_directory.make_rendered_file_path(self.rendered_name)}")
    #         print(f'File "{self.project_directory.make_rendered_file_path(self.rendered_name)}"')






















    def get_text_center(self, draw:ImageDraw.ImageDraw, text, font, xy, color:tuple=(255,255,255), draw_alignment=False, draw_text=False):
        anchor = "mm"
        align = "center"
        """
        Good colors = 
        (100,100,255)
        (0, 0, 255)
        """
        
        # Get the bounding box of the text
        bbox = draw.textbbox(xy, text, anchor=anchor, align=align, font=font)  # (0, 0) means we aren't positioning it yet
        bbbox_left, bbox_top, bbox_right, bbox_bottom = bbox

        # Calculate the center of the bounding box
        x_bbox_center = (bbbox_left + bbox_right) / 2
        y_bbox_center = (bbox_top + bbox_bottom) / 2

        if draw_alignment:
            # Calculate width and height of the text box
            text_box_width = bbox_right - bbbox_left
            text_box_height = bbox_bottom - bbox_top

            # Print the width and height of the text box
            print(f"Text box width: {text_box_width}, height: {text_box_height}")
            draw.rectangle([bbbox_left, bbox_top, bbox_right, bbox_bottom], outline=color, width=1)
            draw.line([x_bbox_center, bbox_top, x_bbox_center, bbox_bottom], fill=color, width=3)
            draw.line([bbbox_left, y_bbox_center, bbox_right, y_bbox_center], fill=color, width=3)

        if draw_text:
            # Draw the text with current anchor and align settings
            draw.text(xy, text, font=font, anchor=anchor, align=align, fill=color)

        return x_bbox_center, y_bbox_center

    def draw_text_centered(self, draw:ImageDraw.ImageDraw, font, text, xy:tuple, color:tuple=(255,255,255)):
        x_frame_center, y_frame_center=xy

        # print(f"x_center:{x_frame_center} y_center:{y_frame_center}")

        # Calculate the text bounding box (RAW)
        x_old_bbox_center, y_old_bbox_center = self.get_text_center(draw, text, font, (x_frame_center, y_frame_center), color=color)
        # print(f"Text center will be at: ({x_old_bbox_center}, {y_old_bbox_center})")    

        x_adjusted_frame_center = x_frame_center + (x_frame_center - x_old_bbox_center)
        y_adjusted_frame_center = y_frame_center + (y_frame_center - y_old_bbox_center )
        
        correct_center_x, correct_center_y = self.get_text_center(draw, text, font, (x_adjusted_frame_center, y_adjusted_frame_center), color=color, draw_text=True, draw_alignment=False)

        # print(f"CORRECTEDTEXTCENTER: new_x:{correct_center_x} | new_y:{correct_center_y}")

    def draw_table(self, data_rows:list, draw_alignment=False):
        # Define starting position and padding
        rows = len(data_rows) + 1  # Number of rows based on your data + 1 for headers
        columns = len(self.HEADERS) if rows > 0 else 0  # Number of columns based on headers

        
        x, y = 0,0

        cell_width = (self.FRAME_WIDTH-1)/columns
        # cell_height = (self.FRAME_HEIGHT-1)/rows
        max_cell_height = 50  # Example max height (adjust as needed)
        cell_height = min((self.FRAME_HEIGHT - 1) / rows, max_cell_height)

        # print(f"cell_width:{cell_width} | cell_height:{cell_height} | rows:{rows} | columns{columns}")


        
        img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)  # Initial image
        
        # pil_img = Image.fromarray(img)
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
                top_left = (x_pos, y + row * cell_height)
                bottom_right = (x_pos + col_width, y + (row + 1) * cell_height)


                

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


                
                self.draw_text_centered(draw, current_font, text,  (cell_center_x,cell_center_y), color=text_color)

                if draw_alignment:
                    # Draw vertical center line through the cell
                    draw.line([cell_center_x, top_left[1], cell_center_x, bottom_right[1]], fill='red', width=1)

                    # Draw horizontal center line through the cell
                    draw.line([top_left[0], cell_center_y, bottom_right[0], cell_center_y], fill='red', width=1)
        # pil_img.show()  # This opens the image in the default image viewer
        return pil_img

    def create_table_section(self, lap_number, target_lap, temp_dir):
        print(f"lap_number: {lap_number}")
        current_laps = self.project_directory.lap_time_deltas[:lap_number]

        duration = float(target_lap[1])
        frame_count = int(duration * self.fps)
        filename = os.path.join(temp_dir, f"lap_{lap_number:02}.mp4")
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')
        writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.FRAME_WIDTH, self.FRAME_HEIGHT))


        img = self.draw_table(current_laps)

        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)


        try:
            for _ in tqdm(range(frame_count), desc=f"Rendering Table for Lap {lap_number}"):
                writer.write(frame_bgr)
        finally:
            writer.release()  # Ensure it's always released
            del writer


        return filename



    def make_table_overlay(self):
        with tempfile.TemporaryDirectory() as temp_dir:
            # 1. Create start blank video
            # start_blank = os.path.join(temp_dir, "start_blank.mp4")
            # print("Creating Blank")
            # self.create_blank_video(self.start_duration, start_blank)
            # create_headers_video(END_DURATION, filename)
            
            # print(f"lap_timed{self.project_directory.lap_times}")
            # print(f"lap_time_deltas{self.project_directory.lap_time_deltas}")

            # # print(f"len(lap_time_deltas)={len(self.project_directory.lap_time_deltas)} | len(lap_times)={len(self.project_directory.lap_times)}")
            # last_lap_video = self.create_last_lap_table(len(self.project_directory.lap_times), temp_dir)
            # # 2. Render laps in parallel
            # self.create_table_section(len(self.project_directory.lap_times), temp_dir)
            # lap_videos = [last_lap_video]




            

            render_single = False

            # for i, target_lap in enumerate(LAP_TIMES):
            #     lap_videos.append(create_lap_table( i , target_lap, temp_dir))
            lap_videos = []
            if render_single:
                lap_video = self.create_table_section( 2, self.project_directory.lap_time_deltas[2], temp_dir)
                lap_videos.append(lap_video)
            else:
                with ThreadPoolExecutor() as executor:
                    futures = {
                                executor.submit(self.create_table_section, i , target_lap, temp_dir): i
                                for i, target_lap in enumerate(self.project_directory.lap_time_deltas)
                            }

                    for future in tqdm(as_completed(futures), total=len(futures), desc="Rendering laps in parallel"):
                        lap_number = futures[future]
                        lap_videos.append(future.result())

            # Sort videos by lap number (they can complete out of order)
            lap_videos.sort(key=lambda x: int(os.path.basename(x).split('_')[1].split('.')[0]))

            # 3. Concatenate all videos: start_blank + lap videos
            self.concat_videos(lap_videos, self.rendered_name)

            # Temp files deleted automatically on context exit
            print(f"✅ Timer Overlay Video saved as {self.project_directory.make_rendered_file_path(self.rendered_name)}")
            print(f'File "{self.project_directory.make_rendered_file_path(self.rendered_name)}"')












            