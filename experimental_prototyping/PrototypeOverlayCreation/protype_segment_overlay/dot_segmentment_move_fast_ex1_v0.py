import cv2
import numpy as np
from tqdm import tqdm
import subprocess

# CONFIG
FPS = 60
WIDTH = 800
HEIGHT = 200
LINE_THICKNESS = 2

def save_dot_video_ultrafast(filename, duration_sec):
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, FPS, (WIDTH, HEIGHT))
    frame_count = int(FPS * duration_sec)
    
    # Pre-allocate black frame once
    frame = np.zeros((HEIGHT, WIDTH, 3), dtype=np.uint8)

    prev_x_pos = None
    line_thickness = 2

    for f in tqdm(range(frame_count), desc="Saving dot overlay ULTRAFAST video"):
        progress = f / frame_count
        x_pos = int(progress * WIDTH)

        # Only update if x_pos changes
        if prev_x_pos != x_pos:
            if prev_x_pos is not None:
                # Clear previous line
                frame[:, prev_x_pos:prev_x_pos+line_thickness, :] = 0

            # Draw new line
            frame[:, x_pos:x_pos+line_thickness, :] = 255

            prev_x_pos = x_pos

        # Write frame (even if not changed — VideoWriter needs full sequence)
        writer.write(frame)

    writer.release()



# MAIN
if __name__ == "__main__":
    import cv2
    import numpy as np
    from tqdm import tqdm

    # Config
    WIDTH = 800
    HEIGHT = 200
    FPS = 60

    output_file = "dot_overlay_ultrafast.mp4"
    LAP_TIMES = [23.715, 22.728, 22.784, 22.75, 23.901, 23.076, 22.719, 22.742, 23.345,
                22.614, 22.423, 23.725, 22.988, 22.766, 22.386, 22.592, 22.322, 22.796,
                22.49, 22.315, 22.473, 22.187, 22.221]

    total_duration_sec = sum(LAP_TIMES) 

    save_dot_video_ultrafast(output_file, total_duration_sec)
