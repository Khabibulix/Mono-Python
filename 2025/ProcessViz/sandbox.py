import wmi

s = wmi.WMI()
results = {}

for service in s.Win32_Service():
    
    try:
        pid = int(service.ProcessID) if service.ProcessID not in (None, '') else 0
    except Exception:
        pid = 0
    
    name = service.Name
    display = getattr(service, 'DisplayName', None)

    if pid > 0:
        results.setdefault(pid, []).append(name)
    
print(results)
