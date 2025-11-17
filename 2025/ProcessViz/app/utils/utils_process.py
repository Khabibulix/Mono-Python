import pythoncom
from typing import TYPE_CHECKING

from app.ProcessGetter import ProcessGetter
from app.setup_log import setup_logger

if TYPE_CHECKING:
    from app.ProcessAnalyzer import ProcessAnalyzer

logger = setup_logger(__name__)

WHITELIST = {"explorer.exe", "python.exe", "cmd.exe"}


async def fetch_and_analyze(pid: int):
    pythoncom.CoInitialize()
    try:
        logger.info("Analyzing process PID=%d", pid)
        infos = await ProcessGetter.get_infos_for_process_with_pid(pid)
        if not infos:
            logger.warning("Process PID=%d not found", pid)
            return None, None
        analyzer = ProcessAnalyzer(pid)
        result = await analyzer.run()
        return infos, result
    finally:
        pythoncom.CoUninitialize()
