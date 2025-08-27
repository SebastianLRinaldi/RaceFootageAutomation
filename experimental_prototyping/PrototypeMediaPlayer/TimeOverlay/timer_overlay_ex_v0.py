import sys
import os
import sys
from PyQt6 import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtMultimediaWidgets import *
from PyQt6.QtCore import *


# class VideoOverlay(QGraphicsView):
#     def __init__(self, parent=None):
#         super().__init__(parent)

#         self.scene = QGraphicsScene(self)
#         self.setScene(self.scene)

#         self.mediaPlayer = QMediaPlayer()
#         self.videoItem = QGraphicsVideoItem()
#         self.scene.addItem(self.videoItem)
#         self.mediaPlayer.setVideoOutput(self.videoItem)

#         #create overlay rectangle
#         self.overlay = QGraphicsRectItem(0, 0, 100, 50, self.videoItem)
#         self.overlay.setBrush(QBrush(QColor(255, 0, 0, 128))) # Semi-transparent red

#         self.mediaPlayer.setSource(QUrl.fromLocalFile("video_only.mp4")) # Replace with your video path
#         self.mediaPlayer.play()

# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     player = VideoOverlay()
#     player.show()
#     sys.exit(app.exec())


file = 'main_overlay.mp4'
import sys
from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

class VideoOverlay(QGraphicsView):
    def __init__(self, parent=None):
        super().__init__(parent)

        # Setup scene and video player
        self.scene = QGraphicsScene(self)
        self.setScene(self.scene)

        # Media player and video item setup
        self.mediaPlayer = QMediaPlayer()
        self.videoItem = QGraphicsVideoItem()
        self.scene.addItem(self.videoItem)
        self.mediaPlayer.setVideoOutput(self.videoItem)

        # Create overlay rectangle
        self.overlay = QGraphicsRectItem(0, 0, 250, 50, self.videoItem)
        self.overlay.setBrush(QBrush(QColor(0, 0, 0, 128)))  # Semi-transparent black

        # Create text item for timer display
        self.timerText = QGraphicsTextItem(self.overlay)
        self.timerText.setDefaultTextColor(QColor(255, 255, 255))  # White text
        self.timerText.setFont(QFont('Arial', 14))

        # Set video source and start playing
        self.mediaPlayer.setSource(QUrl.fromLocalFile(file))  # Replace with your video path
        self.mediaPlayer.play()

        # Connect to frame updates using video sink
        self.sink = self.videoItem.videoSink()
        self.sink.videoFrameChanged.connect(self.on_frame_changed)

        # High-resolution timer for more accurate position tracking
        self.elapsedTimer = QElapsedTimer()
        self.elapsedTimer.start()

    def on_frame_changed(self, frame: QVideoFrame):
        # Get the timestamp of the current frame in microseconds
        timestamp = frame.startTime() / 1e6  # Convert to seconds
        
        # Update the overlay text with the timestamp
        time_str = f"{timestamp:06.3f}"  # Show time in seconds with millisecond precision
        self.timerText.setPlainText(time_str)

    def update_time(self, current_time_ms):
        # Not needed anymore with frame-based updates, keeping for reference if necessary
        pass

if __name__ == '__main__':
    app = QApplication(sys.argv)
    player = VideoOverlay()
    player.show()
    sys.exit(app.exec())


