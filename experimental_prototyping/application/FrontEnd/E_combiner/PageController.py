from typing import Dict, TypedDict
from application.apps.mediaView.mediaViewFunctions import*
from application.apps.raceStats.raceStatsFunctions import*
from application.apps.myThirdWindow.myThirdWindowFunctions import*

class LogicDict(TypedDict):
    first: MediaViewLogic
    second:RaceStatsLogic
    third: ThirdPageLogic

class PageController:
    def __init__(self, logic: LogicDict):
        self.logic = logic

        # self.logic["first"].ui.update_widget_btn.clicked.connect(
        #     self.logic["second"].update_widget
        # )

        # self.logic["first"].ui.reset_widget_btn.clicked.connect(
        #     lambda: self.logic["second"].ui.name_label.setText("Updated Another Way")
        # )
        