import psutil, re
from app.utils import is_signed, normalizing_score, analyze_score_risk
from app.utils_process import is_invocating_scripts, is_deleted_executable
from app.utils_services import is_process_bound_to_a_service
from app.config_loader import get_config

MAX_SCORE = 135

class ProcessAnalyzer:
    def __init__(self, pid:int):
        self.pid = pid
        self.analysis = None

    
    async def run(self):
        CONFIG = await get_config()
        if not psutil.pid_exists(self.pid):
            return None

        try:
            proc = psutil.Process(self.pid)
            exe_path = proc.exe()
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return None

        score = 0
        justifications = {}
        raw_metrics = {
            "path_suspicious": False,
            "path_trustworthy": False,
            "is_signed": True,
            "invokes_python": False,
            "not_bound_to_service": False,
            "path_deleted": False,
            "strange_chars": False,
            "network_active": False
        }

        # Suspicious path
        for path in CONFIG["paths"]["suspicious"]:
            if exe_path.startswith(path.lower()):
                score += CONFIG["weights"]["suspicious_path"]
                justifications["path_suspicious"] = True
                raw_metrics["path_suspicious"] = True

        # Trustworthy path
        for path in CONFIG["paths"]["trustworthy"]:
            if exe_path.startswith(path.lower()):
                score += CONFIG["weights"]["trustworthy_path"]
                raw_metrics["path_trustworthy"] = True
                break

        # Signature
        if not is_signed(exe_path):
            score += CONFIG["weights"]["not_signed"]
            justifications["is_signed"] = True
            raw_metrics["is_signed"] = False

        # Invokes Python
        if is_invocating_scripts(proc):
            score += CONFIG["weights"]["invokes_python"]
            justifications["invokes_python"] = True
            raw_metrics["invokes_python"] = True

        # Not bound to service
        if not is_process_bound_to_a_service(proc):
            score += CONFIG["weights"]["not_bound_to_service"]
            justifications["not_bound_to_a_service"] = True
            raw_metrics["not_bound_to_service"] = True

        # Deleted path
        if is_deleted_executable(proc):
            score += CONFIG["weights"]["deleted_path"]
            justifications["path_deleted"] = True
            raw_metrics["path_deleted"] = True

        # Strange chars
        if re.search(r'[^a-zA-Z0-9_:\\\.\- ]', exe_path):
            score += CONFIG["weights"]["strange_chars"]
            justifications["strange_chars"] = True
            raw_metrics["strange_chars"] = True

        # Network activity
        try:
            if any(conn.status == psutil.CONN_ESTABLISHED and conn.raddr for conn in proc.net_connections(kind='inet')):
                score += CONFIG["weights"]["network_activity"]
                justifications["network_active"] = True
                raw_metrics["network_active"] = True
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            pass

        normalized = normalizing_score(score, MAX_SCORE)
        risk = analyze_score_risk(normalized)

        self.analysis = {
            "score": normalized,
            "justifications": justifications,
            "raw_metrics": raw_metrics,
            "risk_level": risk
        }

        return self.analysis
        
