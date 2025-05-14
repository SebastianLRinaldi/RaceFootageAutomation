from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

import csv
from anaylsis_of_a_racers_times import get_racer_times
from application.apps.myFirstWindow.myFirstWindowLayout import My_First_Page

class FirstPageLogic:
    def __init__(self, ui: My_First_Page):
        self.ui = ui
        self.offset_ms = 0
        self.race_start_ms = None
        self.lap_start_ms = None
        self.lap_times = []
        self.durations = []
        self.current_lap_index = 0

    # def on_position_changed(self, pos_ms):
    #     timestamp = pos_ms / 1000  # float, keep the ms
    #     time_str = f"{timestamp:06.3f}"  # match precision
    #     self.ui.ElapsVideoTimer.setText(time_str)

    #     # Race timer
    #     if self.race_start_ms is not None and pos_ms >= self.race_start_ms:
    #         race_time = (pos_ms - self.race_start_ms) / 1000
    #         race_str = f"{race_time:06.3f}"
    #         self.ui.RaceTimerLabel.setText(race_str)
    #     else:
    #         self.ui.RaceTimerLabel.setText("00.000")



    def update_table_lap_time(self):
        if self.current_lap_index < len(self.lap_times):
            lap_time = self.durations[self.current_lap_index]
            self.ui.table.insertRow(self.ui.table.rowCount())
            if lap_time is not None:
                # Set the lap time in the table (for example, in the first row and first column)
                self.ui.table.setItem(self.current_lap_index, 0, QTableWidgetItem(str(lap_time)))  # Convert back to seconds if needed

            else:
                # Handle case where lap time is None (e.g., display 'N/A' or leave it blank)
                self.ui.table.setItem(self.current_lap_index, 0, QTableWidgetItem("N/A"))



    def on_position_changed(self, pos_ms):
        # Update elapsed video timer
        timestamp = pos_ms / 1000
        self.ui.ElapsVideoTimer.setText(f"{timestamp:06.3f}")

        # Update race timer
        if self.race_start_ms is not None and pos_ms >= self.race_start_ms:
            race_time_ms = pos_ms - self.race_start_ms
            self.ui.RaceTimerLabel.setText(f"{race_time_ms / 1000:06.3f}")

            # Initialize lap start on first call
            if self.lap_start_ms is None:
                self.lap_start_ms = race_time_ms

            # Check if we passed the current lap's end
            if (self.current_lap_index < len(self.lap_times) and
                    race_time_ms >= self.lap_times[self.current_lap_index]):
                self.current_lap_index += 1
                self.update_table_lap_time()
                self.lap_start_ms = race_time_ms  # Reset lap timer

            # Update lap timer
            lap_time = (race_time_ms - self.lap_start_ms) / 1000
            self.ui.LapTimerLabel.setText(f"{lap_time:06.3f}")
        else:
            self.ui.RaceTimerLabel.setText("00.000")
            self.ui.LapTimerLabel.setText("00.000")

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

    def set_race_start_time(self):
        self.race_start_ms = self.ui.bgPlayer.position()
        print(f"Race starts at {self.race_start_ms} ms")


    def set_lap_durations(self):
        # durations = [24.552, 23.575, ...] in seconds
        self.durations = get_racer_times('lap_times.csv', 'EpicX18 GT9')
        print(self.durations)

        end_times = []
        total = 0
        for dur in self.durations:
            if dur is not None:  # Check if the duration is not None
                total += dur
                end_times.append(int(total * 1000))  # convert to ms
            else:
                end_times.append(None)  # Append None if the duration is None

        self.lap_times = end_times
        self.current_lap_index = 0
        self.lap_start_ms = None



    def manual_set_offset(self):
        offset_ms = int(self.ui.overlayOffsetTimeInput.text())
        self.offset_ms = offset_ms
        print(f"Offset: {self.offset_ms} ms")
        self.seek(0)


    def manual_set_race_start_time(self):
        ms = int(self.ui.raceStartTimeInput.text())
        self.race_start_ms = ms
        print(f"Race starts at {self.race_start_ms} ms")