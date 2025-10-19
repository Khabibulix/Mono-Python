import psutil, os

def is_invocating_scripts(process: psutil.Process) -> bool:
    try:
        cmdline = process.cmdline()
        name = process.name().lower()
        exe = process.exe() if process.exe() else ""

        if "python" in name or "python" in exe:
            return any(arg.endswith((".py", ".pyw")) or arg.startswith("-c") for arg in cmdline)
        return False
    
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False
    
    
def is_deleted_executable(process: psutil.Process) -> bool:
    try: 
        exe_path = process.exe()
        return not os.path.exists(exe_path)
    except (psutil.AccessDenied, psutil.NoSuchProcess):
        return False
    

def build_process_tree(processes_by_pid):
    """Build one or more process trees from a dictionary with process infos

    :param processes_by_pid: PID of the process we will visualize
    :type processes_by_pid: dict
    :return: Tree(s)
    :rtype: dict
    """
    from collections import defaultdict
    
    # Build childs table {parent_pid: [child_pid1, child_pid2, ...]}
    children_map = defaultdict(list)
    for pid, info in processes_by_pid.items():
        parent_pid = info["parent_pid"]
        children_map[parent_pid].append(pid)

    # Build node from a PID
    def build_node(pid):
        process_info = processes_by_pid[pid]
        return {
            "pid":pid,
            "name": process_info["name"],
            "children": [build_node(child_pid) for child_pid in children_map.get(pid, [])]
        }        
    
    #Find roots (process with unknown parents)
    roots_pids = [
            pid for pid, info in processes_by_pid.items() 
            if info["parent_pid"] not in processes_by_pid
        ]

    # Build forest from roots
    process_forest = [build_node(pid) for pid in roots_pids]
    return process_forest