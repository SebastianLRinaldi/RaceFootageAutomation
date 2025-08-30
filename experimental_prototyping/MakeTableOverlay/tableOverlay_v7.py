import numpy as np
import cv2
import random
from PIL import Image, ImageDraw, ImageFont
import time

class TableGenerator:
    def __init__(self):
        self.FRAME_WIDTH = 530
        self.FRAME_HEIGHT = 1080
        self.PADDING = 10

        self.COL_WIDTHS = [150, 150, 150]  # Just an example width for 3 columns
        self.HEADERS = ["Lap", "Time", "Delta"]

        self.font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"

        self.data_rows = self.generate_fake_lap_times()






    # def test_old(self):
    #         x_frame_center = self.FRAME_WIDTH / 2
    #         y_frame_center = self.FRAME_HEIGHT / 2
    #         text = "ggZ6"
    #         anchor = "mm"
    #         align = "center"


    #         print(f"x_center:{x_frame_center} y_center:{y_frame_center}")
    #         print(f"anchor:{anchor} | align:{align}")
            


    #         # Create a new image for each combination
    #         img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
    #         pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #         draw = ImageDraw.Draw(pil_img)
    #         font = ImageFont.truetype(self.font_path, 128)

    #         # # Draw a green circle at the center
    #         # dot_radius = 64
    #         # left = int(x_center - dot_radius)
    #         # top = int(y_center - dot_radius)
    #         # right = int(x_center + dot_radius)
    #         # bottom = int(y_center + dot_radius)
    #         # draw.ellipse([left, top, right, bottom], fill=(0, 255, 0))
        

    #         # Calculate the text bounding box (RAW)############################
    #         bbox = draw.textbbox((x_frame_center, y_frame_center), text, anchor=anchor, align=align, font=font)
    #         left, top, right, bottom = bbox
    #         center_x = (left + right) / 2
    #         center_y = (top + bottom) / 2

    #         print(f"TEXT: center_x:{center_x} | center_y:{center_y}")

    #         # Draw the bounding box and center lines
    #         draw.rectangle([left, top, right, bottom], outline=(0, 0, 255), width=2)
    #         draw.line([center_x, top, center_x, bottom], fill=(0, 0, 255), width=4)
    #         draw.line([left, center_y, right, center_y], fill=(0, 0, 255), width=4)
    #         #########################################################################


    #         # Corrected Calculate the text bounding box (CORRECTED)############################
    #         x_new_offset = x_frame_center - center_x  # Positive or negative difference
    #         y_new_offset = y_frame_center - center_y  # Positive or negative difference

    #         new_center_x = x_frame_center + x_new_offset
    #         new_center_y = y_frame_center + y_new_offset


            
    #         bbox = draw.textbbox((new_center_x, new_center_y), text, anchor=anchor, align=align, font=font)
    #         left, top, right, bottom = bbox
    #         center_x = (left + right) / 2
    #         center_y = (top + bottom) / 2

    #         print(f"CORRECTEDTEXT: new_x:{new_center_x} | new_y:{new_center_y}")

    #         # Draw the bounding box and center lines
    #         draw.rectangle([left, top, right, bottom], outline=(100, 100, 255), width=2)
    #         draw.line([center_x, top, center_x, bottom], fill=(100, 100, 255), width=4)
    #         draw.line([left, center_y, right, center_y], fill=(100, 100, 255), width=4)
    #         #########################################################################













            

    #         # Draw the middle lines
    #         y_top_center = 0
    #         top_center = (x_frame_center, y_top_center)
    #         y_bottom_center = self.FRAME_HEIGHT
    #         bottom_center = (x_frame_center, y_bottom_center)

    #         x_left_center = 0
    #         left_center = (x_left_center, y_frame_center)
    #         x_right_center = self.FRAME_WIDTH
    #         right_center = (x_right_center, y_frame_center)

    #         draw.line([x_frame_center, y_top_center, x_frame_center, y_bottom_center], fill=(0, 255, 255), width=4)
    #         draw.line([x_left_center, y_frame_center, x_right_center, y_frame_center], fill=(0, 255, 255), width=4)

    #         # Draw the white rectangle around the frame
    #         top_left = (0, 0)
    #         bottom_right = (self.FRAME_WIDTH, self.FRAME_HEIGHT)
    #         draw.rectangle([top_left, bottom_right], outline=(255, 255, 0), width=2)

    #         # Draw the text with current anchor and align settings 
    #         # BAD CENTER
    #         draw.text((x_frame_center, y_frame_center), text, font=font, anchor=anchor, align=align, fill=(255, 255, 255))

    #         # GOOD CENTER
    #         draw.text((new_center_x, new_center_y), text, font=font, anchor=anchor, align=align, fill=(255, 255, 255))

    #         # Convert back to BGR for OpenCV
    #         img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    #         # Display the image
    #         cv2.imshow("Text Image", img)
    #         cv2.waitKey(0)  # Use 1 instead of 0 for non-blocking
    #         cv2.destroyAllWindows()
    
    # def get_text_center(self, draw:ImageDraw.ImageDraw, text, font, xy, color:tuple):
    #     anchor = "mm"
    #     align = "center"
    #     print(f"anchor:{anchor} | align:{align}")
    #     # Get the bounding box of the text
    #     bbox = draw.textbbox(xy, text, anchor=anchor, align=align, font=font)  # (0, 0) means we aren't positioning it yet
    #     bbbox_left, bbox_top, bbox_right, bbox_bottom = bbox

    #     # Calculate the center of the bounding box
    #     x_bbox_center = (bbbox_left + bbox_right) / 2
    #     y_bbox_center = (bbox_top + bbox_bottom) / 2

    #     draw.rectangle([bbbox_left, bbox_top, bbox_right, bbox_bottom], outline=color, width=2)
    #     draw.line([x_bbox_center, bbox_top, x_bbox_center, bbox_bottom], fill=color, width=4)
    #     draw.line([bbbox_left, y_bbox_center, bbox_right, y_bbox_center], fill=color, width=4)


    #     # Draw the text with current anchor and align settings
    #     draw.text(xy, text, font=font, anchor=anchor, align=align, fill=color)

    #     return x_bbox_center, y_bbox_center

    # def test(self):
    #         x_frame_center = self.FRAME_WIDTH / 2
    #         y_frame_center = self.FRAME_HEIGHT / 2
    #         text = "21.010"



    #         print(f"x_center:{x_frame_center} y_center:{y_frame_center}")
            
            


    #         # Create a new image for each combination
    #         img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
    #         pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #         draw = ImageDraw.Draw(pil_img)
    #         font = ImageFont.truetype(self.font_path, 128)


      

    #         # Calculate the text bounding box (RAW)
    #         x_old_bbox_center, y_old_bbox_center = self.get_text_center(draw, text, font, (x_frame_center, y_frame_center), color=(0, 0, 255))
    #         print(f"Text center will be at: ({x_old_bbox_center}, {y_old_bbox_center})")    

    #         # Corrected Calculate the text bounding box (CORRECTED)
    #         # x_new_offset = x_frame_center - x_old_bbox_center  # Positive or negative difference
    #         # y_new_offset = y_frame_center - y_old_bbox_center  # Positive or negative difference

    #         # new_center_x = x_frame_center + x_new_offset
    #         # new_center_y = y_frame_center + y_new_offset


    #         x_adjusted_frame_center = x_frame_center + (x_frame_center - x_old_bbox_center)
    #         y_adjusted_frame_center = y_frame_center + (y_frame_center - y_old_bbox_center )
            
    #         correct_center_x, correct_center_y = self.get_text_center(draw, text, font, (x_adjusted_frame_center, y_adjusted_frame_center), color=(100,100,255))

    #         print(f"CORRECTEDTEXTCENTER: new_x:{correct_center_x} | new_y:{correct_center_y}")
    


    #         ########################################################
    #         # FRAME DRAWING
    #         ########################################################
    #         # Draw the middle lines
    #         y_top_center = 0
    #         top_center = (x_frame_center, y_top_center)
    #         y_bottom_center = self.FRAME_HEIGHT
    #         bottom_center = (x_frame_center, y_bottom_center)

    #         x_left_center = 0
    #         left_center = (x_left_center, y_frame_center)
    #         x_right_center = self.FRAME_WIDTH
    #         right_center = (x_right_center, y_frame_center)

    #         draw.line([x_frame_center, y_top_center, x_frame_center, y_bottom_center], fill=(0, 255, 255), width=2)
    #         draw.line([x_left_center, y_frame_center, x_right_center, y_frame_center], fill=(0, 255, 255), width=2)

    #         # Draw the white rectangle around the frame
    #         top_left = (0, 0)
    #         bottom_right = (self.FRAME_WIDTH, self.FRAME_HEIGHT)
    #         draw.rectangle([top_left, bottom_right], outline=(255, 255, 0), width=2)

    #         # Convert back to BGR for OpenCV
    #         img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    #         # Display the image
    #         cv2.imshow("Text Image", img)
    #         cv2.waitKey(0)  # Use 1 instead of 0 for non-blocking
    #         cv2.destroyAllWindows()

    # def generate_test_alignment_images(self):
    #         # anchors = [
    #         #     "mt", "mb", "lm", "rm", "lt", "rt", "lb", "rb", "mm"
    #         # ]
    #         # aligns = [
    #         #     "left", "center", "right", "justify"
    #         # ]
    #         # values = list(range(100, -100, -10))
    #         values = list(range(100, -100, -10))

    #         anchors = [
    #             "mm"
    #         ]
    #         aligns = [
    #             "center",
    #         ]

    #         values = list(range(20, -20, -2))


            

    #         x_center = self.FRAME_WIDTH / 2
    #         y_center = self.FRAME_HEIGHT / 2
    #         text = "21.010"

    #         for anchor in anchors:
    #             for align in aligns:
    #                 for val in values:
    #                     for x_offset in [val]:
    #                         for y_offset in [val]:

    #                             print(f"anchor:{anchor} | align:{align} | x_offset:{x_offset} | y_offset:{y_offset}")
    #                             x_offset_center = x_center + x_offset
    #                             y_offset_center = y_center + y_offset

    #                             # Create a new image for each combination
    #                             img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
    #                             pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #                             draw = ImageDraw.Draw(pil_img)
    #                             font = ImageFont.truetype(self.font_path, 128)

    #                             # Draw a green circle at the center
    #                             dot_radius = 64
    #                             left = int(x_center - dot_radius)
    #                             top = int(y_center - dot_radius)
    #                             right = int(x_center + dot_radius)
    #                             bottom = int(y_center + dot_radius)
    #                             draw.ellipse([left, top, right, bottom], fill=(0, 255, 0))

    #                             # Calculate the text bounding box
    #                             bbox = draw.textbbox((x_offset_center, y_offset_center), text, anchor=anchor, align=align, font=font)
    #                             left, top, right, bottom = bbox
    #                             center_x = (left + right) / 2
    #                             center_y = (top + bottom) / 2

    #                             # Draw the bounding box and center lines
    #                             draw.rectangle([left, top, right, bottom], outline=(0, 0, 255), width=2)
    #                             draw.line([center_x, top, center_x, bottom], fill=(0, 0, 255), width=4)
    #                             draw.line([left, center_y, right, center_y], fill=(0, 0, 255), width=4)

    #                             # Draw the middle lines
    #                             y_top_center = 0
    #                             top_center = (x_center, y_top_center)
    #                             y_bottom_center = self.FRAME_HEIGHT
    #                             bottom_center = (x_center, y_bottom_center)

    #                             x_left_center = 0
    #                             left_center = (x_left_center, y_center)
    #                             x_right_center = self.FRAME_WIDTH
    #                             right_center = (x_right_center, y_center)

    #                             draw.line([x_center, y_top_center, x_center, y_bottom_center], fill=(0, 255, 255), width=4)
    #                             draw.line([x_left_center, y_center, x_right_center, y_center], fill=(0, 255, 255), width=4)

    #                             # Draw the white rectangle around the frame
    #                             top_left = (0, 0)
    #                             bottom_right = (self.FRAME_WIDTH, self.FRAME_HEIGHT)
    #                             draw.rectangle([top_left, bottom_right], outline=(255, 255, 0), width=2)

    #                             # Draw the text with current anchor and align settings
    #                             draw.text((x_offset_center, y_offset_center), text, font=font, anchor=anchor, align=align, fill=(255, 255, 255))

    #                             # Convert back to BGR for OpenCV
    #                             img = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

    #                             # Display the image
    #                             cv2.imshow("Text Image", img)
    #                             cv2.waitKey(0)  # Use 1 instead of 0 for non-blocking
    #                             cv2.destroyAllWindows()

    # def draw_text_centered(self, text):
    #         x_frame_center = self.FRAME_WIDTH / 2
    #         y_frame_center = self.FRAME_HEIGHT / 2

    #         print(f"x_center:{x_frame_center} y_center:{y_frame_center}")
            
    #         # Create a new image for each combination
    #         img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)
    #         pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    #         draw = ImageDraw.Draw(pil_img)
    #         font = ImageFont.truetype(self.font_path, 128)

    #         # Calculate the text bounding box (RAW)
    #         x_old_bbox_center, y_old_bbox_center = self.get_text_center(draw, text, font, (x_frame_center, y_frame_center), color=(0, 0, 255))
    #         print(f"Text center will be at: ({x_old_bbox_center}, {y_old_bbox_center})")    

    #         x_adjusted_frame_center = x_frame_center + (x_frame_center - x_old_bbox_center)
    #         y_adjusted_frame_center = y_frame_center + (y_frame_center - y_old_bbox_center )
            
    #         correct_center_x, correct_center_y = self.get_text_center(draw, text, font, (x_adjusted_frame_center, y_adjusted_frame_center), color=(100,100,255))

    #         print(f"CORRECTEDTEXTCENTER: new_x:{correct_center_x} | new_y:{correct_center_y}")





























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



    # def calculate_font_size(self,img):
    #     # Start with an initial large font size
    #     total_cells = len(self.data_rows) + 1  # Include header
    #     available_height = img.shape[0]
    #     cell_height = max(self.CELL_HEIGHT_MIN, min(self.CELL_HEIGHT_MAX, available_height // total_cells))

    #     # # Set the font size based on the cell height
    #     # font_size_cell = cell_height  # Font size for regular cells
    #     # font_size_header = int(cell_height * 0.7)  # Slightly smaller font for the header

    #     return optimal_font_size



    def draw_table(self, draw_alignment=False):
        # Define starting position and padding
        rows = len(self.data_rows) + 1  # Number of rows based on your data + 1 for headers
        columns = len(self.HEADERS) if rows > 0 else 0  # Number of columns based on headers

        
        x, y = 0,0
        # cell_width = 200
        # cell_height = 50

        cell_width = (self.FRAME_WIDTH-1)/columns
        cell_height = (self.FRAME_HEIGHT-1)/rows


        
        img = np.zeros((self.FRAME_HEIGHT, self.FRAME_WIDTH, 3), dtype=np.uint8)  # Initial image
        pil_img = Image.fromarray(img)
        draw = ImageDraw.Draw(pil_img)
        # row_font = ImageFont.truetype(self.font_path, 36)
        header_font = ImageFont.truetype(self.font_path, cell_height * 1.05)
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
                self.draw_text_centered(draw, current_font, text,  (cell_center_x,cell_center_y), color=text_color)

                if draw_alignment:
                    # Draw vertical center line through the cell
                    draw.line([cell_center_x, top_left[1], cell_center_x, bottom_right[1]], fill='red', width=1)

                    # Draw horizontal center line through the cell
                    draw.line([top_left[0], cell_center_y, bottom_right[0], cell_center_y], fill='red', width=1)



        pil_img.show()  # This opens the image in the default image viewer


















    def generate_fake_lap_times(self, num_laps=20):
        lap_times = []
        previous_time = 25.000  # Start from a reasonable time
        for lap in range(num_laps):
            lap_time = round(random.uniform(20.000, 30.000), 3)
            delta = round(lap_time - previous_time, 3)
            lap_times.append([lap + 1, lap_time, delta])
            previous_time = lap_time
        return lap_times

    def create_table_with_lap_times(self):
        # Generate fake lap times
        
        # self.test()
        # self.generate_images()

        # # Draw the table with lap times
        self.draw_table()




if __name__ == "__main__":
    generator = TableGenerator()
    generator.create_table_with_lap_times()  # Save the table as an image

