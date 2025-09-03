from PIL import ImageFont, ImageDraw, Image

def get_text_center(draw:ImageDraw.ImageDraw, text, font, xy, color:tuple=(255,255,255), draw_alignment=False, draw_text=False):
    anchor = "mm"
    align = "center"
    """
    Good colors = 
    
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
        # print(f"Text box width: {text_box_width}, height: {text_box_height}")
        draw.rectangle([bbbox_left, bbox_top, bbox_right, bbox_bottom], outline=(100,100,255), width=1)
        draw.line([x_bbox_center, bbox_top, x_bbox_center, bbox_bottom], fill=(100,100,255), width=3)
        draw.line([bbbox_left, y_bbox_center, bbox_right, y_bbox_center], fill=(100,100,255), width=3)

    if draw_text:
        # Draw the text with current anchor and align settings
        draw.text(xy, text, font=font, anchor=anchor, align=align, fill=color)

    return x_bbox_center, y_bbox_center






def draw_text_centered( draw:ImageDraw.ImageDraw, font:ImageFont.FreeTypeFont, text, xy:tuple, color:tuple=(255,255,255)):
    x_frame_center, y_frame_center=xy
    
    # x_frame_center = x_frame_center // 2
    # y_frame_center = y_frame_center // 2
    
    """
    GOOD CODE
    """
    x_old_bbox_center, y_old_bbox_center = get_text_center(draw, text, font, (x_frame_center, y_frame_center), color=color, draw_text=False, draw_alignment=False)

    x_adjusted_frame_center = x_frame_center + (x_frame_center - x_old_bbox_center)
    y_adjusted_frame_center = y_frame_center + (y_frame_center - y_old_bbox_center )
    
    correct_center_x, correct_center_y = get_text_center(draw, text, font, (x_adjusted_frame_center, y_adjusted_frame_center), color=color, draw_text=True, draw_alignment=False)