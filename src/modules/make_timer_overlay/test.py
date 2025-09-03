import cv2
import numpy as np
from PIL import Image, ImageDraw, ImageFont
from tqdm import tqdm
import time
import tracemalloc
import subprocess
import time
import tracemalloc
FONT_PATH = "C:\\Users\\epics\\AppData\\Local\\Microsoft\\Windows\\Fonts\\NIS-Heisei-Mincho-W9-Condensed.TTF"
def generate_timer_video_cv(asset_name, width, height, max_time, fps, timer_fill_color=(255, 255, 255)):
    total_frames = int(max_time * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(asset_name, fourcc, fps, (width, height))

    font = cv2.FONT_HERSHEY_SIMPLEX
    font_scale = 2
    thickness = 2

    start_time = time.time()
    tracemalloc.start()

    for frame in tqdm(range(total_frames), desc="Rendering timer video (OpenCV)"):
        time_elapsed = frame / fps
        time_text = f"{time_elapsed:.3f} sec"

        img = np.zeros((height, width, 3), dtype=np.uint8)
        text_size, _ = cv2.getTextSize(time_text, font, font_scale, thickness)
        text_x = (width - text_size[0]) // 2
        text_y = (height + text_size[1]) // 2

        cv2.putText(img, time_text, (text_x, text_y), font, font_scale, timer_fill_color, thickness, cv2.LINE_AA)
        out.write(img)

    out.release()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[OpenCV] Time: {end_time - start_time:.2f}s, Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")

def generate_timer_video_pil(asset_name, width, height, max_time, fps, timer_fill_color=(255, 255, 255)):
    total_frames = int(max_time * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(asset_name, fourcc, fps, (width, height))

    font = ImageFont.truetype(FONT_PATH, 48)

    start_time = time.time()
    tracemalloc.start()

    for frame in tqdm(range(total_frames), desc="Rendering timer video (PIL)"):
        time_elapsed = frame / fps
        time_text = f"{time_elapsed:.3f} sec"

        img = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Use textbbox to get the size
        bbox = draw.textbbox((0, 0), time_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]

        text_x = (width - text_width) // 2
        text_y = (height - text_height) // 2

        draw.text((text_x, text_y), time_text, font=font, fill=timer_fill_color)

        frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[PIL] Time: {end_time - start_time:.2f}s, Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")



def generate_timer_video_cv_pil(asset_name, width, height, max_time, fps, timer_fill_color=(255, 255, 255)):
    """OpenCV video using PIL for custom TTF text"""
    total_frames = int(max_time * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(asset_name, fourcc, fps, (width, height))

    font = ImageFont.truetype(FONT_PATH, 48)

    start_time = time.time()
    tracemalloc.start()

    for frame in tqdm(range(total_frames), desc="Rendering OpenCV+PIL timer video"):
        time_elapsed = frame / fps
        time_text = f"{time_elapsed:.3f} sec"

        # Black frame
        img = np.zeros((height, width, 3), dtype=np.uint8)

        # Convert to PIL
        pil_img = Image.fromarray(cv2.cvtColor(img, cv2.COLOR_BGR2RGB))
        draw = ImageDraw.Draw(pil_img)

        bbox = draw.textbbox((0, 0), time_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        draw.text((x, y), time_text, font=font, fill=timer_fill_color)

        # Back to OpenCV
        frame_bgr = cv2.cvtColor(np.array(pil_img), cv2.COLOR_RGB2BGR)
        out.write(frame_bgr)

    out.release()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[OpenCV+PIL] Time: {end_time - start_time:.2f}s, Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")


def generate_timer_video_pil_bgr(asset_name, width, height, max_time, fps):
    """PIL timer using BGR tuples directly (no RGB->BGR conversion)"""
    total_frames = int(max_time * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(asset_name, fourcc, fps, (width, height))

    font = ImageFont.truetype(FONT_PATH, 48)

    start_time = time.time()
    tracemalloc.start()

    for frame in tqdm(range(total_frames), desc="Rendering PIL (BGR) timer video"):
        time_elapsed = frame / fps
        time_text = f"{time_elapsed:.3f} sec"

        # Create black frame in BGR order
        # Note: PIL still thinks this is RGB, but we'll use BGR tuples
        img = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Measure text size
        bbox = draw.textbbox((0, 0), time_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw text using BGR tuple
        draw.text((x, y), time_text, font=font, fill=(0, 255, 0))  # B=0, G=255, R=0

        # Convert directly to NumPy array without cvtColor
        frame_bgr = np.array(img, dtype=np.uint8)
        out.write(frame_bgr)

    out.release()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[PIL BGR] Time: {end_time - start_time:.2f}s, Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")

def generate_timer_video_cached(asset_name, width, height, max_time, fps):
    total_frames = int(max_time * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(asset_name, fourcc, fps, (width, height))

    # Load font
    font = ImageFont.truetype(FONT_PATH, 48)
    

    # Pre-render every possible time text as PIL image in BGR order
    print("Pre-rendering text images...")
    
    start_time = time.time()
    tracemalloc.start()
    
    cached_frames = {}
    for frame in range(total_frames):
        time_elapsed = frame / fps
        time_text = f"{time_elapsed:.3f} sec"

        # Create PIL image
        img = Image.new("RGB", (width, height), (0, 0, 0))
        draw = ImageDraw.Draw(img)

        # Measure text size
        bbox = draw.textbbox((0, 0), time_text, font=font)
        text_width = bbox[2] - bbox[0]
        text_height = bbox[3] - bbox[1]
        x = (width - text_width) // 2
        y = (height - text_height) // 2

        # Draw text using BGR tuple (so no conversion needed)
        draw.text((x, y), time_text, font=font, fill=(0, 255, 0))  # Example: green in BGR

        # Convert to NumPy BGR array
        frame_bgr = np.array(img, dtype=np.uint8)
        cached_frames[frame] = frame_bgr

    # REAL RENDERING STARTS

    for frame in tqdm(range(total_frames), desc="Rendering cached timer video"):
        out.write(cached_frames[frame])

    out.release()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[Cached PIL BGR] Time: {end_time - start_time:.2f}s, Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")


def generate_timer_video_cached_text(asset_name, width, height, max_time, fps):
    total_frames = int(max_time * fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    out = cv2.VideoWriter(asset_name, fourcc, fps, (width, height))

    font = ImageFont.truetype(FONT_PATH, 48)

    # Reusable background frame (black)
    background = np.zeros((height, width, 3), dtype=np.uint8)

    # Cache for rendered text images
    text_cache = {}

    start_time = time.time()
    tracemalloc.start()

    for frame in tqdm(range(total_frames), desc="Rendering cached text timer video"):
        time_elapsed = frame / fps
        time_text = f"{time_elapsed:.3f} sec"

        # Get or create cached text image
        if time_text not in text_cache:
            # Render text to small image
            dummy_img = Image.new("RGB", (width, height), (0, 0, 0))
            draw = ImageDraw.Draw(dummy_img)
            bbox = draw.textbbox((0, 0), time_text, font=font)
            text_width = bbox[2] - bbox[0]
            text_height = bbox[3] - bbox[1]
            text_img = Image.new("RGB", (text_width, text_height), (0, 0, 0))
            draw_text = ImageDraw.Draw(text_img)
            draw_text.text((0, 0), time_text, font=font, fill=(0, 255, 0))  # BGR

            # Convert to NumPy array (BGR)
            text_cache[time_text] = np.array(text_img, dtype=np.uint8)

        text_frame = text_cache[time_text]
        th, tw, _ = text_frame.shape

        # Copy background to frame
        frame_bgr = background.copy()

        # Compute center
        x = (width - tw) // 2
        y = (height - th) // 2

        # Paste text onto frame
        frame_bgr[y:y+th, x:x+tw] = text_frame

        out.write(frame_bgr)

    out.release()
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()
    print(f"[Cached Text PIL BGR] Time: {end_time - start_time:.2f}s, Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")

def generate_ffmpeg_timer(asset_name, width=640, height=480, duration=5, fps=30, font_path="arial.ttf"):
    # font_path = r"C:\Users\epics\AppData\Local\Microsoft\Windows\Fonts\NIS-Heisei-Mincho-W9-Condensed.TTF"
    # font_path = r"C:/Users/epics/AppData/Local/Microsoft/Windows/Fonts/NIS-Heisei-Mincho-W9-Condensed.TTF"
    # font_path = "C:\\\\Users\\\\epics\\\\AppData\\\\Local\\\\Microsoft\\\\Windows\\\\Fonts\\\\NIS-Heisei-Mincho-W9-Condensed.TTF"
    font_path = "C:/Users/epics/AppData/Local/Microsoft/Windows/Fonts/NIS-Heisei-Mincho-W9-Condensed.TTF"


    # drawtext_filter = (
    #     f"drawtext=fontfile={font_path}:fontsize=48:fontcolor=green:"
    #     f"x=(w-text_w)/2:y=(h-text_h)/2:text='%{{pts}} sec'"
    # )
    # drawtext_filter = (
    #     # f"drawtext=fontfile='{font_path}':fontsize=48:fontcolor=green:"
    #     # f"drawtext=fontfile={font_path}:fontsize=48:fontcolor=green:"
    #     # f"x=(w-text_w)/2:y=(h-text_h)/2:text='%{{pts}} sec'"
    #     f"drawtext=font='NIS-Heisei Mincho W9 Condensed':fontsize=48:fontcolor=green:x=(w-text_w)/2:y=(h-text_h)/2:text='%{{pts}} sec'"
    # )

    font_path = "C:/Users/epics/AppData/Local/Microsoft/Windows/Fonts/NIS-Heisei-Mincho-W9-Condensed.TTF"
    drawtext_filter = (
        f"drawtext=fontfile={font_path}:fontsize=48:fontcolor=green:"
        "x=(w-text_w)/2:y=(h-text_h)/2:text='%{{pts}}'"
    )

    cmd = [
        "ffmpeg",
        "-y",
        "-f", "lavfi",
        "-i", f"color=c=black:s={width}x{height}:d={duration}:r={fps}",
        "-vf", drawtext_filter,
        "-c:v", "libx264",
        "-pix_fmt", "yuv420p",
        asset_name
    ]






    # Start memory and time tracking
    start_time = time.time()
    tracemalloc.start()

    subprocess.run(cmd, check=True)

    # Stop tracking
    end_time = time.time()
    current, peak = tracemalloc.get_traced_memory()
    tracemalloc.stop()

    print(f"[FFmpeg Timer] Time: {end_time - start_time:.2f}s, "
          f"Current Memory: {current/1024:.1f} KB, Peak Memory: {peak/1024:.1f} KB")

if __name__ == "__main__":
    width, height = 640, 480
    max_time = 30  # seconds
    fps = 60
    
    print("Starting FFMPEG timer video...")
    generate_ffmpeg_timer("timer_ffmpeg.mp4", width, height, max_time, fps)

    # print("Starting OpenCV timer video...")
    # generate_timer_video_cv("timer_opencv.mp4", width, height, max_time, fps)

    # # print("\nStarting PIL timer video...")
    # # generate_timer_video_pil("timer_pil.mp4", width, height, max_time, fps)
    
    # # print("\nStarting PIL+CV timer video...")
    # # generate_timer_video_cv_pil("timer_opencv_and_pil.mp4", width, height, max_time, fps)
    
    # print("\nStarting PIL BGR timer video...")
    # generate_timer_video_pil_bgr("timer_pil_BGR.mp4", width, height, max_time, fps)

    # print("\nStarting PIL timer cached video...")
    # generate_timer_video_cached("timer_PIL_cached.mp4", width, height, max_time, fps)

    # print("\nStarting PIL timer EXTRA cached video...")
    # generate_timer_video_cached_text("timer_PIL_EXTRA_cached.mp4", width, height, max_time, fps)