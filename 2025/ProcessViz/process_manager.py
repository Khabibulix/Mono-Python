import psutil


def get_all_names_for__running_processes():
    names = []
    for process_pid in psutil.pids():
        names.append(psutil.Process(process_pid).name())
    return names

print(get_all_names_for__running_processes())