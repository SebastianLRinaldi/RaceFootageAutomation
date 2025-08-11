import os
from src.helper_functions import *

class ProjectDirectory():
    
    def __init__(self):
        self.project_name: str = ""
        self.project_path: str = ""
        self.module_path: str = ""
        
        self.config_path: str = ""
        self.lap_times: list = []
        self.lap_times_csv = None

        self.rendered_path : str = ""
        self.asset_path: str = ""

    def __str__(self):
        attrs = vars(self)
        return "\n".join(f"{key}: {value}" for key, value in attrs.items())

    def set_up_directory(self, project_name: str, project_path: str, module_path: str):
        self.project_name = project_name
        self.project_path = project_path
        self.module_path = module_path

        self.config_path = os.path.join(self.project_path, f"{self.project_name}.json")
        self.update_lap_times()

        self.rendered_path = os.path.join(self.module_path, "rendered")
        
        self.asset_path: str = os.path.join(self.module_path, "assets")

    def update_lap_times(self):
        self.lap_times_csv = get_config_value(self.config_path, "lap_time_csv")
        self.lap_times = get_config_value(self.config_path, "lap_time_list")
        

    def make_asset_path(self, filename: str) -> str:
        if not os.path.exists(self.asset_path):
            os.makedirs(self.asset_path, exist_ok=True)
        return os.path.join(self.asset_path, filename)

    def make_rendered_path(self, filename: str) -> str:
        if not os.path.exists(self.rendered_path):
            os.makedirs(self.rendered_path, exist_ok=True)
        return os.path.join(self.rendered_path, filename)
