from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

from application.apps.myFirstWindow.myFirstWindowLayout import My_First_Page

class FirstPageLogic:
    def __init__(self, ui: My_First_Page):
        self.ui = ui
        self.offset_ms = 0

    def on_frame_changed(self, frame: QVideoFrame):
        # Get the timestamp of the current frame in microseconds
        timestamp = frame.startTime() / 1e6  # Convert to seconds
        
        # Update the overlay text with the timestamp
        time_str = f"{timestamp:06.3f}"  # Show time in seconds with millisecond precision
        self.ui.ElapsVideoTimer.setText(time_str)

    def on_position_changed(self, pos_ms):
        timestamp = pos_ms / 1000  # float, keep the ms
        time_str = f"{timestamp:06.3f}"  # match precision
        self.ui.ElapsVideoTimer.setText(time_str)

    def toggle_play(self):
        bg = self.ui.bgPlayer
        overlay = self.ui.overlayPlayer
        if bg.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            bg.pause()
            overlay.pause()
        else:
            bg.play()
            overlay.play()

    def seek(self, delta_ms):
        bg = self.ui.bgPlayer
        overlay = self.ui.overlayPlayer
        new_pos = max(0, bg.position() + delta_ms)
        bg.setPosition(new_pos)
        overlay.setPosition(max(0, new_pos + self.offset_ms))

    def seek_main(self, pos):
        self.ui.bgPlayer.pause()
        self.ui.overlayPlayer.pause()
        self.ui.bgPlayer.setPosition(pos)
        self.ui.overlayPlayer.setPosition(max(0, pos + self.offset_ms))

    def seek_overlay(self, pos):
        self.ui.overlayPlayer.pause()
        main_pos = self.ui.bgPlayer.position()
        self.offset_ms = pos - main_pos
        print(f"Offset adjusted via slider: {self.offset_ms} ms")
        self.seek(0)

    def update_main_duration(self, duration):
        self.ui.mainTimeline.setRange(0, duration)

    def update_main_slider(self, position):
        self.ui.mainTimeline.blockSignals(True)
        self.ui.mainTimeline.setValue(position)
        self.ui.mainTimeline.blockSignals(False)

    def update_overlay_duration(self, duration):
        self.ui.overlayTimeline.setRange(0, duration)

    def update_overlay_slider(self, position):
        self.ui.overlayTimeline.blockSignals(True)
        self.ui.overlayTimeline.setValue(position)
        self.ui.overlayTimeline.blockSignals(False)

    def adjust_offset(self, delta):
        self.offset_ms += delta
        print(f"Offset: {self.offset_ms} ms")
        self.seek(0)

    def step_frame(self, step):
        frame_ms = 1000 // 30  # Assuming 30 FPS
        new_pos = max(0, self.ui.bgPlayer.position() + step * frame_ms)
        self.ui.bgPlayer.pause()
        self.ui.overlayPlayer.pause()
        self.ui.bgPlayer.setPosition(new_pos)
        self.ui.overlayPlayer.setPosition(max(0, new_pos + self.offset_ms))
        