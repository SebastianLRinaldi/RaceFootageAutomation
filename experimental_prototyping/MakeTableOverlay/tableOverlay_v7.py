import numpy as np
import cv2
import random
from PIL import Image, ImageDraw, ImageFont
import time
import subprocess
import os
import tempfile
class TableGenerator:
    def __init__(self):
        self.FRAME_WIDTH = 530
        self.FRAME_HEIGHT = 1080
        self.PADDING = 10

        self.COL_WIDTHS = [150, 150, 150]  # Just an example width for 3 columns
        self.HEADERS = ["Lap", "Time", "Delta"]

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

        self.data_rows = self.generate_fake_lap_times()




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
            draw.rectangle([bbbox_left, bbox_top, bbox_right, bbox_bottom], outline=color, width=1)
            draw.line([x_bbox_center, bbox_top, x_bbox_center, bbox_bottom], fill=color, width=3)
            draw.line([bbbox_left, y_bbox_center, bbox_right, y_bbox_center], fill=color, width=3)

        if draw_text:
            # Draw the text with current anchor and align settings
            draw.text(xy, text, font=font, anchor=anchor, align=align, fill=color)

        return x_bbox_center, y_bbox_center


    def draw_text_centered(self, draw:ImageDraw.ImageDraw, font, text, xy:tuple, color:tuple=(255,255,255)):

            x_frame_center, y_frame_center=xy


            print(f"x_center:{x_frame_center} y_center:{y_frame_center}")

            # Calculate the text bounding box (RAW)
            x_old_bbox_center, y_old_bbox_center = self.get_text_center(draw, text, font, (x_frame_center, y_frame_center), color=color)
            print(f"Text center will be at: ({x_old_bbox_center}, {y_old_bbox_center})")    

            x_adjusted_frame_center = x_frame_center + (x_frame_center - x_old_bbox_center)
            y_adjusted_frame_center = y_frame_center + (y_frame_center - y_old_bbox_center )
            
            correct_center_x, correct_center_y = self.get_text_center(draw, text, font, (x_adjusted_frame_center, y_adjusted_frame_center), color=color, draw_text=True, draw_alignment=False)

            print(f"CORRECTEDTEXTCENTER: new_x:{correct_center_x} | new_y:{correct_center_y}")





    def draw_table(self, draw_alignment=False):
        # Define starting position and padding
        rows = len(self.data_rows) + 1  # Number of rows based on your data + 1 for headers
        columns = len(self.HEADERS) if rows > 0 else 0  # Number of columns based on headers

        
        x, y = 0,0

        cell_width = (self.FRAME_WIDTH-1)/columns
        cell_height = (self.FRAME_HEIGHT-1)/rows


        
        img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)  # Initial image
        # pil_img = Image.fromarray(img)
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)
        # row_font = ImageFont.truetype(self.font_path, 36)
        header_font = ImageFont.truetype(self.font_path, cell_height * 0.9)
        row_font = ImageFont.truetype(self.font_path, cell_height * 0.8)
        
        sorted_rows = sorted(enumerate(self.data_rows), key=lambda x: x[1][1])  # Sort by time in column 1
        best_time_row = sorted_rows[0][0] + 1  # Best time row (add 1 for header offset)
        second_best_row = sorted_rows[1][0] + 1  # Second best time row
        third_best_row = sorted_rows[2][0] + 1  # Third best time row
        worst_time_row = sorted_rows[-1][0] + 1  # Worst time row

        # Draw the grid (rows and columns)
        for row in range(rows):  # We now have an extra row for headers
            for col in range(columns):
                # Calculate top left and bottom right coordinates of each cell
                top_left = (x + col * cell_width, y + row * cell_height)
                bottom_right = (x + (col + 1) * cell_width, y + (row + 1) * cell_height)

                # Draw the rectangle for the cell
                draw.rectangle([top_left, bottom_right], outline=(255,255,255), width=1)


                # Add the corresponding data inside the cell (centered)
                if row == 0:
                    text = self.HEADERS[col]  # Use header text for the first row
                    current_font = header_font  # Use header font for the header
                    text_color = (255, 255, 255)
                else:

                    print(f"row{row} [length: row={rows }] | col{col} [length: col={columns}]")
                    print(f"data_rows[row - 1]: {self.data_rows[row - 1]}")
                    
                    text = str(self.data_rows[row - 1][col])  # Subtract 1 from row index for data rows
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
                print(f"TEXT={text} | type={type(text)}")
                self.draw_text_centered(draw, current_font, text,  (cell_center_x,cell_center_y), color=text_color)

                if draw_alignment:
                    # Draw vertical center line through the cell
                    draw.line([cell_center_x, top_left[1], cell_center_x, bottom_right[1]], fill='red', width=1)

                    # Draw horizontal center line through the cell
                    draw.line([top_left[0], cell_center_y, bottom_right[0], cell_center_y], fill='red', width=1)



        # pil_img.show()  # This opens the image in the default image viewer
        
        return pil_img #cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)







    def make_video(self):
        # Get the single table frame
        frame = self.draw_table()
        

        # Set the total number of frames for a 30-second video at 30 FPS
        frame_count = 30 * 15  # 30 FPS * 15 seconds

        # Initialize the VideoWriter object
        fourcc = cv2.VideoWriter_fourcc(*'mp4v')  # You can change this codec if needed
        video_writer = cv2.VideoWriter('output.mp4', fourcc, 30.0, (self.FRAME_WIDTH, self.FRAME_HEIGHT))

        # Write the same frame multiple times into the video
        for _ in range(frame_count):
            video_writer.write(np.array(frame))  # Directly write the frame

        # Release the VideoWriter
        video_writer.release()

        print("DONE")







    def generate_fake_lap_times(self, num_laps=20):
        lap_times = []
        previous_time = 25.000  # Start from a reasonable time
        for lap in range(num_laps):
            lap_time = round(random.uniform(20.000, 30.000), 3)
            delta = round(lap_time - previous_time, 3)
            lap_times.append([lap + 1, lap_time, delta])
            previous_time = lap_time
        return lap_times





if __name__ == "__main__":
    generator = TableGenerator()
    generator.make_video()





