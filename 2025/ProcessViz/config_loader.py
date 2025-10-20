import json, os

config_path = os.path.join(os.path.dirname(__file__), "config.json")

def load_config():
    with open(config_path, "r", encoding='utf-8') as f:
        return json.load(f)

CONFIG = load_config()