from application.apps.myFirstWindow.myFirstWindowFunctions import*

class FirstPageConnections:
    def __init__(self, ui: My_First_Page, logic: FirstPageLogic):
        self.ui = ui
        self.logic = logic
        
        # Connect to frame updates using video sink
        # self.ui.bgVideoItem.videoSink().videoFrameChanged.connect(self.logic.on_frame_changed)


        self.ui.bgPlayer.positionChanged.connect(self.logic.on_position_changed)



        

        self.ui.playBtn.clicked.connect(self.logic.toggle_play)
        self.ui.skipFwdBtn.clicked.connect(lambda: self.logic.seek(5000))
        self.ui.skipBackBtn.clicked.connect(lambda: self.logic.seek(-5000))
        self.ui.offsetFwdBtn.clicked.connect(lambda: self.logic.adjust_offset(100))
        self.ui.offsetBackBtn.clicked.connect(lambda: self.logic.adjust_offset(-100))
        self.ui.stepFwdBtn.clicked.connect(lambda: self.logic.step_frame(1))
        self.ui.stepBackBtn.clicked.connect(lambda: self.logic.step_frame(-1))

        self.ui.mainTimeline.sliderMoved.connect(self.logic.seek_main)
        self.ui.overlayTimeline.sliderMoved.connect(self.logic.seek_overlay)

        self.ui.bgPlayer.durationChanged.connect(self.logic.update_main_duration)
        self.ui.bgPlayer.positionChanged.connect(self.logic.update_main_slider)

        self.ui.overlayPlayer.durationChanged.connect(self.logic.update_overlay_duration)
        self.ui.overlayPlayer.positionChanged.connect(self.logic.update_overlay_slider)
