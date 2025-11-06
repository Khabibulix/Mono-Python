import psutil, asyncio
from app.setup_log import setup_logger
from app.utils.utils_process import score_process

logger = setup_logger()
alerts_queue = asyncio.Queue()


async def process_watcher(interval=2):
    old_pids = set(psutil.pids())
    while True:
        await asyncio.sleep(interval)
        new_pids = set(psutil.pids())
        started = new_pids - old_pids
        old_pids = new_pids

        for pid in started:
            try:
                proc = psutil.Process(pid)
                logger.info(
                    f"New process detected: PID={pid}, Name={proc.name()}, Path={proc.exe()}"
                )
                score = score_process(proc)
                if score > 0:
                    alert = {
                        "pid": pid,
                        "name": proc.name(),
                        "path": proc.exe(),
                        "score": score,
                    }
                    await alerts_queue.put(alert)
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                continue
