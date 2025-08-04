

file = 'E:\\DCIM\\100GOPRO\\GH022591.MP4'

import os
import sys
from PyQt6.QtWidgets import QApplication, QWidget, QPushButton, QVBoxLayout, QStyle
from PyQt6.QtMultimedia import QMediaPlayer, QAudioOutput
from PyQt6.QtMultimediaWidgets import QVideoWidget
from PyQt6.QtCore import QUrl, QTimer

class VideoPlayer(QWidget):
    def __init__(self, video_path):
        super().__init__()
        self.setWindowTitle("Video Player with Frame-by-Frame Control")

        self.media_player = QMediaPlayer(self)
        self.audio_output = QAudioOutput(self)
        self.media_player.setAudioOutput(self.audio_output)

        self.video_widget = QVideoWidget(self)
        self.media_player.setVideoOutput(self.video_widget)

        # Buttons for control
        self.play_button = QPushButton(self)
        self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        self.play_button.clicked.connect(self.toggle_play)

        self.prev_frame_button = QPushButton("⏮ Prev Frame")
        self.prev_frame_button.clicked.connect(self.prev_frame)
        self.next_frame_button = QPushButton("Next Frame ⏭")
        self.next_frame_button.clicked.connect(self.next_frame)

        layout = QVBoxLayout()
        layout.addWidget(self.video_widget)
        layout.addWidget(self.prev_frame_button)
        layout.addWidget(self.play_button)
        layout.addWidget(self.next_frame_button)
        self.setLayout(layout)

        self.media_player.setSource(QUrl.fromLocalFile(video_path))
        self.media_player.durationChanged.connect(self.duration_changed)
        self.media_player.positionChanged.connect(self.position_changed)

        # Timer to control frame steps
        self.frame_duration = 40  # Time for a single frame in milliseconds (adjust as needed)
        self.timer = QTimer(self)
        self.timer.timeout.connect(self.next_frame_step)
        self.current_position = 0

    def toggle_play(self):
        if self.media_player.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.media_player.pause()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPlay))
        else:
            self.media_player.play()
            self.play_button.setIcon(self.style().standardIcon(QStyle.StandardPixmap.SP_MediaPause))

    def prev_frame(self):
        self.current_position -= self.frame_duration
        if self.current_position < 0:
            self.current_position = 0
        self.media_player.setPosition(self.current_position)

    def next_frame(self):
        self.current_position += self.frame_duration
        if self.current_position >= self.media_player.duration():
            self.current_position = self.media_player.duration() - 1
        self.media_player.setPosition(self.current_position)

    def next_frame_step(self):
        self.current_position += self.frame_duration
        if self.current_position >= self.media_player.duration():
            self.current_position = self.media_player.duration() - 1
        self.media_player.setPosition(self.current_position)

    def duration_changed(self, duration):
        self.duration = duration

    def position_changed(self, position):
        self.current_position = position

if __name__ == "__main__":
    app = QApplication(sys.argv)
    player = VideoPlayer(file)
    player.resize(800, 450)
    player.show()
    sys.exit(app.exec())

