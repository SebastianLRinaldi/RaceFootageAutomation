

from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
import sys

file1 = 'main_bg.mp4'   # Background video
file2 = 'main_overlay.mp4'   # Overlay video


class DualVideoOverlay(QGraphicsView):
    def __init__(self):
        super().__init__()
        self.scene = QGraphicsScene()
        self.setScene(self.scene)

        # Background video
        self.bgPlayer = QMediaPlayer()
        self.bgItem = QGraphicsVideoItem()
        self.scene.addItem(self.bgItem)
        self.bgPlayer.setVideoOutput(self.bgItem)

        # Overlay video
        self.overlayPlayer = QMediaPlayer()
        self.overlayItem = QGraphicsVideoItem()
        self.overlayItem.setZValue(1)
        self.overlayItem.setScale(0.1)
        self.scene.addItem(self.overlayItem)
        self.overlayPlayer.setVideoOutput(self.overlayItem)


        # Create overlay rectangle
        self.overlay = QGraphicsRectItem(0, 0, 250, 50, self.bgItem)
        self.overlay.setBrush(QBrush(QColor(0, 0, 0, 128)))  # Semi-transparent black

        # Create text item for timer display
        self.timerText = QGraphicsTextItem(self.overlay)
        self.timerText.setDefaultTextColor(QColor(255, 255, 255))  # White text
        self.timerText.setFont(QFont('Arial', 14))
        self.timerText.setPlainText("00:00")


        
        # Table widget as overlay
        self.table = QTableWidget(5, 3)
        self.table.setHorizontalHeaderLabels(['Col 1', 'Col 2', 'Col 3'])

        # Wrap it in a proxy to add to scene
        self.tableProxy = QGraphicsProxyWidget()
        self.tableProxy.setWidget(self.table)
        self.tableProxy.setZValue(2)  # On top of videos
        self.scene.addItem(self.tableProxy)

        # Position the table on the right side of the view
        self.tableProxy.setPos(900, 100)  # Tune position as needed



        # Sources
        self.bgPlayer.setSource(QUrl.fromLocalFile(file1))
        self.overlayPlayer.setSource(QUrl.fromLocalFile(file2))

        # Audio
        self.bgAudio = QAudioOutput()
        self.overlayAudio = QAudioOutput()
        self.bgPlayer.setAudioOutput(self.bgAudio)
        self.overlayPlayer.setAudioOutput(self.overlayAudio)

        self.bgPlayer.play()
        self.overlayPlayer.play()


        # Connect to frame updates using video sink
        self.sink = self.bgItem.videoSink()
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

    def resizeEvent(self, event):
        width = self.viewport().width()
        height = self.viewport().height()

        # Main center video
        video_width = width * 0.4
        video_height = height * 0.8
        video_x = (width - video_width) / 2
        video_y = (height - video_height) / 2
        self.bgItem.setSize(QSizeF(video_width, video_height))
        self.bgItem.setPos(video_x, video_y)

        # Rear view on the left
        self.overlayItem.setPos(50, (height - self.overlayItem.boundingRect().height() * 0.1) / 2)

        # Table on the right
        table_width = self.table.sizeHint().width()
        table_height = self.table.height()
        table_x = width - table_width - 50
        table_y = (height - table_height) / 2
        self.tableProxy.setPos(table_x, table_y)

        # Timer above the table
        overlay_width = self.overlay.rect().width()
        overlay_height = self.overlay.rect().height()
        overlay_x = table_x + (table_width - overlay_width) / 2
        overlay_y = table_y - overlay_height - 10  # 10 px gap above table
        self.overlay.setPos(overlay_x, overlay_y)

        super().resizeEvent(event)




class DualVideoOverlayWidget(QWidget):
    def __init__(self):
        super().__init__()
        self.view = DualVideoOverlay()
        self.offset_ms = 0

        # Controls
        self.playBtn = QPushButton("Play/Pause")
        self.skipFwdBtn = QPushButton(">> 5s")
        self.skipBackBtn = QPushButton("<< 5s")
        self.offsetFwdBtn = QPushButton("Overlay +0.1s")
        self.offsetBackBtn = QPushButton("Overlay -0.1s")
        self.stepFwdBtn = QPushButton("Frame →")
        self.stepBackBtn = QPushButton("← Frame")

        # Timelines
        self.mainTimeline = QSlider(Qt.Orientation.Horizontal)
        self.mainTimeline.setRange(0, 1000)
        self.overlayTimeline = QSlider(Qt.Orientation.Horizontal)
        self.overlayTimeline.setRange(0, 1000)

        # Layout
        layout = QVBoxLayout()
        layout.addWidget(self.view)
        layout.addWidget(QLabel("Main Video Timeline"))
        layout.addWidget(self.mainTimeline)
        layout.addWidget(QLabel("Overlay Video Timeline"))
        layout.addWidget(self.overlayTimeline)

        btnLayout = QHBoxLayout()
        btnLayout.addWidget(self.skipBackBtn)
        btnLayout.addWidget(self.playBtn)
        btnLayout.addWidget(self.skipFwdBtn)
        btnLayout.addWidget(self.offsetBackBtn)
        btnLayout.addWidget(self.offsetFwdBtn)
        btnLayout.addWidget(self.stepBackBtn)
        btnLayout.addWidget(self.stepFwdBtn)
        layout.addLayout(btnLayout)

        self.setLayout(layout)



        

        

        # Signals
        self.playBtn.clicked.connect(self.toggle_play)
        self.skipFwdBtn.clicked.connect(lambda: self.seek(5000))
        self.skipBackBtn.clicked.connect(lambda: self.seek(-5000))
        self.offsetFwdBtn.clicked.connect(lambda: self.adjust_offset(100))
        self.offsetBackBtn.clicked.connect(lambda: self.adjust_offset(-100))
        self.stepFwdBtn.clicked.connect(lambda: self.step_frame(1))
        self.stepBackBtn.clicked.connect(lambda: self.step_frame(-1))

        self.mainTimeline.sliderMoved.connect(self.seek_main)
        self.overlayTimeline.sliderMoved.connect(self.seek_overlay)

        self.view.bgPlayer.durationChanged.connect(self.update_main_duration)
        self.view.bgPlayer.positionChanged.connect(self.update_main_slider)

        self.view.overlayPlayer.durationChanged.connect(self.update_overlay_duration)
        self.view.overlayPlayer.positionChanged.connect(self.update_overlay_slider)

    def toggle_play(self):
        bg = self.view.bgPlayer
        overlay = self.view.overlayPlayer
        if bg.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            bg.pause()
            overlay.pause()
        else:
            bg.play()
            overlay.play()

    def seek(self, delta_ms):
        bg = self.view.bgPlayer
        overlay = self.view.overlayPlayer
        new_pos = max(0, bg.position() + delta_ms)
        bg.setPosition(new_pos)
        overlay.setPosition(max(0, new_pos + self.offset_ms))

    def seek_main(self, pos):
        self.view.bgPlayer.pause()
        self.view.overlayPlayer.pause()
        self.view.bgPlayer.setPosition(pos)
        self.view.overlayPlayer.setPosition(max(0, pos + self.offset_ms))

    def seek_overlay(self, pos):
        self.view.overlayPlayer.pause()
        main_pos = self.view.bgPlayer.position()
        self.offset_ms = pos - main_pos
        print(f"Offset adjusted via slider: {self.offset_ms} ms")
        self.seek(0)

    def update_main_duration(self, duration):
        self.mainTimeline.setRange(0, duration)

    def update_main_slider(self, position):
        self.mainTimeline.blockSignals(True)
        self.mainTimeline.setValue(position)
        self.mainTimeline.blockSignals(False)

    def update_overlay_duration(self, duration):
        self.overlayTimeline.setRange(0, duration)

    def update_overlay_slider(self, position):
        self.overlayTimeline.blockSignals(True)
        self.overlayTimeline.setValue(position)
        self.overlayTimeline.blockSignals(False)

    def adjust_offset(self, delta):
        self.offset_ms += delta
        print(f"Offset: {self.offset_ms} ms")
        self.seek(0)

    def step_frame(self, step):
        frame_ms = 1000 // 30  # Assuming 30 FPS
        new_pos = max(0, self.view.bgPlayer.position() + step * frame_ms)
        self.view.bgPlayer.pause()
        self.view.overlayPlayer.pause()
        self.view.bgPlayer.setPosition(new_pos)
        self.view.overlayPlayer.setPosition(max(0, new_pos + self.offset_ms))


if __name__ == '__main__':
    app = QApplication(sys.argv)
    win = DualVideoOverlayWidget()
    win.resize(1280, 800)
    win.show()
    sys.exit(app.exec())
