import json
import os

def load_config(config_path):
    if not os.path.exists(config_path):
        return {}
    with open(config_path, "r") as f:
        return json.load(f)

def save_config(config_path, config):
    with open(config_path, "w") as f:
        json.dump(config, f, indent=2)

def get_config_value(config_path, key, default=None):
    config = load_config(config_path)
    return config.get(key, default)

def set_config_value(config_path, key, value):
    config = load_config(config_path)
    config[key] = value
    save_config(config_path, config)

def create_config(config_path, initial_data=None, overwrite=False):
    """
    Creates a config file at config_path.
    - initial_data: dict with default keys/values
    - overwrite: if True, will overwrite existing file
    """
    if os.path.exists(config_path) and not overwrite:
        raise FileExistsError(f"Config already exists at {config_path}")
    
    config = initial_data or {}
    save_config(config_path, config)