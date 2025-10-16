import json, os

def load_config(path="config.json"):
    with open(path, "r") as f:
        return json.load(f)

CONFIG = load_config()