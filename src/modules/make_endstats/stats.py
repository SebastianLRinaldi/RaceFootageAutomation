def create_end_stats(self, duration, filename):
    frame_count = int(duration * self.fps)
    fourcc = cv2.VideoWriter_fourcc(*'mp4v')
    writer = cv2.VideoWriter(filename, fourcc, self.fps, (self.width, self.height), True)

    # Create a styled stats frame using PIL
    img = Image.new("RGB", (self.width, self.height), (0, 0, 0))
    draw = ImageDraw.Draw(img)
    self.draw_stats(draw)

    frame_bgr = cv2.cvtColor(np.array(img), cv2.COLOR_RGB2BGR)

    for _ in range(frame_count):
        writer.write(frame_bgr)

    writer.release()

def draw_stats(self, draw):
    avg = sum(self.project_directory.lap_times) / len(self.project_directory.lap_times)
    best = min(self.project_directory.lap_times)
    worst = max(self.project_directory.lap_times)
    diff = worst - best

    stats = [
        f"Avg:   {avg:.3f} sec",
        f"Best:  {best:.3f} sec",
        f"Worst: {worst:.3f} sec",
        f"Δ:     {diff:.3f} sec"
    ]

    txt_pos = {"start_y": self.width  // 2-self.distance_from_center, "spacing": self.spacing, "fill": self.stats_fill_color}

    self.draw_centered_text(draw, stats, txt_pos)