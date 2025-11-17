import asyncio
import psutil
import time
from app.utils.utils import grab_sha256_async


class ProcessGetter:
    @staticmethod
    async def fetch_infos_for_process(process, process_pid, include_opened_files=False):
        """Main function to provide infos about processes.
        Edits the dict named datas, for more infos about psutil module, see over here: https://psutil.readthedocs.io/en/latest/

        :param process: Process to analyze
        :type process: psutil.Process object
        :param process_pid: PID of the process
        :type process_pid: int
        """

        with process.oneshot():
            info = process.as_dict(
                attrs=["name", "memory_percent", "exe", "create_time", "status", "ppid"]
            )
            try:
                process_parent = process.parent().name() if process.parent() else None
            except (psutil.NoSuchProcess, psutil.AccessDenied):
                process_parent = None

        process_path = info.get("exe", None)
        process_hash = None

        if process_path and process_path.endswith(".exe"):
            process_hash = await grab_sha256_async(process_path)

        process_opened_files = None
        process_opened_dll = None

        if include_opened_files:
            try:
                loop = asyncio.get_event_loop()
                from app.utils.utils_process import get_dll_info_sync
                process_opened_dll = await loop.run_in_executor(
                    None, get_dll_info_sync, process
                )
            except Exception:
                process_opened_dll = None

        try:
            connections = process.net_connections()
            active_connections = []

            for conn in connections:
                addr = conn.raddr if conn.raddr else conn.laddr
                ip = addr.ip if hasattr(addr, "ip") else addr[0]
                port = addr.port if hasattr(addr, "port") else addr[1]
                status = conn.status
                active_connections.append(f"{ip}:{port} -> {status}")

            if not active_connections:
                active_connections = None

        except (psutil.AccessDenied, psutil.NoSuchProcess):
            active_connections = None

        return {
            "name": info["name"],
            "PID": process_pid,
            "memory_percent": round(info["memory_percent"], 2),
            "path": process_path,
            "time_alive": time.strftime(
                "%d-%m-%Y %H:%M:%S", time.localtime(info["create_time"])
            ),
            "status": info["status"],
            "connections": active_connections,
            "parent": process_parent,
            "hash": process_hash,
            "parent_pid": info["ppid"],
            "opened_files": process_opened_files,
            "opened_dll": process_opened_dll,
        }

    @staticmethod
    async def get_infos_for_process_with_pid(pid):
        if not psutil.pid_exists(pid):
            return None
        try:
            return await ProcessGetter.fetch_infos_for_process(
                psutil.Process(pid), pid, include_opened_files=True
            )
        except (psutil.AccessDenied, psutil.NoSuchProcess):
            return None

    @staticmethod
    async def get_processes():
        processes = {}

        async def gather_process_info(pid):
            try:
                proc = psutil.Process(pid)
                info = await ProcessGetter.fetch_infos_for_process(
                    proc, pid, include_opened_files=False
                )
                return pid, info
            except (psutil.AccessDenied, psutil.NoSuchProcess):
                return None

        pids = psutil.pids()
        tasks = [gather_process_info(pid) for pid in pids]

        semaphore = asyncio.Semaphore(20)

        async def sem_task(task):
            async with semaphore:
                return await task

        sem_tasks = [sem_task(task) for task in tasks]
        for res in await asyncio.gather(*sem_tasks):
            if res is not None:
                pid, info = res
                processes[pid] = info

        return processes
