from typing import Dict, TypedDict
from application.apps.myFirstWindow.myFirstWindowFunctions import*
from application.apps.mySecondWindow.mySecondWindowFunctions import*
from application.apps.myThirdWindow.myThirdWindowFunctions import*

class LogicDict(TypedDict):
    first: FirstPageLogic
    second:SecondPageLogic
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
        