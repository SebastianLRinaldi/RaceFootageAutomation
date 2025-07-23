from src.apps.Basic.Functions import Logic as BasicLogic
from src.apps.Web.Functions import Logic as WebLogic
from src.apps.Second.Functions import Logic as SecondLogic
from src.apps.GatherRaceTimes.Functions import Logic as GatherracetimesLogic      
from src.apps.MakeMergedFootage.Functions import Logic as MakemergedfootageLogic  
from src.apps.MakeSegmentOverlay.Functions import Logic as MakesegmentoverlayLogic
from src.apps.MakeStreamViewer.Functions import Logic as MakestreamviewerLogic    
from src.apps.MakeTableOverlay.Functions import Logic as MaketableoverlayLogic    
from src.apps.MakeTelemOverlay.Functions import Logic as MaketelemoverlayLogic
from src.apps.MakeTimerOverlay.Functions import Logic as MaketimeroverlayLogic

from src.apps.Basic.Layout import Layout as BasicLayout
from src.apps.Web.Layout import Layout as WebLayout
from src.apps.Second.Layout import Layout as SecondLayout
from src.apps.GatherRaceTimes.Layout import Layout as GatherracetimesLayout
from src.apps.MakeMergedFootage.Layout import Layout as MakemergedfootageLayout
from src.apps.MakeSegmentOverlay.Layout import Layout as MakesegmentoverlayLayout
from src.apps.MakeStreamViewer.Layout import Layout as MakestreamviewerLayout
from src.apps.MakeTableOverlay.Layout import Layout as MaketableoverlayLayout
from src.apps.MakeTelemOverlay.Layout import Layout as MaketelemoverlayLayout
from src.apps.MakeTimerOverlay.Layout import Layout as MaketimeroverlayLayout



class AppConnector:
    basic_logic: BasicLogic
    web_logic: WebLogic
    second_logic: SecondLogic
    gatherracetimes_logic: GatherracetimesLogic
    makemergedfootage_logic: MakemergedfootageLogic
    makesegmentoverlay_logic: MakesegmentoverlayLogic
    makestreamviewer_logic: MakestreamviewerLogic
    maketableoverlay_logic: MaketableoverlayLogic
    maketelemoverlay_logic: MaketelemoverlayLogic
    maketimeroverlay_logic: MaketimeroverlayLogic

    basic_ui: BasicLayout
    web_ui: WebLayout
    second_ui: SecondLayout
    gatherracetimes_ui: GatherracetimesLayout
    makemergedfootage_ui: MakemergedfootageLayout
    makesegmentoverlay_ui: MakesegmentoverlayLayout
    makestreamviewer_ui: MakestreamviewerLayout
    maketableoverlay_ui: MaketableoverlayLayout
    maketelemoverlay_ui: MaketelemoverlayLayout
    maketimeroverlay_ui: MaketimeroverlayLayout

    def __init__(self, apps: dict, logic: dict):
        self.apps = apps
        self.logic = logic

        self.init_connections()
        self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)

    """
    This basically just does this part for us:
    
    class AppConnector:
        basic_ui: BasicLayout
        second_logic: SecondLogic

        def __init__(self, apps, logic):
            self.basic_ui = apps["Basic"]
            self.second_logic = logic["Second"]

            self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)
    """
    def init_connections(self):
        for name in self.apps:
            setattr(self, f"{name.lower()}_ui", self.apps[name])
            setattr(self, f"{name.lower()}_logic", self.logic[name])








# class AppConnector:
#     basic_logic: BasicLogic
#     second_logic:SecondLogic
#     web_logic: WebLogic

#     basic_ui: BasicLayout
#     second_logic:SecondLayout
#     web_logic: WebLayout
    
#     def __init__(self, ):



#         self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)

#         self.logic["Basic"].ui.update_widget_btn.clicked.connect(
#             self.logic["Second"].update_widget
#         )

#         # self.logic["Basic"].ui.reset_widget_btn.clicked.connect(
#         #     lambda: self.logic["Second"].ui.name_label.setText("Updated Another Way")
#         # )
        