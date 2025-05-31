from application.apps.myFirstWindow.myFirstWindowFunctions import*

class FirstPageConnections:
    def __init__(self, ui: My_First_Page, logic: FirstPageLogic):
        self.ui = ui
        self.logic = logic

        self.ui.myMediaView.bgPlayer.positionChanged.connect(self.logic.on_main_video_position_changed)
        self.ui.myMediaView.overlayPlayer.positionChanged.connect(self.logic.on_second_video_position_changed)
        
        self.ui.myMediaControls.playBtn.clicked.connect(self.logic.toggle_play)
        self.ui.myMediaControls.skipFwdBtn.clicked.connect(lambda: self.logic.seek(5000))
        self.ui.myMediaControls.skipBackBtn.clicked.connect(lambda: self.logic.seek(-5000))
        
        self.ui.mySecondViewOffsetControls.offsetLFwdBtn.clicked.connect(lambda: self.logic.adjust_offset(100))
        self.ui.mySecondViewOffsetControls.offsetLBackBtn.clicked.connect(lambda: self.logic.adjust_offset(-100))
        self.ui.mySecondViewOffsetControls.offsetMFwdBtn.clicked.connect(lambda: self.logic.adjust_offset(10))
        self.ui.mySecondViewOffsetControls.offsetMBackBtn.clicked.connect(lambda: self.logic.adjust_offset(-10))
        self.ui.mySecondViewOffsetControls.offsetSFwdBtn.clicked.connect(lambda: self.logic.adjust_offset(1))
        self.ui.mySecondViewOffsetControls.offsetSBackBtn.clicked.connect(lambda: self.logic.adjust_offset(-1))
        
        self.ui.myMediaControls.stepFwdBtn.clicked.connect(lambda: self.logic.step_frame(1))
        self.ui.myMediaControls.stepBackBtn.clicked.connect(lambda: self.logic.step_frame(-1))

        self.ui.myMediaTimeline.mainTimeline.sliderMoved.connect(self.logic.seek_main)
        
        self.ui.myMediaTimeline.overlayTimeline.sliderMoved.connect(self.logic.seek_overlay)
        self.ui.mySecondViewOffsetControls.overlayTimeline.sliderMoved.connect(self.logic.seek_overlay)
        
        self.ui.myMediaView.bgPlayer.durationChanged.connect(self.logic.update_main_duration)
        self.ui.myMediaView.bgPlayer.positionChanged.connect(self.logic.update_main_slider)

        self.ui.myMediaView.overlayPlayer.durationChanged.connect(self.logic.update_overlay_duration)
        self.ui.myMediaView.overlayPlayer.positionChanged.connect(self.logic.update_overlay_slider)


        self.ui.myRacingTimeSetControls.markRaceStartTime.clicked.connect(self.logic.set_race_start_time)
        self.ui.myRacingTimeSetControls.grabLapTimeDuration.clicked.connect(self.logic.set_lap_durations)

        self.ui.mySecondViewOffsetControls.setOverlayOffsetTimeBtn.clicked.connect(self.logic.manual_set_offset)
        self.ui.myRacingTimeSetControls.setRaceStartTimeBtn.clicked.connect(self.logic.manual_set_race_start_time)




        