import pythoncom, asyncio, os, re
from quart import Quart, render_template, request, abort
from process_manager import *
from utils import is_readable
from urllib.parse import unquote_plus

app = Quart(__name__)

process_cache = None

async def refresh_cache():
    global process_cache
    while True:
        try:
            data = await asyncio.to_thread(ProcessGetter.get_processes)
            process_cache = data
        except Exception as e:
            print("Cache error")
        await asyncio.sleep(3)

# For using WMI in Quart context
def run_wmi_function(fn, *args, **kwargs):
    pythoncom.CoInitialize()
    try:
        return fn(*args, **kwargs)
    finally:
        pythoncom.CoUninitialize()

@app.before_serving
async def startup():
    app.add_background_task(refresh_cache)

@app.route("/")
async def display_processes():
    if process_cache is None:
        return "⏳ Loading datas, you'll be kind to wait a bit...", 503
    return await render_template('index.html', get_processes=process_cache)

@app.route("/process/<int:pid>")
async def process_view(pid):
    def fetch_and_analyze():
        pythoncom.CoInitialize()
        try:
            infos = ProcessGetter.get_infos_for_process_with_pid(pid)
            if not infos:
                return None, None
            analyzer = ProcessAnalyzer(pid)
            result = analyzer.run()
            return infos, result
        finally:
            pythoncom.CoUninitialize()
    
    infos, result = await asyncio.to_thread(fetch_and_analyze)

    if not infos:
        return "Process not found", 404
    return await render_template('process.html', process_info=infos, result=result)

@app.route("/tree")
async def display_process_tree():
    if process_cache is None:
        return "Loading...", 503
    
    processes_by_pid = {
        v["PID"]: v for v in process_cache.values()
    }

    tree = build_process_tree(processes_by_pid)

    return await render_template("tree.html", process_tree=tree)

@app.route("/process/<int:pid>/dll")
async def dll_view(pid):
    path = request.arg.get("path")
    if not path:
        abort(400, "Missing path param")

    path = unquote_plus(path)
    readable, error = is_readable(path)
    if not readable:
        abort(403, f"Cannot access DLL: {error}")
    
    try:
        with open(path, 'rb') as f:
            data = f.read(64 * 1024)
    except Exception as e:
        abort(500, f"Error reading file: {e}")

    ascii_strings = re.findall(rb'[\x20-\x7E]{4,}', data)
    strings = [s.decode('ascii', errors='ignore') for s in ascii_strings[:100]]

    def hexdump(data:bytes, length:int = 16):
        result = []
        for i in range(0, min(len(data), 512), length):
            chunk = data[i:i+length]
            hex_part = ' '.join(f'{b:02x}' for b in chunk)
            # Classic ASCII Chars, 32 is ' ' and 127 is '~'
            ascii_part = ''.join(chr(b) if 32 <= b < 127 else '.' for b in chunk)
            result.append(f"{i:08x} {hex_part:<48} |{ascii_part}|")
        return result
    
    hex_lines = hexdump(data)

    return await render_template(
        "dll.html",
        pid=pid,
        path=path,
        strings=strings,
        hexdump=hex_lines    
    )


if __name__ == "__main__":
    app.run(debug=True)