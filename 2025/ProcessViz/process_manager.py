import psutil


def get_processes():
    process_datas = {}

    for process_pid in psutil.pids():
        name_of_process = psutil.Process(process_pid).name()
        memory_usage_of_process = psutil.Process(process_pid).memory_percent()
        process_datas[name_of_process] = {"memory usage": memory_usage_of_process}

    return process_datas