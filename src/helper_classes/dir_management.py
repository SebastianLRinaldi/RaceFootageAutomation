import os
from src.helper_functions import *

class ProjectDirectory():
    
    def __init__(self):
        self.project_name: str = ""
        self.project_path: str = ""
        self.module_path: str = ""
        
        self.config_path: str = ""
        self.lap_times: list = []

        self.rendered_path : str = ""
        self.asset_path: str = ""

    def set_up_directory(self, project_name: str, project_path: str, module_path: str):
        self.project_name = project_name
        self.project_path = project_path
        self.module_path = module_path

        self.config_path = os.path.join(self.project_path, f"{self.project_name}.json")
        self.update_lap_times()

        self.rendered_path = os.path.join(self.module_path, "rendered")
        
        self.asset_path: str = os.path.join(self.module_path, "assets")

    def update_lap_times(self):
        get_config_value(self.config_path, "lap_time_csv")
        self.lap_times = get_config_value(self.config_path, "lap_time_list")
        

    def make_asset_path(self, filename: str) -> str:
        return os.path.join(self.asset_path, filename)
