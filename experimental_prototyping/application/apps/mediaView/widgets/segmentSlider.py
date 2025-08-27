import sys
from typing import List, Tuple
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *

class MarkedSlider(QSlider):
    def __init__(self, orientation=Qt.Orientation.Horizontal, parent=None):
        super().__init__(orientation, parent)
        self.lap_segments: List[Tuple[float, float, str]] = []

    def set_lap_times_from_durations(self, base_time: float, durations: List[float], threshold: float):
        self.lap_segments = []
        current_time = base_time

        self.lap_segments.append((0, current_time, "#000000"))

        
        for i, duration in enumerate(durations):
            
            color = "#00FF00" if duration <= threshold else "#FF0000"
            self.lap_segments.append((current_time + duration,  current_time + duration , "#A013FF"))
            self.lap_segments.append((current_time, current_time + duration, color))
            

            current_time += duration
        self.update()



    def paintEvent(self, event):
        super().paintEvent(event)
        if not self.lap_segments:
            return

        painter = QPainter(self)
        slider_min = self.minimum()
        slider_max = self.maximum()
        slider_range = slider_max - slider_min

        slider_length = self.style().pixelMetric(QStyle.PixelMetric.PM_SliderLength)
        available_width = self.width() - slider_length
        # offset = slider_length // 2

        for start, end, color in self.lap_segments:
            # start_ratio = (start - slider_min) / slider_range
            # end_ratio = (end - slider_min) / slider_range

            # start_x = int(start_ratio * available_width)
            # end_x = int( end_ratio * available_width)

            
            start_x = int(start)
            end_x = int( end)

            if color == "#A013FF":  # Separator color
                painter.setPen(QPen(QColor(color), 2))  # thicker line
                # top = self.height() // 4
                # bottom = self.height() * 3 // 4
                # x = (start_x + end_x) // 2
                # painter.drawLine(x, top, x, bottom)  # vertical line
                top = self.height() // 4
                y = self.height() * 3 // 4
                painter.drawLine(start_x, top, end_x, y)
                
            else:
                painter.setPen(QPen(QColor(color), 10, ))
                y = self.height() // 2
                painter.drawLine(start_x, y, end_x, y)

        painter.end()


class MainWindow(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Lap Time Slider")
        layout = QVBoxLayout()

        self.slider = MarkedSlider(Qt.Orientation.Horizontal)
        layout.addWidget(self.slider)
        self.setLayout(layout)

        # Example data
        base_time = 300.0
        durations = [55]
        threshold = 60.0

        self.slider.setMinimum(0)
        self.slider.setMaximum(int(base_time + sum(durations)))
        self.slider.set_lap_times_from_durations(base_time, durations, threshold)

if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = MainWindow()
    window.resize(600, 100)
    window.show()
    sys.exit(app.exec())
