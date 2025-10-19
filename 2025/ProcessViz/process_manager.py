import psutil, time, re, asyncio
from utils import *
from utils_process import *
from utils_services import *
from config_loader import CONFIG

MAX_SCORE = 135


class ProcessGetter:
    @staticmethod    
    async def fetch_infos_for_process(process, process_pid, include_opened_files=False):
        """Main function to provide infos about processes.
        Edits the dict named datas, for more infos about psutil module, see over here: https://psutil.readthedocs.io/en/latest/

        :param process: Process to analyze
        :type process: psutil.Process object
        :param process_pid: PID of the process
        :type process_pid: int
        """        

        with process.oneshot():
            info = process.as_dict(attrs=[
            "name", "memory_percent", "exe", "create_time", "status", "ppid"
        ])
            try:
                process_parent = process.parent().name() if process.parent() else None
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_parent = None
            
        process_path = info.get("exe", None)
        process_hash = None

        if process_path and process_path.endswith(".exe"):
            process_hash = await grab_sha256_async(process_path)

        process_opened_files = None
        process_opened_dll = None

        if include_opened_files:
            try:
                process_opened_files = [f.path for f in process.open_files()]
                
                raw_maps = process.memory_maps()
                opened_dll = []
                seen = set()
                
                for map in raw_maps:
                    path = getattr(map, 'path', None) or getattr(map, 'addr', None) or ''
                    if not path:
                        continue
                    if path in seen:
                        continue
                    seen.add(path)
                    
                    if not looks_like_shared_lib(path):
                        continue

                    accessible, err = is_readable(path)
                    opened_dll.append({
                        "path": path,
                        "accessible": accessible,
                        "error": err
                    })

                    process_opened_dll = opened_dll

            except (psutil.AccessDenied, psutil.NoSuchProcess, OSError):
                pass
                

        try:
            connections = process.net_connections()
            active_connections = []

            for conn in connections:
                addr = conn.raddr if conn.raddr else conn.laddr
                ip = addr.ip if hasattr(addr, 'ip') else addr[0]
                port = addr.port if hasattr(addr, 'port') else addr[1]
                status = conn.status
                active_connections.append(f"{ip}:{port} -> {status}")

            if not active_connections:
                active_connections = None

        except (psutil.AccessDenied, psutil.NoSuchProcess):
            active_connections = None

        return {
            "name": info["name"],
            "PID": process_pid,
            "memory usage": round(info["memory_percent"], 2),
            "path": process_path,
            "time alive": time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(info["create_time"])),
            "status": info["status"],
            "connections": active_connections,
            "parent": process_parent,
            "hash": process_hash,
            "parent_pid":info["ppid"],
            "opened_files":process_opened_files,
            "opened_dll":process_opened_dll
        }


    @staticmethod
    def get_infos_for_process_with_pid(pid):
        if not psutil.pid_exists(pid):
            return None
        try:
            return ProcessGetter.fetch_infos_for_process(psutil.Process(pid), pid, include_opened_files=True)
        except (psutil.AccessDenied, psutil.NoSuchProcess) as error:
            return None


    def get_processes():
        processes = {}
        for process_pid in psutil.pids():
            try:
                proc_info = ProcessGetter.fetch_infos_for_process(psutil.Process(process_pid), process_pid, include_opened_files=False)
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
        
