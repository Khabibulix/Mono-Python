import psutil, re
from app.utils.utils import is_signed, normalizing_score, analyze_score_risk
from app.utils.utils_process_helpers import is_invocating_scripts, is_deleted_executable
from app.utils.utils_services import is_process_bound_to_a_service
from app.config_loader import get_config
from app.setup_log import setup_logger

logger = setup_logger()
MAX_SCORE = 135


async def compute_score(pid: int, mode: str = "full"):
    """Compute score depending on mode:
    - light: quick mode for index page
    - full: slow and complete mode for distinct process analysis

    :param process: Process pid to analyze
    :type process: int
    :param mode: Mode of the score, speed will vary
    :type mode: str
    :return: Score, justifications and other metrics
    :rtype: dict
    """

    try:
        CONFIG = await get_config()
        if not psutil.pid_exists(pid):
            return None
        proc = psutil.Process(pid)
        exe_path = proc.exe()
        score = 0
        justifications = {}
        raw_metrics = {
            "path_suspicious": False,
            "path_trustworthy": False,
            "is_signed": True,
            "path_deleted": False,
            "strange_chars": False,
            "network_active": False,
        }

        if mode in ("light", "full"):

            # Signature
            signed = is_signed(exe_path)
            raw_metrics["is_signed"] = signed
            if not signed:
                score += CONFIG["weights"]["not_signed"]
                justifications["is_signed"] = False

            # Path
            if any(
                exe_path.startswith(path.lower())
                for path in CONFIG["paths"]["suspicious"]
            ):
                score += CONFIG["weights"]["suspicious_path"]
                justifications["path_suspicious"] = True
                raw_metrics["path_suspicious"] = True

            if any(
                exe_path.startswith(p.lower()) for p in CONFIG["paths"]["trustworthy"]
            ):
                score += CONFIG["weights"]["trustworthy_path"]
                justifications["path_trustworthy"] = True
                raw_metrics["path_trustworthy"] = True

            if is_deleted_executable(proc):
                score += CONFIG["weights"]["deleted_path"]
                justifications["path_deleted"] = True
                raw_metrics["path_deleted"] = True

        if mode == "full":
            if is_invocating_scripts(proc):
                score += CONFIG["weights"]["invokes_python"]
                justifications["invokes_python"] = True

            if not is_process_bound_to_a_service(proc):
                score += CONFIG["weights"]["not_bound_to_service"]
                justifications["not_bound_to_service"] = True

            if re.search(r"[^a-zA-Z0-9_:\\\.\- ]", exe_path):
                score += CONFIG["weights"]["strange_chars"]
                justifications["strange_chars"] = True
                raw_metrics["strange_chars"] = True

            try:
                if any(
                    conn.status == psutil.CONN_ESTABLISHED and conn.raddr
                    for conn in proc.net_connections(kind="inet")
                ):
                    score += CONFIG["weights"]["network_activity"]
                    justifications["network_active"] = True
                    raw_metrics["network_active"] = True
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                pass

        normalized = normalizing_score(score, MAX_SCORE)
        risk = analyze_score_risk(normalized)

        return {
            "pid": pid,
            "mode": mode,
            "score": normalized,
            "risk_level": risk,
            "justifications": justifications,
            "raw_metrics": raw_metrics,
        }

    except Exception as e:
        logger.exception(f"Error computing score for PID {pid}")
        return None
