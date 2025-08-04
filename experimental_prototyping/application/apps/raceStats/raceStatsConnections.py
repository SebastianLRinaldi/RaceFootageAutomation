from application.apps.raceStats.raceStatsFunctions import*

class RaceStatsConnections:
    def __init__(self, ui: RaceStatsLayout, logic: RaceStatsLogic):
        self.ui = ui
        self.logic = logic
        
        self.ui.save_button.clicked.connect(lambda: self.logic.process_and_save(self.ui.text_area.toHtml()))