from PyQt6.QtCore import *
from PyQt6.QtGui import *
from PyQt6.QtWidgets import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *
import sys

file1 = 'video_only.MP4'   # Background video
file2 = 'E:\\DCIM\\103GOPRO\\GOPR2567.MP4'   # Overlay video



# class DualVideoOverlay(QGraphicsView):
#     def __init__(self):
#         super().__init__()
#         self.scene = QGraphicsScene()
#         self.setScene(self.scene)

#         # Background video
#         self.bgPlayer = QMediaPlayer()
#         self.bgItem = QGraphicsVideoItem()
#         self.scene.addItem(self.bgItem)
#         self.bgPlayer.setVideoOutput(self.bgItem)

#         # Overlay video
#         self.overlayPlayer = QMediaPlayer()
#         self.overlayItem = QGraphicsVideoItem()
#         self.overlayItem.setZValue(1)
#         # self.overlayItem.setPos(20, 20)  # Top-left corner
#         self.overlayItem.setScale(0.6)  # Resize smaller
#         self.scene.addItem(self.overlayItem)
#         self.overlayPlayer.setVideoOutput(self.overlayItem)

#         # Set sources
#         self.bgPlayer.setSource(QUrl.fromLocalFile(file1))
#         self.overlayPlayer.setSource(QUrl.fromLocalFile(file2))

#         self.bgAudio = QAudioOutput()
#         self.overlayAudio = QAudioOutput()
#         self.bgPlayer.setAudioOutput(self.bgAudio)
#         self.overlayPlayer.setAudioOutput(self.overlayAudio)


        
#         # Start both
#         self.bgPlayer.play()
#         self.overlayPlayer.play()

#     def resizeEvent(self, event):
#         # Resize background video to fill the view
#         self.bgItem.setSize(QSizeF(self.viewport().width(), self.viewport().height()))
#         super().resizeEvent(event)



# class DualVideoOverlayWidget(QWidget):
#     def __init__(self):
#         super().__init__()

#         self.view = DualVideoOverlay()

#         # Playback buttons
#         self.playBtn = QPushButton("Play/Pause")
#         self.skipFwdBtn = QPushButton(">> 5s")
#         self.skipBackBtn = QPushButton("<< 5s")

#         # Layout setup
#         layout = QVBoxLayout()
#         layout.addWidget(self.view)
#         btnLayout = QHBoxLayout()
#         btnLayout.addWidget(self.skipBackBtn)
#         btnLayout.addWidget(self.playBtn)
#         btnLayout.addWidget(self.skipFwdBtn)
#         layout.addLayout(btnLayout)
#         self.setLayout(layout)

#         # Connect buttons
#         self.playBtn.clicked.connect(self.toggle_play)
#         self.skipFwdBtn.clicked.connect(lambda: self.seek(5000))
#         self.skipBackBtn.clicked.connect(lambda: self.seek(-5000))

#     def toggle_play(self):
#         bg = self.view.bgPlayer
#         overlay = self.view.overlayPlayer
#         if bg.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
#             bg.pause()
#             overlay.pause()
#         else:
#             bg.play()
#             overlay.play()

#     def seek(self, delta_ms):
#         bg = self.view.bgPlayer
#         overlay = self.view.overlayPlayer
#         new_pos = max(0, bg.position() + delta_ms)
#         bg.setPosition(new_pos)
#         overlay.setPosition(new_pos)


# if __name__ == '__main__':
#     app = QApplication(sys.argv)
#     win = DualVideoOverlayWidget()
#     win.resize(1280, 800)
#     win.show()
#     sys.exit(app.exec())



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
        self.overlayItem.setScale(0.6)
        self.scene.addItem(self.overlayItem)
        self.overlayPlayer.setVideoOutput(self.overlayItem)

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

    def resizeEvent(self, event):
        self.bgItem.setSize(QSizeF(self.viewport().width(), self.viewport().height()))
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
