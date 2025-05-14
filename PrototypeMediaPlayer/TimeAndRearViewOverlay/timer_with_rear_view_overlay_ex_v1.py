from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
import sys

file1 = 'main_bg.mp4'   # Background video
file2 = 'main_overlay.mp4'   # Overlay video


class DualVideoOverlayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Dual Video Player with Timer & Table")

        # === Main (center) video ===
        self.bgPlayer = QMediaPlayer()
        self.bgVideoItem = QGraphicsVideoItem()
        self.bgScene = QGraphicsScene()
        self.bgScene.addItem(self.bgVideoItem)
        self.bgView = QGraphicsView(self.bgScene)
        self.bgPlayer.setVideoOutput(self.bgVideoItem)

        # === Rear (left) video ===
        self.overlayPlayer = QMediaPlayer()
        self.overlayWidget = QVideoWidget()
        self.overlayPlayer.setVideoOutput(self.overlayWidget)

        # === Timer (top right) ===
        self.timerLabel = QLabel("00:00")
        self.timerLabel.setStyleSheet("color: white; background-color: rgba(0,0,0,128); font-size: 16px;")
        self.timerLabel.setAlignment(Qt.AlignmentFlag.AlignCenter)

        # === Table (bottom right) ===
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(['Col 1', 'Col 2', 'Col 3'])
        for i in range(5):
            for j in range(3):
                self.table.setItem(i, j, QTableWidgetItem(f"Item {i},{j}"))

        # === Right side layout ===
        rightLayout = QVBoxLayout()
        rightLayout.addWidget(self.timerLabel)
        rightLayout.addWidget(self.table)

        # === Main layout: Left (rear), Center (main), Right (timer+table) ===
        mainLayout = QHBoxLayout()
        mainLayout.addWidget(self.overlayWidget)
        mainLayout.addWidget(self.bgView, stretch=2)
        mainLayout.addLayout(rightLayout)

        # === Controls ===
        self.playBtn = QPushButton("Play/Pause")
        self.timeline = QSlider(Qt.Orientation.Horizontal)
        controlsLayout = QHBoxLayout()
        controlsLayout.addWidget(self.playBtn)
        controlsLayout.addWidget(self.timeline)

        # === Final layout ===
        layout = QVBoxLayout()
        layout.addLayout(mainLayout)
        layout.addLayout(controlsLayout)
        self.setLayout(layout)

        # === Load media ===
        self.bgPlayer.setSource(QUrl.fromLocalFile(file1))
        self.overlayPlayer.setSource(QUrl.fromLocalFile(file2))

        self.bgAudio = QAudioOutput()
        self.overlayAudio = QAudioOutput()
        self.bgPlayer.setAudioOutput(self.bgAudio)
        self.overlayPlayer.setAudioOutput(self.overlayAudio)

        # === Play immediately ===
        self.bgPlayer.play()
        self.overlayPlayer.play()

        # === Connect video frame to timer update ===
        self.bgVideoItem.videoSink().videoFrameChanged.connect(self.update_timer)
        self.playBtn.clicked.connect(self.toggle_play)

    def update_timer(self, frame: QVideoFrame):
        if not frame.isValid():
            return
        timestamp = frame.startTime() / 1e6  # Convert µs to seconds
        self.timerLabel.setText(f"{timestamp:06.3f}")

    def toggle_play(self):
        if self.bgPlayer.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            self.bgPlayer.pause()
            self.overlayPlayer.pause()
        else:
            self.bgPlayer.play()
            self.overlayPlayer.play()


if __name__ == "__main__":
    app = QApplication(sys.argv)
    widget = DualVideoOverlayWidget()
    widget.resize(1200, 600)
    widget.show()
    sys.exit(app.exec())
