from .Functions import*

class Connections:
    def __init__(self, ui: Layout, logic: Logic):
        self.ui = ui
        self.logic = logic
        
        self.ui.start_page_btn.clicked.connect(
            lambda: self.logic.load_url("https://open.spotify.com/embed/playlist/37i9dQZEVXcRbPtT6vrrSL")
            )
        
        self.ui.disable_element_btn.clicked.connect(
            lambda: self.logic.disable_element("/html/body/div/div/div/div[4]")
            )
        
        self.ui.inject_css_btn.clicked.connect(
            lambda:self.logic.inject_css("/html/body")
            )
        
        self.ui.highlight_elm_btn.clicked.connect(
            lambda:self.logic.highlight_element("/html/body/div/div/div/div[1]/div[1]/div")
            )
        
        self.ui.design_mode_btn.clicked.connect(
            self.logic.activate_design_mode
            )
        
        self.ui.devtools_btn.clicked.connect(
            self.logic.activate_devtools
            )
        
        self.ui.change_url_btn.clicked.connect(
            self.logic.change_url
            )
        