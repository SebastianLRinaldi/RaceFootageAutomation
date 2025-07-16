# from PyQt6.QtCore import *
# from PyQt6.QtWidgets import * 
# from PyQt6.QtGui import *
# from PyQt6.QtMultimedia import *
# from PyQt6.QtMultimediaWidgets import *

# import csv
# from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times
# from application.apps.mediaView.mediaViewLayout import MediaViewLayout




# LAP_TIMES_FILE = "F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv"
# RACE_NAME = "EpicX18 GT9"









# class MediaViewLogic:
#     def __init__(self, ui: MediaViewLayout):
#         self.ui = ui
#         self.offset_ms = 0
#         self.race_start_ms = None
#         self.lap_start_ms = None
#         self.lap_times = []
#         self.durations = []
#         self.current_lap_index = 0

#     def update_table_lap_time(self):
#         if self.current_lap_index < len(self.lap_times):
#             lap_time = self.durations[self.current_lap_index]
#             self.ui.myTimerKeeperView.table.insertRow(self.ui.myTimerKeeperView.table.rowCount())
#             if lap_time is not None:
#                 # Set the lap time in the table (for example, in the first row and first column)
#                 self.ui.myTimerKeeperView.table.setItem(self.current_lap_index, 0, QTableWidgetItem(str(lap_time)))  # Convert back to seconds if needed

#             else:
#                 # Handle case where lap time is None (e.g., display 'N/A' or leave it blank)
#                 self.ui.myTimerKeeperView.table.setItem(self.current_lap_index, 0, QTableWidgetItem("N/A"))

#     def on_second_video_position_changed(self, pos_ms):
#         # Update elapsed video timer
#         timestamp_ms = pos_ms
#         minutes = timestamp_ms // 60000
#         seconds = (timestamp_ms % 60000) // 1000
#         milliseconds = timestamp_ms % 1000
#         self.ui.myMediaTimeline.ElapsSecondVideoTimer.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")




#     def on_main_video_position_changed(self, pos_ms):
#         # Update elapsed video timer
#         timestamp_ms = pos_ms
#         minutes = timestamp_ms // 60000
#         seconds = (timestamp_ms % 60000) // 1000
#         milliseconds = timestamp_ms % 1000
#         self.ui.myMediaTimeline.ElapsMainVideoTimer.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")

#         # Update race timer
#         if self.race_start_ms is not None and pos_ms >= self.race_start_ms:
#             race_time_ms = pos_ms - self.race_start_ms
#             self.ui.myTimerKeeperView.RaceTimerLabel.setText(f"{race_time_ms / 1000:06.3f}")

#             # Initialize lap start on first call
#             if self.lap_start_ms is None:
#                 self.lap_start_ms = race_time_ms

#             # Check if we passed the current lap's end
#             if (race_time_ms is not None and
#                     self.current_lap_index < len(self.lap_times) and
#                     race_time_ms >= self.lap_times[self.current_lap_index]):
#                 self.update_table_lap_time()
#                 self.current_lap_index += 1
#                 self.lap_start_ms = race_time_ms # Reset lap timer

#             # Update lap timer
#             lap_time = (race_time_ms - self.lap_start_ms) / 1000
#             self.ui.myTimerKeeperView.LapTimerLabel.setText(f"{lap_time:06.3f}")
#         else:
#             self.ui.myTimerKeeperView.RaceTimerLabel.setText("00.000")
#             self.ui.myTimerKeeperView.LapTimerLabel.setText("00.000")

#     def toggle_play(self):
#         bg = self.ui.myMediaView.bgPlayer
#         overlay = self.ui.myMediaView.overlayPlayer
#         if bg.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
#             overlay.pause()
#             bg.pause()
#         else:
#             overlay.play()
#             bg.play()
            

#     def seek(self, delta_ms):
#         bg = self.ui.myMediaView.bgPlayer
#         overlay = self.ui.myMediaView.overlayPlayer
#         new_pos = max(0, bg.position() + delta_ms)
#         bg.setPosition(new_pos)
#         overlay.setPosition(max(0, new_pos + self.offset_ms))

#     def seek_main(self, pos):
#         self.ui.myMediaView.bgPlayer.pause()
#         self.ui.myMediaView.overlayPlayer.pause()
#         self.ui.myMediaView.bgPlayer.setPosition(pos)
#         self.ui.myMediaView.overlayPlayer.setPosition(max(0, pos + self.offset_ms))

#     def seek_overlay(self, pos):
#         self.ui.myMediaView.bgPlayer.pause()
#         self.ui.myMediaView.overlayPlayer.pause()
#         main_pos = self.ui.myMediaView.bgPlayer.position()
#         self.offset_ms = pos - main_pos


#         sign = "-" if self.offset_ms < 0 else ""
#         abs_ms = abs(self.offset_ms)

#         minutes = abs_ms // 60000
#         seconds = (abs_ms % 60000) // 1000
#         milliseconds = abs_ms % 1000
        
#         print(f"Offset adjusted via slider: {self.offset_ms} ms")
#         print(f"Offset adjusted via slider: {sign}{minutes:02}:{seconds:02}.{milliseconds:03}")
#         self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")

#         self.seek(0)

#     def update_main_duration(self, duration):
#         self.ui.myMediaTimeline.mainTimeline.setRange(0, duration)

#     def update_main_slider(self, position):
#         self.ui.myMediaTimeline.mainTimeline.blockSignals(True)
#         self.ui.myMediaTimeline.mainTimeline.setValue(position)
#         self.ui.myMediaTimeline.mainTimeline.blockSignals(False)

#     def update_overlay_duration(self, duration):
#         self.ui.myMediaTimeline.overlayTimeline.setRange(0, duration)
#         self.ui.mySecondViewOffsetControls.overlayTimeline.setRange(0, duration)

#     def update_overlay_slider(self, position):
#         self.ui.myMediaTimeline.overlayTimeline.blockSignals(True)
#         self.ui.myMediaTimeline.overlayTimeline.setValue(position)
#         self.ui.myMediaTimeline.overlayTimeline.blockSignals(False)

#         self.ui.mySecondViewOffsetControls.overlayTimeline.blockSignals(True)
#         self.ui.mySecondViewOffsetControls.overlayTimeline.setValue(position)
#         self.ui.mySecondViewOffsetControls.overlayTimeline.blockSignals(False)


#     def adjust_offset(self, delta):
#         self.offset_ms += delta

#         sign = "-" if self.offset_ms < 0 else ""
#         abs_ms = abs(self.offset_ms)

#         minutes = abs_ms // 60000
#         seconds = (abs_ms % 60000) // 1000
#         milliseconds = abs_ms % 1000

#         print(f"Offset: {self.offset_ms} ms")

#         print(f"Offset: {sign}{minutes:02}:{seconds:02}.{milliseconds:03}")

#         self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")


        
#         self.seek(0)

#     def step_frame(self, step):
#         frame_ms = 1000 / 60  # Accurate frame time
#         new_pos = max(0, int(self.ui.myMediaView.bgPlayer.position() + step * frame_ms))
#         self.ui.myMediaView.bgPlayer.pause()
#         self.ui.myMediaView.overlayPlayer.pause()
#         self.ui.myMediaView.bgPlayer.setPosition(new_pos)
#         self.ui.myMediaView.overlayPlayer.setPosition(max(0, new_pos + self.offset_ms))

#     def set_race_start_time(self):

#         if not self.durations:
#             self.set_lap_durations()
        
#         self.race_start_ms = self.ui.myMediaView.bgPlayer.position()
#         print(f"Race starts at {self.race_start_ms} ms")

#         pos_ms = self.ui.myMediaView.bgPlayer.position()
#         minutes = pos_ms // 60000
#         seconds = (pos_ms % 60000) // 1000
#         milliseconds = pos_ms % 1000
#         print(f"Race starts at {minutes:02}:{seconds:02}.{milliseconds:03}")
#         self.ui.myRacingTimeSetControls.currentRaceTimeStartLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")
#         self.race_start_ms = pos_ms


#     def set_lap_durations(self):
#         # durations = [24.552, 23.575, ...] in seconds
#         self.durations = get_racer_times(LAP_TIMES_FILE, RACE_NAME)
#         print(self.durations)

#         end_times = []
#         total = 0
#         for dur in self.durations:
#             if dur is not None:  # Check if the duration is not None
#                 total += dur
#                 end_times.append(int(total * 1000))  # convert to ms
#             else:
#                 end_times.append(None)  # Append None if the duration is None

#         self.lap_times = end_times
#         self.current_lap_index = 0
#         self.lap_start_ms = None


#     def manual_set_offset(self):
#         offset_ms = int(self.ui.mySecondViewOffsetControls.overlayOffsetTimeInput.text())
#         self.offset_ms = offset_ms
        

#         sign = "-" if self.offset_ms < 0 else ""
#         abs_ms = abs(self.offset_ms)

#         minutes = abs_ms // 60000
#         seconds = (abs_ms % 60000) // 1000
#         milliseconds = abs_ms % 1000

#         print(f"Offset: {self.offset_ms} ms")

#         print(f"Offset: {sign}{minutes:02}:{seconds:02}.{milliseconds:03}")

#         self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")
        
#         self.seek(0)


#     def manual_set_race_start_time(self):
#         if not self.durations:
#             self.set_lap_durations()
        
#         ms = int(self.ui.myRacingTimeSetControls.raceStartTimeInput.text())
#         self.race_start_ms = ms
#         print(f"Race starts at {self.race_start_ms} ms")

#         minutes = ms // 60000
#         seconds = (ms % 60000) // 1000
#         milliseconds = ms % 1000
#         print(f"Race starts at {minutes:02}:{seconds:02}.{milliseconds:03}")
#         self.race_start_ms = ms
        
#         self.ui.myRacingTimeSetControls.currentRaceTimeStartLabel.setText(f"{int(minutes):02}:{int(seconds):02}.{int(milliseconds):03}")



from PyQt6.QtCore import *
from PyQt6.QtWidgets import * 
from PyQt6.QtGui import *
from PyQt6.QtMultimedia import *
from PyQt6.QtMultimediaWidgets import *

import csv
from GatherRaceTimes.anaylsis_of_a_racers_times import get_racer_times
from application.apps.mediaView.mediaViewLayout import MediaViewLayout

LAP_TIMES_FILE = "F:\\_Small\\344 School Python\\TrackFootageEditor\\RaceStorage\\(6-20-25)-R2\\lap_times(6-20-25)-R2.csv"
RACE_NAME = "EpicX18 GT9"
FRAME_RATE = 60

def time_to_frame(seconds):
    return int(seconds * FRAME_RATE)

def frame_to_time(frames):
    return frames / FRAME_RATE

def ms_to_frame(ms):
    return int(ms * FRAME_RATE / 1000)

def frame_to_ms(frame):
    return int(frame * 1000 / FRAME_RATE)

class MediaViewLogic:
    def __init__(self, ui: MediaViewLayout):
        self.ui = ui
        self.offset_frames = 0
        self.race_start_frame = None
        self.lap_start_frame = None
        self.lap_times = []
        self.durations = []
        self.current_lap_index = 0

    def update_table_lap_time(self):
        if self.current_lap_index < len(self.durations):
            lap_time = self.durations[self.current_lap_index]
            self.ui.myTimerKeeperView.table.insertRow(self.ui.myTimerKeeperView.table.rowCount())
            if lap_time is not None:
                self.ui.myTimerKeeperView.table.setItem(self.current_lap_index, 0, QTableWidgetItem(f"{lap_time:.3f}"))
            else:
                self.ui.myTimerKeeperView.table.setItem(self.current_lap_index, 0, QTableWidgetItem("N/A"))

    def on_second_video_position_changed(self, pos_ms):
        frame = ms_to_frame(pos_ms)
        time_str = f"{frame_to_time(frame):06.3f}"
        self.ui.myMediaTimeline.ElapsSecondVideoTimer.setText(time_str)

    def on_main_video_position_changed(self, pos_ms):
        current_frame = ms_to_frame(pos_ms)
        if self.race_start_frame is not None and current_frame >= self.race_start_frame:
            race_frame = current_frame - self.race_start_frame
            race_time = frame_to_time(race_frame)
            self.ui.myTimerKeeperView.RaceTimerLabel.setText(f"{race_time:06.3f}")

            if self.lap_start_frame is None:
                self.lap_start_frame = race_frame

            if (self.current_lap_index < len(self.lap_times) and
                race_frame >= self.lap_times[self.current_lap_index]):
                self.update_table_lap_time()
                self.current_lap_index += 1
                self.lap_start_frame = race_frame

            lap_time = frame_to_time(race_frame - self.lap_start_frame)
            self.ui.myTimerKeeperView.LapTimerLabel.setText(f"{lap_time:06.3f}")
        else:
            self.ui.myTimerKeeperView.RaceTimerLabel.setText("00.000")
            self.ui.myTimerKeeperView.LapTimerLabel.setText("00.000")

    def toggle_play(self):
        bg = self.ui.myMediaView.bgPlayer
        overlay = self.ui.myMediaView.overlayPlayer
        if bg.playbackState() == QMediaPlayer.PlaybackState.PlayingState:
            overlay.pause()
            bg.pause()
        else:
            overlay.play()
            bg.play()

    def seek(self, delta_frames):
        bg = self.ui.myMediaView.bgPlayer
        overlay = self.ui.myMediaView.overlayPlayer
        delta_ms = frame_to_ms(delta_frames)
        new_pos = max(0, bg.position() + delta_ms)
        bg.setPosition(new_pos)
        overlay.setPosition(max(0, new_pos + frame_to_ms(self.offset_frames)))

    def seek_main(self, pos_ms):
        self.ui.myMediaView.bgPlayer.pause()
        self.ui.myMediaView.overlayPlayer.pause()
        self.ui.myMediaView.bgPlayer.setPosition(pos_ms)
        self.ui.myMediaView.overlayPlayer.setPosition(max(0, pos_ms + frame_to_ms(self.offset_frames)))

    def seek_overlay(self, pos_ms):
        self.ui.myMediaView.bgPlayer.pause()
        self.ui.myMediaView.overlayPlayer.pause()
        main_pos = self.ui.myMediaView.bgPlayer.position()
        self.offset_frames = ms_to_frame(pos_ms - main_pos)

        offset_str = f"{frame_to_time(abs(self.offset_frames)):06.3f}"
        self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(offset_str)

        self.seek(0)

    def update_main_duration(self, duration_ms):
        self.ui.myMediaTimeline.mainTimeline.setRange(0, duration_ms)

    def update_main_slider(self, position_ms):
        self.ui.myMediaTimeline.mainTimeline.blockSignals(True)
        self.ui.myMediaTimeline.mainTimeline.setValue(position_ms)
        self.ui.myMediaTimeline.mainTimeline.blockSignals(False)

    def update_overlay_duration(self, duration_ms):
        self.ui.myMediaTimeline.overlayTimeline.setRange(0, duration_ms)
        self.ui.mySecondViewOffsetControls.overlayTimeline.setRange(0, duration_ms)

    def update_overlay_slider(self, position_ms):
        self.ui.myMediaTimeline.overlayTimeline.blockSignals(True)
        self.ui.myMediaTimeline.overlayTimeline.setValue(position_ms)
        self.ui.myMediaTimeline.overlayTimeline.blockSignals(False)

        self.ui.mySecondViewOffsetControls.overlayTimeline.blockSignals(True)
        self.ui.mySecondViewOffsetControls.overlayTimeline.setValue(position_ms)
        self.ui.mySecondViewOffsetControls.overlayTimeline.blockSignals(False)

    def adjust_offset(self, delta_frames):
        self.offset_frames += delta_frames
        offset_str = f"{frame_to_time(abs(self.offset_frames)):06.3f}"
        self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(offset_str)
        self.seek(0)

    def step_frame(self, step):
        current_ms = self.ui.myMediaView.bgPlayer.position()
        current_frame = ms_to_frame(current_ms)
        new_frame = max(0, current_frame + step)
        new_pos = frame_to_ms(new_frame)
        self.ui.myMediaView.bgPlayer.pause()
        self.ui.myMediaView.overlayPlayer.pause()
        self.ui.myMediaView.bgPlayer.setPosition(new_pos)
        self.ui.myMediaView.overlayPlayer.setPosition(max(0, new_pos + frame_to_ms(self.offset_frames)))

    def set_race_start_time(self):
        if not self.durations:
            self.set_lap_durations()
        pos_ms = self.ui.myMediaView.bgPlayer.position()
        self.race_start_frame = ms_to_frame(pos_ms)
        self.ui.myRacingTimeSetControls.currentRaceTimeStartLabel.setText(f"{frame_to_time(self.race_start_frame):06.3f}")

    def set_lap_durations(self):
        self.durations = get_racer_times(LAP_TIMES_FILE, RACE_NAME)
        end_times = []
        total = 0
        for dur in self.durations:
            if dur is not None:
                total += dur
                end_times.append(time_to_frame(total))
            else:
                end_times.append(None)
        self.lap_times = end_times
        self.current_lap_index = 0
        self.lap_start_frame = None

    def manual_set_offset(self):
        offset_val = float(self.ui.mySecondViewOffsetControls.overlayOffsetTimeInput.text())
        self.offset_frames = time_to_frame(offset_val)
        self.ui.mySecondViewOffsetControls.currentOffsetTimeLabel.setText(f"{frame_to_time(self.offset_frames):06.3f}")
        self.seek(0)

    def manual_set_race_start_time(self):
        start_val = float(self.ui.myRacingTimeSetControls.raceStartTimeInput.text())
        self.race_start_frame = time_to_frame(start_val)
        self.ui.myRacingTimeSetControls.currentRaceTimeStartLabel.setText(f"{frame_to_time(self.race_start_frame):06.3f}")
