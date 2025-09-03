# import subprocess

# input_file = "Timer_Overlay.mp4"
# output_file = "with_chapters.mp4"
# metadata_file = "chapters.txt"

# cmd = [
#     "ffmpeg", "-i", input_file,
#     "-i", metadata_file,
#     "-map_metadata", "1",
#     "-map_chapters", "1",
#     "-codec", "copy",
#     output_file
# ]
# subprocess.run(cmd, check=True)


def format_timestamp(seconds: float) -> str:
    sec = int(seconds)  # floor to whole seconds
    m, s = divmod(sec, 60)
    h, m = divmod(m, 60)
    return f"{h:d}:{m:02d}:{s:02d}" if h else f"{m:d}:{s:02d}"

def generate_chapters(buffer=5, laps=20, lap_duration=25, cooldown=10):
    chapters = []
    t = 0

    # buffer
    chapters.append((t, "Pit Exit / Buffer"))
    t += buffer

    # laps
    for i in range(1, laps + 1):
        chapters.append((t, f"Lap {i}"))
        t += lap_duration

    # cooldown
    chapters.append((t, "Cool Down Lap"))
    t += cooldown

    # print block
    for sec, title in chapters:
        print(f"{format_timestamp(sec)} {title}")

# Example: 5 sec buffer, 19 laps, 23 sec each, 10 sec cooldown
generate_chapters(buffer=5, laps=19, lap_duration=23, cooldown=10)

