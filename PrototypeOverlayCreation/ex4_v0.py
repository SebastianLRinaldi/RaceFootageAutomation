# import cv2
# import numpy as np
# from PIL import ImageFont, ImageDraw, Image

# # Image size
# width, height = 500, 200
# white = (255, 255, 255)
# bg_color = (0, 0, 0)

# # Font path (make sure you have this font or change path)
# font_path = "C:\\Windows\\Fonts\\Helvetica.ttf"
# font = ImageFont.load_default()
# def draw_centered_text_pil(img, text, x, y, font_size, color):
#     pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
#     draw = ImageDraw.Draw(pil_img)
#     font = ImageFont.truetype(font_path, font_size)
#     text_w, text_h = draw.textsize(text, font=font)
#     position = (int(x - text_w / 2), int(y - text_h / 2))
#     draw.text(position, text, font=font, fill=color)
#     return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# # Create blank image
# img = np.zeros((height, width, 3), dtype=np.uint8)
# img[:] = bg_color

# # Draw text
# img = draw_centered_text_pil(img, "Hello, world!", width // 2, height // 2, 48, white)

# # Show image using OpenCV window
# cv2.imshow("Preview", img)
# cv2.waitKey(0)
# cv2.destroyAllWindows()


import cv2
import numpy as np
from PIL import ImageFont, ImageDraw, Image

# Image size
width, height = 500, 200
white = (255, 255, 255)
bg_color = (0, 0, 0)

def draw_centered_text_pil(img, text, x, y, font_size, color):
    pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
    draw = ImageDraw.Draw(pil_img)
    # Use default font if truetype font not available
    try:
        font_path = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
        font = ImageFont.truetype(font_path, font_size)
    except IOError:
        font = ImageFont.load_default()
        print("FALLBACK")

    # Use textbbox for accurate size
    bbox = draw.textbbox((0, 0), text, font=font)
    text_w = bbox[2] - bbox[0]
    text_h = bbox[3] - bbox[1]

    position = (int(x - text_w / 2), int(y - text_h / 2))
    draw.text(position, text, font=font, fill=color)
    return cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)

# Create blank image
img = np.zeros((height, width, 3), dtype=np.uint8)
img[:] = bg_color

# Draw text
img = draw_centered_text_pil(img, "EVA 日本語を楽しいですね", width // 2, height // 2, 48, white)

# Show image using OpenCV window
cv2.imshow("Preview", img)
cv2.waitKey(0)
cv2.destroyAllWindows()
