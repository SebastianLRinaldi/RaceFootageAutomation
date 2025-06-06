from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

import csv
from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times
from application.apps.mediaView.mediaViewLayout import MediaViewLayout

class MediaViewLogic:
    def __init__(self, ui: MediaViewLayout):
        self.ui = ui
        self.offset_ms = 0
        self.race_start_ms = None
        self.lap_start_ms = None
        self.lap_times = []
        self.durations = []
        self.current_lap_index = 0

    def update_table_lap_time(self):
        if self.current_lap_index < len(self.lap_times):
            lap_time = self.durations[self.current_lap_index]
            self.ui.myTimerKeeperView.table.insertRow(self.ui.myTimerKeeperView.table.rowCount())
            if lap_time is not None:
                # Set the lap time in the table (for example, in the first row and first column)
                self.ui.myTimerKeeperView.table.setItem(self.current_lap_index, 0, QTableWidgetItem(str(lap_time)))  # Convert back to seconds if needed

            else:
                # Handle case where lap time is None (e.g., display 'N/A' or leave it blank)
                self.ui.myTimerKeeperView.table.setItem(self.current_lap_index, 0, QTableWidgetItem("N/A"))

    def on_second_video_position_changed(self, pos_ms):
        # Update elapsed video timer
        timestamp_ms = pos_ms
        minutes = timestamp_ms // 60000
        seconds = (timestamp_ms % 60000) // 1000
        milliseconds = timestamp_ms % 1000
        self.ui.myMediaTimeline.ElapsSecondVideoTimer.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")




    def on_main_video_position_changed(self, pos_ms):
        # Update elapsed video timer
        timestamp_ms = pos_ms
        minutes = timestamp_ms // 60000
        seconds = (timestamp_ms % 60000) // 1000
        milliseconds = timestamp_ms % 1000
        self.ui.myMediaTimeline.ElapsMainVideoTimer.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")

        # Update race timer
        if self.race_start_ms is not None and pos_ms >= self.race_start_ms:
            race_time_ms = pos_ms - self.race_start_ms
            self.ui.myTimerKeeperView.RaceTimerLabel.setText(f"{race_time_ms / 1000:06.3f}")

            # Initialize lap start on first call
            if self.lap_start_ms is None:
                self.lap_start_ms = race_time_ms

            # Check if we passed the current lap's end
            if (race_time_ms is not None and
                    self.current_lap_index < len(self.lap_times) and
                    race_time_ms >= self.lap_times[self.current_lap_index]):
                self.update_table_lap_time()
                self.current_lap_index += 1
                self.lap_start_ms = race_time_ms # Reset lap timer

            # Update lap timer
            lap_time = (race_time_ms - self.lap_start_ms) / 1000
            self.ui.myTimerKeeperView.LapTimerLabel.setText(f"{lap_time:06.3f}")
        else:
            self.ui.myTimerKeeperView.RaceTimerLabel.setText("00.000")
            self.ui.myTimerKeeperView.LapTimerLabel.setText("00.000")

    def toggle_play(self):
        bg = self.ui.myMediaView.bgPlayer
        overlay = self.ui.myMediaView.overlayPlayer
        if bg.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            bg.pause()
            overlay.pause()
        else:
            overlay.play()
            bg.play()
            

    def seek(self, delta_ms):
        bg = self.ui.myMediaView.bgPlayer
        overlay = self.ui.myMediaView.overlayPlayer
        new_pos = max(0, bg.position() + delta_ms)
        bg.setPosition(new_pos)
        overlay.setPosition(max(0, new_pos + self.offset_ms))

    def seek_main(self, pos):
        self.ui.myMediaView.bgPlayer.pause()
        self.ui.myMediaView.overlayPlayer.pause()
        self.ui.myMediaView.bgPlayer.setPosition(pos)
        self.ui.myMediaView.overlayPlayer.setPosition(max(0, pos + self.offset_ms))

    def seek_overlay(self, pos):
        self.ui.myMediaView.bgPlayer.pause()
        self.ui.myMediaView.overlayPlayer.pause()
        main_pos = self.ui.myMediaView.bgPlayer.position()
        self.offset_ms = pos - main_pos


        sign = "-" if self.offset_ms < 0 else ""
        abs_ms = abs(self.offset_ms)

        minutes = abs_ms // 60000
        seconds = (abs_ms % 60000) // 1000
        milliseconds = abs_ms % 1000
        
        print(f"Offset adjusted via slider: {self.offset_ms} ms")
        print(f"Offset adjusted via slider: {sign}{minutes:02}:{seconds:02}.{milliseconds:03}")
        self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")

        self.seek(0)

    def update_main_duration(self, duration):
        self.ui.myMediaTimeline.mainTimeline.setRange(0, duration)

    def update_main_slider(self, position):
        self.ui.myMediaTimeline.mainTimeline.blockSignals(True)
        self.ui.myMediaTimeline.mainTimeline.setValue(position)
        self.ui.myMediaTimeline.mainTimeline.blockSignals(False)

    def update_overlay_duration(self, duration):
        self.ui.myMediaTimeline.overlayTimeline.setRange(0, duration)
        self.ui.mySecondViewOffsetControls.overlayTimeline.setRange(0, duration)

    def update_overlay_slider(self, position):
        self.ui.myMediaTimeline.overlayTimeline.blockSignals(True)
        self.ui.myMediaTimeline.overlayTimeline.setValue(position)
        self.ui.myMediaTimeline.overlayTimeline.blockSignals(False)

        self.ui.mySecondViewOffsetControls.overlayTimeline.blockSignals(True)
        self.ui.mySecondViewOffsetControls.overlayTimeline.setValue(position)
        self.ui.mySecondViewOffsetControls.overlayTimeline.blockSignals(False)


    def adjust_offset(self, delta):
        self.offset_ms += delta

        sign = "-" if self.offset_ms < 0 else ""
        abs_ms = abs(self.offset_ms)

        minutes = abs_ms // 60000
        seconds = (abs_ms % 60000) // 1000
        milliseconds = abs_ms % 1000

        print(f"Offset: {self.offset_ms} ms")

        print(f"Offset: {sign}{minutes:02}:{seconds:02}.{milliseconds:03}")

        self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")


        
        self.seek(0)

    def step_frame(self, step):
        frame_ms = 1000 / 60  # Accurate frame time
        new_pos = max(0, int(self.ui.myMediaView.bgPlayer.position() + step * frame_ms))
        self.ui.myMediaView.bgPlayer.pause()
        self.ui.myMediaView.overlayPlayer.pause()
        self.ui.myMediaView.bgPlayer.setPosition(new_pos)
        self.ui.myMediaView.overlayPlayer.setPosition(max(0, new_pos + self.offset_ms))

    def set_race_start_time(self):

        if not self.durations:
            self.set_lap_durations()
        
        self.race_start_ms = self.ui.myMediaView.bgPlayer.position()
        print(f"Race starts at {self.race_start_ms} ms")

        pos_ms = self.ui.myMediaView.bgPlayer.position()
        minutes = pos_ms // 60000
        seconds = (pos_ms % 60000) // 1000
        milliseconds = pos_ms % 1000
        print(f"Race starts at {minutes:02}:{seconds:02}.{milliseconds:03}")
        self.ui.myRacingTimeSetControls.currentRaceTimeStartLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")
        self.race_start_ms = pos_ms


    def set_lap_durations(self):
        # durations = [24.552, 23.575, ...] in seconds
        self.durations = get_racer_times('Race_2_(5-30-25).csv', 'EpicX18 GT9')
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
        offset_ms = int(self.ui.mySecondViewOffsetControls.overlayOffsetTimeInput.text())
        self.offset_ms = offset_ms
        

        sign = "-" if self.offset_ms < 0 else ""
        abs_ms = abs(self.offset_ms)

        minutes = abs_ms // 60000
        seconds = (abs_ms % 60000) // 1000
        milliseconds = abs_ms % 1000

        print(f"Offset: {self.offset_ms} ms")

        print(f"Offset: {sign}{minutes:02}:{seconds:02}.{milliseconds:03}")

        self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")
        
        self.seek(0)


    def manual_set_race_start_time(self):
        if not self.durations:
            self.set_lap_durations()
        
        ms = int(self.ui.myRacingTimeSetControls.raceStartTimeInput.text())
        self.race_start_ms = ms
        print(f"Race starts at {self.race_start_ms} ms")

        minutes = ms // 60000
        seconds = (ms % 60000) // 1000
        milliseconds = ms % 1000
        print(f"Race starts at {minutes:02}:{seconds:02}.{milliseconds:03}")
        self.race_start_ms = ms
        
        self.ui.myRacingTimeSetControls.currentRaceTimeStartLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")