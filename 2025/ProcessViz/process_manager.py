import psutil, time, re
from utils import *
from config_loader import CONFIG

MAX_SCORE = 135


class ProcessGetter:
    @staticmethod    
    def fetch_infos_for_process(process, process_pid):
        """Main function to provide infos about processes.
        Edits the dict named datas, for more infos about psutil module, see over here: https://psutil.readthedocs.io/en/latest/

        :param process: Process to analyze
        :type process: psutil.Process object
        :param process_pid: PID of the process
        :type process_pid: int
        """
    
        with process.oneshot():
            process_name = process.name()
            process_memory_usage = process.memory_percent()
            process_path = process.exe()
            process_starting_time = (time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(process.create_time())))
            process_status = process.status()
            process_parent = process.parent().name() if process.parent() is not None else process.parent()   
            process_parent_pid = process.ppid()
            process_hash = grab_sha256_hash_of_process(process_path) if process_path.endswith('.exe') else None

        try:
            connections = process.net_connections()
            active_connections = [connections[0][3], connections[0][-1]] if connections else None
        except psutil.AccessDenied:
            active_connections = None

        return {
            "name": process_name,
            "PID": process.pid,
            "memory usage": round(process_memory_usage, 2),
            "path": process_path,
            "time alive": process_starting_time,
            "status": process_status,
            "connections": active_connections,
            "parent": process_parent,
            "hash": process_hash,
            "parent_pid":process_parent_pid
        }


    @staticmethod
    def get_infos_for_process_with_pid(pid):
        if not psutil.pid_exists(pid):
            return None
        try:
            return ProcessGetter.fetch_infos_for_process(psutil.Process(pid), pid)
        except (psutil.AccessDenied, psutil.NoSuchProcess) as error:
            return None


    def get_processes():
        processes = {}
        for process_pid in psutil.pids():
            try:
                proc_info = ProcessGetter.fetch_infos_for_process(psutil.Process(process_pid), process_pid)
                processes[proc_info["name"]] = proc_info
            except (psutil.AccessDenied, psutil.NoSuchProcess) as error:
                continue
        return processes


class ProcessAnalyzer:
    def __init__(self, pid:int):
        self.pid = pid
        self.analysis = None
    
    def run(self):
        if not psutil.pid_exists(self.pid):
            return None

        try:
            proc = psutil.Process(self.pid)
            exe_path = proc.exe().lower()
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
            if exe_path.startswith(path):
                score += 20
                justifications["path_suspicious"] = True
                raw_metrics["path_suspicious"] = True

        # Trustworthy path
        for path in CONFIG["paths"]["trustworthy"]:
            if exe_path.startswith(path):
                score -= 20
                raw_metrics["path_trustworthy"] = True

        # Signature
        if not is_signed(exe_path):
            score += 30
            justifications["is_signed"] = True
            raw_metrics["is_signed"] = False

        # Invokes Python
        if is_invocating_scripts(proc):
            score += 20
            justifications["invokes_python"] = True
            raw_metrics["invokes_python"] = True

        # Not bound to service
        if not is_process_bound_to_a_service(proc):
            score += 15
            justifications["not_bound_to_a_service"] = True
            raw_metrics["not_bound_to_service"] = True

        # Deleted path
        if is_deleted_executable(proc):
            score += 15
            justifications["path_deleted"] = True
            raw_metrics["path_deleted"] = True

        # Strange chars
        if re.search(r'[^a-zA-Z0-9_:\\\.\- ]', exe_path):
            score += 15
            justifications["strange_chars"] = True
            raw_metrics["strange_chars"] = True

        # Network activity
        try:
            if any(conn.status == psutil.CONN_ESTABLISHED and conn.raddr for conn in proc.net_connections(kind='inet')):
                score += 20
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
        
