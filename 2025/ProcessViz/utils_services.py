import psutil, wmi

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
