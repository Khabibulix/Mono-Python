import hashlib, subprocess, os, psutil, win32service, win32serviceutil


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

def open_session_SCM() -> dict:
    scm_handle = win32service.OpenSCManager(
        None,
        None, 
        win32service.SC_MANAGER_ENUMERATE_SERVICE
    )
    return scm_handle

def close_session_SCM(scm) -> None:
    win32service.CloseServiceHandle(scm)

def get_services() -> dict:
    service_map = {}
    scm = open_session_SCM()

    services, _ = win32service.EnumServicesStatusEx(
        scm,
        win32service.SC_ENUM_PROCESS_INFO,  # Niveau d'info: on veut les PIDs
        win32service.SERVICE_WIN32,         # Type: services classiques
        win32service.SERVICE_ACTIVE,        # Seulement les services actifs
        None                          # Resume handle pour pagination
    )

    for svc in services:
        pid = svc['ProcessId']
        name = svc['ServiceName']
        if pid > 0:
            service_map[pid] = name

    # services = win32service.EnumServicesStatus(
    #             scm,
    #             win32service.SERVICE_WIN32,
    #             win32service.SERVICE_STATE_ALL
    #         )
    
    # for service in services:
    #     name = service[0]
    #     try:
    #         status = win32serviceutil.QueryServiceStatus(name)
    #         pid = status[-1]
    #         if pid > 0:
    #             service_map[pid] = name
    #     except Exception:
    #         pass
    
    close_session_SCM(scm)
    return service_map

print(get_services())