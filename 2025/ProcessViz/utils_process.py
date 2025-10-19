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
    
