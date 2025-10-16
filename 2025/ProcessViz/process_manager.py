import psutil, time, re
from utils import *
from config_loader import CONFIG


datas = {}
MAX_SCORE = 135


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

        if process_path != '' and process_path[-4:] == '.exe':
            process_hash = grab_sha256_hash_of_process(process_path)
        else:
            process_hash = None

    connections = process.net_connections()
    if connections:
        # Socket Address, Status of Connection
        active_connections = [connections[0][3], connections[0][-1]]
    else:
        active_connections = None

    datas[process_name] = {
            "PID": process_pid,
            "memory usage": round(process_memory_usage, 2),
            "path": process_path,
            "time alive": process_starting_time,
            "status": process_status,
            "connections": active_connections,
            "parent": process_parent,
            "hash": process_hash
        }


def get_infos_for_process_with_pid(pid):
    datas.clear()
    if psutil.pid_exists(pid):
        try:
            fetch_infos_for_process(psutil.Process(pid), pid)
        except (psutil.AccessDenied, psutil.NoSuchProcess) as error:
            pass
    else:
        return []
    return datas


def get_processes():
    """Function to loop in all existing process and to grab datas about them

    :return: datas
    :rtype: dict
    """
    for process_pid in psutil.pids():
        try:
            fetch_infos_for_process(psutil.Process(process_pid), process_pid)
        except (psutil.AccessDenied, psutil.NoSuchProcess) as error:
            continue
    return datas

#alived_pids_for_tests = [12700, 580, 11420]

def analyze_process(process_pid):
    score = 0
    justifications = {}
    
    raw_metrics =  {
        "path_suspicious": False,
        "path_trustworthy": False,
        "is_signed": True,
        "invokes_python": False,
        "not_bound_to_service": False,
        "path_deleted": False,
        "strange_chars": False,
        "network_active": False
    }

    current_process = psutil.Process(process_pid) if psutil.pid_exists(process_pid) else None

    if not current_process:
        return None

    try:
        exe_path = current_process.exe().lower()
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return None

    
    # Exec path not in standard folder
    for path in CONFIG["paths"]["suspicious"]:
        if exe_path.startswith(path):
            score += 20
            justifications["path_suspicious"] = True
            raw_metrics["path_suspicious"] = True

    # Exec path in sys path decrements non-trustfullness score
    for path in CONFIG["paths"]["trustworthy"]:
        if exe_path.startswith(path):
            score -= 20

    # Is not binary signed
    if not is_signed(exe_path):
        score += 30
        justifications["is_signed"] = True
        raw_metrics["is_signed"] = False

    # Invocating Python scripts
    if is_invocating_scripts(current_process):
        score += 20
        justifications["invokes_python"] = True
        raw_metrics["invokes_python"] = True

    # Non associe a un service mais lance comme systeme 15
    if not is_process_bound_to_a_service(current_process):
        score += 15
        justifications["not_bound_to_a_service"] = True
        raw_metrics["not_bound_to_service"] = True

    # Deleted path
    if is_deleted_executable(current_process):
        score += 15
        justifications["path_deleted"] = True
        raw_metrics["path_deleted"] = True

    # Strange char in path
    if re.search(r'[^a-zA-Z0-9_:\\\.\- ]', exe_path):
        score += 15
        justifications["strange_chars"] = True
        raw_metrics["strange_chars"] = True

    # Internet connections
    try:
        if any(conn.status == psutil.CONN_ESTABLISHED and conn.raddr for conn in current_process.net_connections(kind='inet')):
            score += 20
            justifications["network_active"] = True   
            raw_metrics["network_active"] = True
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        pass

    normalized = normalizing_score(score, MAX_SCORE)

    risk = analyze_score_risk(normalized)

    return {
        "score":normalized,
        "justifications":justifications,
        "raw_metrics":raw_metrics,
        "risk_level": risk
    }