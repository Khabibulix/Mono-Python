import psutil

def get_processes():
    process_datas = {}

    for process_pid in psutil.pids():

        current_process = psutil.Process(process_pid)
        name_of_process = current_process.name()
        memory_usage_of_process = current_process.memory_percent()
        
        if len(current_process.net_connections()) > 0:
            # Socket Address, Status of Connection
            active_connections = [current_process.net_connections()[0][3], current_process.net_connections()[0][-1]]
        else:
            active_connections = None

        process_datas[name_of_process] = {
            "PID": process_pid,
            "memory usage": round(memory_usage_of_process, 2),
            "connections": active_connections
        }

    return process_datas

all_processes = get_processes()
print(all_processes)