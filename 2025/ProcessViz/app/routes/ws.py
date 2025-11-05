import asyncio
import json
from quart import Blueprint, websocket, current_app
from app.setup_log import setup_logger

ws_bp = Blueprint("ws", __name__)
logger = setup_logger(__name__)


@ws_bp.websocket("/ws")
async def process_stream():
    logger.info("Client connected via WebSocket")

    try:
        while True:
            cache = current_app.config.get("PROCESS_CACHE")

            if not cache:
                await websocket.send(json.dumps({"status": "loading", "data": []}))
                await asyncio.sleep(2)
                continue

            top = sorted(
                cache.items(),
                key=lambda item: float(item[1].get("memory_percent", 0) or 0),
                reverse=True,
            )[:10]

            light_cache = {
                name: {
                    "Name": proc.get("name"),
                    "PID": proc.get("PID"),
                    "Memory Usage": proc.get("memory_percent"),
                    "Status": proc.get("status"),
                    "Time Alive": proc.get("time_alive"),
                }
                for name, proc in top
            }

            data = {"status": "ok", "data": light_cache}
            await websocket.send(json.dumps(data))
            await asyncio.sleep(5)

    except Exception as e:
        logger.warning("WebSocket connection closed or errored: %s", e)
