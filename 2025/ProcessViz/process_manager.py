import psutil, time

datas = {}

def fetch_infos_for_process(process, process_pid):
    
    with process.oneshot():
        process_name = process.name()
        process_memory_usage = process.memory_percent()
        process_path = process.exe()
        process_starting_time = (time.strftime("%d-%m-%Y %H:%M:%S", time.localtime(process.create_time())))
        process_status = process.status()
        process_parent = process.parent().name() if process.parent() is not None else process.parent()




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
            "parent": process_parent # Name of parent process
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
    for process_pid in psutil.pids():
        try:
            fetch_infos_for_process(psutil.Process(process_pid), process_pid)
        except (psutil.AccessDenied, psutil.NoSuchProcess) as error:
            continue
    return datas
