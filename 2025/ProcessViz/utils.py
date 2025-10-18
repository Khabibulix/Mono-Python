import hashlib, subprocess, os, psutil, wmi


def grab_sha256_hash_of_process(path: str) -> str:
    h = hashlib.sha256()
    with open(path, 'rb') as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()

def is_signed(filepath: str) -> bool | str:
    signtool_path = os.path.join(os.path.dirname(__file__), "bin", "signtool.exe")
    try:
        result = subprocess.run(
            [signtool_path, "verify", "/pa", filepath],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True,
            check = False
        )
        output = result.stdout + result.stderr
        return "No signature found" not in output

    except FileNotFoundError:
        return "signtool.exe not found, must be in /bin folder"
    
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

def get_services() -> dict:
    results = {}

    for service in wmi.WMI().Win32_Service():
        
        try:
            pid = int(service.ProcessID) if service.ProcessID not in (None, '') else 0
        except Exception:
            pid = 0
        
        name = service.Name

        if pid > 0:
            results.setdefault(pid, []).append(name)
        
    return results


def is_process_bound_to_a_service(process: psutil.Process) -> bool:
    return process.pid in get_services()

def normalizing_score(score, max_score):
    return min(int((score / max_score) * 100), 100)

def analyze_score_risk(score: int) -> str:
    if score >= 80:
        return "critical"
    if score >= 50:
        return "warning"
    return "safe"

def build_process_tree(processes_by_pid):
    tree = {}
    children = {}

    for pid, info in processes_by_pid.items():
        parent = info["parent_pid"]
        if parent not in children:
            children[parent] = []
        children[parent].append(pid)

    def build_subtree(pid):
        node = {
            "pid":pid,
            "name": processes_by_pid[pid]["name"],
            "children": []
        }
        for child_pid in children.get(pid, []):
            node["children"].append(build_subtree(child_pid))
        return node
    
    #Find roots
    roots = [pid for pid in processes_by_pid if processes_by_pid[pid]["parent_pid"] not in processes_by_pid]

    forest = [build_subtree(pid) for pid in roots]
    return forest