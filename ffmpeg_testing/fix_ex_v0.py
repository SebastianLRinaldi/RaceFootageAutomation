import subprocess

# subprocess.run([
#     "ffmpeg",
#     "-y",
#     "-i", "lap_table_video_test_multi_column.mp4",
#     "-movflags", "+faststart",
#     "-c", "copy",
#     "fixed_overlay1.mp4"
# ], check=True)


subprocess.run([
    "ffmpeg",
    "-y",
    "-i", "lap_table_video_test_multi_column.mp4",
    "-movflags", "+faststart",
    "-c:v", "libx264",
    "-pix_fmt", "yuv420p",
    "-crf", "18",
    "-preset", "slow",
    "fixed_overlay2.mp4"
], check=True)