import hashlib, subprocess, os, psutil, wmi


def grab_sha256_hash_of_process(path_of_process):
    h = hashlib.sha256()
    with open(path_of_process, 'rb') as f:
        while True:
            chunk = f.read(65536)
            if not chunk:
                break
            h.update(chunk)
    return h.hexdigest()

def is_signed(filepath):
    signtool_path = os.path.join(os.path.dirname(__file__), "bin", "signtool.exe")
    try:
        result = subprocess.run(
            [signtool_path, "verify", "/pa", filepath],
            stdout = subprocess.PIPE,
            stderr = subprocess.PIPE,
            text = True
        )
        output = result.stderr + result.stdout
        return False if "No signature found" in output else True

    except FileNotFoundError as fnfe:
        return "signtool.exe not found, must be in /bin folder"
    
def is_invocating_scripts(process: psutil.Process) -> bool:
    try:
        cmd = process.cmdline()
        name = process.name().lower()
        exe = process.exe() if process.exe() else ""

        is_python_process = ("python" in name or "python" in exe.lower())

        if is_python_process:
            for arg in cmd:
                if arg.endswith(".py") or arg.endswith(".pyw") or arg.startswith("-c"):
                    return True
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
    return True if get_services().get(process.pid) is not None else False

def normalizing_score(score, max_score):
    return min(int((score / max_score) * 100), 100)

def analyze_score_risk(score):
    risk = ''
    if score >= 80:
        risk = "critical"
    elif score >= 50:
        risk = "warning"
    else:
        risk = "safe"
    return risk