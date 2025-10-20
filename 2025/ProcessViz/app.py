import pythoncom, os, re, logging, asyncio
from setup_log import setup_logger
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
            data = await ProcessGetter.get_processes()
            process_cache = data
            logger.debug("Process cache updated with %d entries", len(data))
        except Exception as e:
            logger.warning("Cache refresh error: %s", e)
        await asyncio.sleep(3)

@app.context_processor
def utility_processor():
    def basename(path):
        return os.path.basename(path)
    return dict(basename=basename)

@app.before_serving
async def startup():
    app.add_background_task(refresh_cache)

@app.route("/")
async def display_processes():
    if process_cache is None:
        return await render_template("loading.html"), 503
    return await render_template('index.html', get_processes=process_cache)

@app.route("/process/<int:pid>")
async def process_view(pid):
    async def fetch_and_analyze():
        pythoncom.CoInitialize()
        try:
            logger.info("Analyzing process PID=%d", pid)
            infos = await ProcessGetter.get_infos_for_process_with_pid(pid)
            if not infos:
                logger.warning("Process PID=%d not found", pid)
                return None, None
            analyzer = ProcessAnalyzer(pid)
            result = analyzer.run()
            return infos, result
        finally:
            pythoncom.CoUninitialize()
    
    infos, result = await fetch_and_analyze

    if not infos:
        return "Process not found", 404
    return await render_template('process.html', process_info=infos, result=result)

@app.route("/tree")
async def display_process_tree():
    if process_cache is None:
        logger.warning("Cache not ready when accessing /tree")
        return await render_template("loading.html"), 503
    
    processes_by_pid = {
        v["PID"]: v for v in process_cache.values()
    }

    logger.debug("Building process tree from %d processes", len(processes_by_pid))

    try:
        tree = build_process_tree(processes_by_pid)
    except Exception as e:
        logger.exception("Error building process tree")
        return "Internal error while building tree", 500

    return await render_template("tree.html", process_tree=tree)

@app.route("/process/<int:pid>/dll")
async def dll_view(pid):
    path = request.args.get("path")
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
    loop = asyncio.new_event_loop()
    asyncio.set_event_loop(loop)
    loop.set_debug(True)

    logger = setup_logger(__name__)
    logger.info("Launching Quart app...")
    
    app.run(debug=False)