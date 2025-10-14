import psutil, time
from utils import grab_sha256_hash_of_process, is_signed, is_invocating_scripts


datas = {}
SUSPICIOUS_PATHS = [
    r"C:\Users",
    r"C:\Temp",
    r"C:\Windows\Temp",
    r"C:\ProgramData",
    r"C:\$Recycle.Bin",
    r"C:\PerfLogs",
    r"C:\Logs"
]

POTENTIALLY_TRUSTFUL_PATHS = [
    r"C:\Windows\System32\drivers",
    r"C:\Windows\System32",
    r"C:\Windows"
]


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


    if len(process.net_connections()) > 0:
        # Socket Address, Status of Connection
        active_connections = [process.net_connections()[0][3], process.net_connections()[0][-1]]
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
    current_process = psutil.Process(process_pid) if psutil.pid_exists(process_pid) else None

    if not current_process:
        return

    # Exec path not in standard folder
    for path in SUSPICIOUS_PATHS:
        if current_process.exe().lower().startswith(path):
            score += 20
            justifications["Non standard path"] = True

    # Exec path in sys path decrements non-trustfullness score
    for path in POTENTIALLY_TRUSTFUL_PATHS:
        if current_process.exe().lower().startswith(path):
            score -= 20

    # Is binary signed
    if not is_signed(current_process.exe()):
        score += 30
        justifications["Not signed file signature"] = True

    # Invocating Python scripts
    if is_invocating_scripts(current_process):
        score += 20
        justifications["Invocating Python scripts"] = True

    # Binaire sys mais faux chemin 25

    # Non associe a un service mais lance comme systeme 15
    # Chemin supprime 15
    # Exécutable avec chemin contenant des caractères inhabituels 15
    # Communique avec Internet 20
    

    return {"score":score, "justifications":justifications}

print(analyze_process(11420)["score"])