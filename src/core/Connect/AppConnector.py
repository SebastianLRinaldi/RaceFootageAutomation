from src.apps.ProjectEditor.Functions import Logic as ProjecteditorLogic        
from src.apps.ProjectBaseScreen.Functions import Logic as ProjectbasescreenLogic

from src.apps.ProjectEditor.Layout import Layout as ProjecteditorLayout
from src.apps.ProjectBaseScreen.Layout import Layout as ProjectbasescreenLayout 



class AppConnector:
    projecteditor_logic: ProjecteditorLogic
    projectbasescreen_logic: ProjectbasescreenLogic

    projecteditor_ui: ProjecteditorLayout
    projectbasescreen_ui: ProjectbasescreenLayout


    def __init__(self, apps: dict, logic: dict):
        self.apps = apps
        self.logic = logic

        self.init_connections()
        # self.basic_ui.btn1.clicked.connect(self.second_logic.somefunction)

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
        