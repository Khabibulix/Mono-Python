from app.setup_log import setup_logger
from app.utils.utils_score import compute_score

logger = setup_logger()


class ProcessAnalyzer:
    def __init__(self, pid: int, mode: str = "full"):
        self.pid = pid
        self.mode = mode
        self.analysis = None

    async def run(self):
        try:
            self.analysis = await compute_score(self.pid, mode=self.mode)
            return self.analysis
        except Exception:
            logger.exception(f"Error analyzing process PID: {self.pid}")
            return None
