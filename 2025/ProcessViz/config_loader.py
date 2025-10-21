import json, os, aiofiles

config_path = os.path.join(os.path.dirname(__file__), "config.json")

async def load_config():
    async with aiofiles.open(config_path, "r", encoding='utf-8') as f:
        content = await f.read()
        return json.load(content)

CONFIG = load_config()