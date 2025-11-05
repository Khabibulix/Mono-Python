import json, os, aiofiles

_config = None

config_path = os.path.abspath(
    os.path.join(os.path.dirname(__file__), "..", "config.json")
)


async def get_config():
    global _config
    if _config is None:
        async with aiofiles.open(config_path, "r", encoding="utf-8") as f:
            content = await f.read()
            return json.loads(content)
    return _config
